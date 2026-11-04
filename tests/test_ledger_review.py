import json
import unittest
from datetime import datetime

from ledger_review import TZ, audit, predictions, settle


TEXT = """[PREDICTION_LEDGER]
PREDICTION_ID: 2026-11-03-PM-2330-01
原始字句: 預測2026-11-04台積電收盤低於2295元。
數字門檻: 2026-11-04 official 2330 close <2295.00 TWD
期間: 2026-11-04 regular session
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
PREDICTION_ID: FAKE-RECAP
[/ROLLING_ERROR_LOG]
"""


def report(close=2260, source_date="2026-11-04", status="PASS"):
    return json.dumps({"generated_at_taipei": "2026-11-04T23:45:00+08:00",
                       "readiness": {"overall": "DATA_PARTIAL"},
                       "stocks": {"2330": {
                           "daily_ohlcv": {"status": status, "source_date": source_date,
                                           "data": {"stock_id": "2330", "date": source_date, "close": close}},
                           "metrics": {"source": "FinMind TaiwanStockPrice"}}}})


class LedgerReviewTests(unittest.TestCase):
    def setUp(self):
        self.prediction = predictions(TEXT)[0]
        self.now = datetime(2026, 11, 5, 8, tzinfo=TZ)

    def evaluate(self, raw):
        return settle(self.prediction, lambda _: raw, self.now)

    def test_partial_report_does_not_block_valid_individual_outcome(self):
        result = self.evaluate(report())
        self.assertEqual(result["status"], "PROVIDER_MATCHED")
        self.assertEqual(result["outcome"], "HIT")
        self.assertFalse(result["formal_score_eligible"])
        self.assertEqual(result["evidence"]["source"], "FinMind TaiwanStockPrice")

    def test_equal_threshold_is_miss_for_strict_less_than(self):
        self.assertEqual(self.evaluate(report(close=2295))["outcome"], "MISS")

    def test_future_target_never_uses_existing_future_outcome(self):
        early = datetime(2026, 11, 4, 9, tzinfo=TZ)
        result = settle(self.prediction, lambda _: report(), early)
        self.assertEqual(result["status"], "PENDING")
        self.assertNotIn("actual", result)

    def test_wrong_date_nan_or_failed_section_cannot_settle(self):
        for raw in [report(source_date="2026-11-03"), report(close=float("nan")), report(status="STALE"), report(close=0)]:
            with self.subTest(raw=raw):
                self.assertEqual(self.evaluate(raw)["status"], "UNVERIFIABLE")

    def test_conditional_threshold_not_silently_reduced_to_close(self):
        self.prediction["fields"]["數字門檻"] += "; conditional on official prior baseline"
        self.assertEqual(self.evaluate(report())["reason"], "CONDITIONAL_RULE_NEEDS_REVIEW")

    def test_missing_or_malformed_outcome_is_explicit(self):
        for raw in [None, "not json", "[]"]:
            self.assertEqual(self.evaluate(raw)["status"], "UNVERIFIABLE")

    def test_future_generation_cannot_leak_into_as_of_review(self):
        raw = json.loads(report())
        raw["generated_at_taipei"] = "2026-11-06T00:00:00+08:00"
        self.assertEqual(self.evaluate(json.dumps(raw))["reason"], "FUTURE_OR_UNZONED_OUTCOME")

    def test_invalid_target_date_fails_closed(self):
        self.prediction["fields"]["期間"] = "2026-02-30 regular session"
        self.prediction["fields"]["數字門檻"] = "2026-02-30 official 2330 close <2295.00 TWD"
        self.assertEqual(self.evaluate(report())["reason"], "INVALID_TARGET_DATE")

    def test_market_provider_outcome_is_not_official_certification(self):
        self.prediction["id"] = "2026-11-03-PM-MKT-01"
        raw = json.loads(report())
        raw["market_context"] = {"TAIEX": {"status": "PASS", "source_date": "2026-11-04",
                                            "source": "FinMind TaiwanStockPrice TAIEX", "close": 42948.91}}
        self.prediction["fields"]["數字門檻"] = "official TAIEX close <43307.54"
        result = self.evaluate(json.dumps(raw))
        self.assertEqual(result["outcome"], "HIT")
        self.assertEqual(result["status"], "PROVIDER_MATCHED")
        self.assertFalse(result["formal_score_eligible"])

    def test_thousands_separator_not_truncated_into_false_hit(self):
        self.prediction["fields"]["數字門檻"] = "official 2330 close >1,000.00"
        result = self.evaluate(report(close=900))
        self.assertEqual(result["threshold"], 1000)
        self.assertEqual(result["outcome"], "MISS")

    def test_wrong_instrument_rule_cannot_use_id_instrument(self):
        self.prediction["fields"]["數字門檻"] = "official 5483 close <2295.00"
        self.assertEqual(self.evaluate(report())["reason"], "RULE_INSTRUMENT_MISMATCH")

    def test_compound_or_extra_clause_is_not_silently_ignored(self):
        for suffix in [" and volume >100000000", "; if trend holds", " 且量增"]:
            self.prediction["fields"]["數字門檻"] = "official 2330 close <2295.00" + suffix
            self.assertEqual(self.evaluate(report())["status"], "UNVERIFIABLE")

    def test_rule_date_must_match_explicit_period(self):
        self.prediction["fields"]["數字門檻"] = "official 2026-11-03 2330 close <2295.00"
        self.assertEqual(self.evaluate(report())["reason"], "RULE_TARGET_DATE_MISMATCH")

    def test_malformed_nested_shape_does_not_abort_batch(self):
        for stocks in [[], "bad", {"2330": []}, {"2330": {"daily_ohlcv": {"data": []}}}]:
            raw = json.loads(report())
            raw["stocks"] = stocks
            self.assertEqual(self.evaluate(json.dumps(raw))["status"], "UNVERIFIABLE")

    def test_only_original_block_is_parsed(self):
        self.assertEqual(len(predictions(TEXT)), 1)
        self.assertEqual(predictions("no original block"), [])

    def test_na_open_not_reconstructed(self):
        self.prediction["id"] = "OPEN-20261104-AM"
        self.assertEqual(self.evaluate(report())["status"], "NOT_TESTED")

    def test_erratum_preserves_input_and_does_not_reconcile_scope(self):
        original = TEXT + "\nvolume value TWD 11148.21 billion"
        result = audit({"predictions/2026-11-04/evening.md": original}, lambda _: report(), self.now, "abc")
        self.assertIn("TWD 11148.21 billion", original)
        self.assertEqual(len(result["errata"]), 1)
        self.assertEqual(result["errata"][0]["status"], "SUSPECTED_UNIT_ERROR_NEEDS_SOURCE_RECONCILIATION")
        self.assertNotIn("corrected", result["errata"][0])


if __name__ == "__main__":
    unittest.main()
