import json
import tempfile
import unittest
from pathlib import Path
from teacher_audit import audit

class TeacherAuditTest(unittest.TestCase):
    def test_replay_without_formal_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / "ledger/replay/2026-11-24.json"
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps({"date":"2026-11-24","previous_close":100,"models":{"V0":{"center":100},"V1":{"center":103}}}))
            q = [{"id":"test","stage":"OPEN","priority":1}]
            first = audit(q, root)
            self.assertEqual(first["gate"]["status"], "CONTINUE")
            self.assertIn("blocker", first["replays"][0])
            e = root / "reports/2026-11-24/evening.json"
            e.parent.mkdir(parents=True)
            e.write_text(json.dumps({"market_context":{}}))
            self.assertIn("blocker", audit(q, root)["replays"][0])
            e.write_text(json.dumps({"market_context":{"TAIEX":{"status":"PASS","source_date":"2026-11-24","source":"TWSE MI_5MINS_HIST","open":102}}}))
            second = audit(q, root)
            self.assertEqual(second["replays"][0]["scores"]["V1"]["absolute_error"],1)
            self.assertTrue(second["replays"][0]["scores"]["V1"]["direction_match"])
            self.assertEqual(second["replays"][0]["scores"]["V0"]["signed_error"],-2)

    def test_official_fallback_date(self):
        from teacher_audit import official_open
        rows = [{"Date":"115/11/23","OpeningIndex":"99"},{"Date":"115/11/24","OpeningIndex":"102.5"}]
        self.assertEqual(official_open("2026-11-24", rows)["open"],102.5)
        self.assertEqual(official_open("2026-11-25", rows),{})

    def test_monthly_fallback_settles_only_exact_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            replay = root / "ledger/replay/2026-11-24.json"
            replay.parent.mkdir(parents=True)
            replay.write_text(json.dumps({
                "date": "2026-11-24", "previous_close": 100,
                "models": {"V0": {"center": 100}},
            }))
            monthly = lambda day: [
                {"Date": "115/11/23", "OpeningIndex": "99"},
                {"Date": "115/11/24", "OpeningIndex": "102"},
            ]
            result = audit([], root, lambda: [], monthly)["replays"][0]
            self.assertEqual(result["actual"], 102)
            self.assertIn("date=20261101", result["actual_ref"])
