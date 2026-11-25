import unittest
from datetime import datetime
from unittest.mock import patch

from opening_review import review
from paper_actions import evaluate, summarize
from report_handoff import document_status, qualify, report_chain


class ReportHandoffTest(unittest.TestCase):
    def test_missing_optional_document_does_not_hide_other_paths(self):
        status = document_status({"docs/REPORT_CONTRACT.md"}, ["docs/REPORT_CONTRACT.md", "docs/old.md"])
        self.assertEqual(status["docs/old.md"], "MISSING_AT_PINNED_COMMIT")
        self.assertEqual(status["docs/REPORT_CONTRACT.md"], "PRESENT_AT_PINNED_COMMIT")

    def test_missing_original_and_late_replay_do_not_become_formal(self):
        self.assertEqual(qualify("ref", "2026-11-25", None)[1], "MISSING_ORIGINAL")
        record = {"published": "2026-11-25T09:01:00+08:00"}
        self.assertEqual(qualify("ref", "2026-11-25", record)[1], "OUTSIDE_PREOPEN_WINDOW")

    def test_paired_comparison_holds_v0_dates_constant(self):
        common = {"eligible": True, "original_ref": "ledger", "actual_ref": "TWSE",
                  "actual": 103, "previous_close": 100}
        base = {"V0-CARRY": {"center": 100}}
        records = [
            {**common, "date": "2026-11-24", "models": base},
            {**common, "date": "2026-11-25", "models": {**base, "V1-TX-ZERO-BASIS": {"center": 104}}},
        ]
        score = review(records)["paired_metrics"]["5"]["models"]["V1-TX-ZERO-BASIS"]
        self.assertEqual((score["n"], score["mae"], score["v0_mae_same_dates"]), (1, 1, 3))
        with self.assertRaises(ValueError):
            review(records + [records[1]])

    def test_after_cutoff_input_rejects_even_when_ledger_preopen(self):
        day = "2026-11-25"
        record = {"published": day + "T08:40:00+08:00", "ref": "ledger",
                  "text": "OPEN-20261125-AM Source ref " + "a" * 40}
        source = {"generated_at_taipei": day + "T08:37:00+08:00",
                  "source_fetched_at": {"market": day + "T08:21:00+08:00",
                                        "cross": day + "T08:39:00+08:00"}}
        with patch("report_handoff.subprocess.run") as git, patch(
            "report_handoff.publication", return_value=(day + "T08:37:30+08:00", source)
        ):
            git.return_value.returncode = 0
            self.assertEqual(qualify("ref", day, record)[1], "SOURCE_OUTSIDE_CUTOFF")

    def test_original_evening_handoff_and_next_morning_readback(self):
        day = "2026-11-25"
        previous_path = "predictions/2026-11-24/evening.md"
        morning_path = f"predictions/{day}/morning.md"
        evening_path = f"predictions/{day}/evening.md"
        next_path = "predictions/2026-11-26/morning.md"
        entries = {
            previous_path: {"ref": "prior:" + previous_path, "text": "[RESEARCH_STATE]\nstate"},
            morning_path: {"ref": "original:" + morning_path, "text": ""},
            evening_path: {"ref": "evening:" + evening_path, "text": "[RESEARCH_STATE]\nstate"},
            next_path: {"ref": "next:" + next_path, "text": "[RESEARCH_STATE]\nparent evening:" + evening_path},
        }
        forecast = {"date": day, "source_ref": "data"}
        with patch("report_handoff.original", side_effect=lambda ref, path: entries.get(path)), patch(
            "report_handoff.qualify", return_value=(forecast, "VERIFIED_PREOPEN_ORIGINAL")
        ), patch("report_handoff.publication", return_value=("time", {
            "market_context": {"TAIEX": {"status": "PASS", "source_date": "2026-11-24"}}
        })):
            result = report_chain("data", day, sorted(entries), lambda _: {"open": 102, "ref": "TWSE"})
            self.assertEqual(result["previous_evening_state"], "AVAILABLE")
            self.assertEqual(result["settlement_status"], "OFFICIAL_SETTLED")
            self.assertEqual(result["next_morning_handoff"], "VERIFIED")
            del entries[previous_path]
            result = report_chain("data", day, sorted(entries), lambda _: {"open": 102, "ref": "TWSE"})
            self.assertEqual(result["previous_evening_state"], "MISSING")

    def test_paper_costs_and_locked_session(self):
        action = {
            "id": "ACT-1", "version": "v1", "symbol": "2330",
            "rule": "PREPLACED_BUY_LIMIT_OPEN_TO_OPEN", "limit": 102,
            "entry_day": "2026-11-25", "exit_day": "2026-11-26",
            "earliest_at": "2026-11-25T08:45:00+08:00", "invalidation": "CANCEL_IF_ENTRY_AUCTION_MISSED",
            "benchmark": "0050", "costs": {"version": "sim-v1", "trade_method": "cash_swing",
                "instrument_type": "stock", "fee_bps_per_side": 15, "sell_tax_bps": 30,
                "slippage_bps_per_side": 10},
        }
        published = datetime.fromisoformat("2026-11-25T08:40:00+08:00")

        def quote(symbol, day):
            price = (100 if day.endswith("25") else 104) if symbol == "2330" else 50
            return {"open": price, "low": price - 1, "high": price + 1,
                    "volume": 1000, "ref": day}

        row = evaluate(action, published, quote, "2026-11-26")
        self.assertEqual(row["status"], "SIMULATED")
        self.assertLess(row["net_return"], 0.04)
        self.assertEqual(summarize([row])["n"], 1)
        self.assertEqual(evaluate(action, published, lambda *_: {}, "2026-11-26")["status"],
                         "NO_EXECUTION_EVIDENCE")
        self.assertEqual(evaluate({**action, "limit": 99}, published, quote, "2026-11-26")["status"],
                         "NOT_TRIGGERED")
        def locked(symbol, day):
            row = quote(symbol, day)
            return {**row, "low": row["open"], "high": row["open"]}
        self.assertEqual(evaluate(action, published, locked, "2026-11-26")["status"],
                         "NO_EXECUTION_EVIDENCE")
        late = datetime.fromisoformat("2026-11-25T09:10:00+08:00")
        self.assertEqual(evaluate(action, late, quote, "2026-11-26")["status"], "INVALID_RULE")
