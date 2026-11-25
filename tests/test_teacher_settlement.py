import unittest

from opening_review import review
from report_handoff import settlement_summary


class TeacherSettlementTests(unittest.TestCase):
    def test_duplicate_replay_attempts_count_one_session_and_never_enter_formal_metrics(self):
        formal = review([{
            "date": "2026-11-25", "eligible": True, "actual": 103, "previous_close": 100,
            "original_ref": "original", "actual_ref": "official",
            "models": {"V0-CARRY": {"center": 100}},
        }, {"date": "2026-11-24", "eligible": False}])
        baseline = {
            "date": "2026-11-24", "record": "ledger/replay/2026-11-24.json",
            "actual": 102, "actual_ref": "official",
            "actual_evidence": {"status": "PASS", "source_date": "2026-11-24",
                                "source": "TWSE MI_5MINS_HIST direct"},
            "scores": {"V0-CARRY": {"signed_error": -2}},
        }
        retry = {**baseline, "record": "ledger/replay/2026-11-24-retry.json"}
        bad_source = {**baseline, "date": "2026-11-23"}
        result = settlement_summary(formal, [retry, bad_source, baseline, retry])
        self.assertEqual(result["formal"], {"n": 1, "dates": ["2026-11-25"]})
        self.assertEqual(result["replay"]["n"], 1)
        self.assertEqual(result["replay"]["by_date"]["2026-11-24"]["record"], baseline["record"])
        self.assertEqual(result, settlement_summary(formal, [baseline, retry, baseline]))

    def test_missing_replay_evidence_is_distinct_from_zero_samples(self):
        self.assertIsNone(settlement_summary({"rows": []}, None)["replay"]["n"])
        self.assertEqual(settlement_summary({"rows": []}, [])["replay"]["n"], 0)
