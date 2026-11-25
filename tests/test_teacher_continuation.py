import json
import subprocess
import unittest
from datetime import datetime
from unittest.mock import patch

from report_handoff import correction_handoffs, evening_status


class TeacherContinuationTests(unittest.TestCase):
    def test_evening_not_due_missing_and_lookup_error_are_distinct(self):
        day = "2026-11-25"
        early = datetime.fromisoformat(day + "T19:00:00+08:00")
        late = datetime.fromisoformat(day + "T23:05:00+08:00")
        with patch("report_handoff.git", return_value=""):
            self.assertEqual(evening_status("ref", day, early)["status"], "NOT_DUE")
            self.assertEqual(evening_status("ref", day, late)["status"], "MISSING_AFTER_DEADLINE")
        with patch("report_handoff.git", side_effect=subprocess.CalledProcessError(1, "git")):
            self.assertEqual(evening_status("ref", day, early)["status"], "LOOKUP_FAILED")

    def test_exact_correction_and_next_morning_state_are_required(self):
        day = "2026-11-25"
        correction = "ledger/corrections/2026-11-25-breadth.json"
        morning = f"predictions/{day}/morning.md"
        evening = f"predictions/{day}/evening.md"
        next_morning = "predictions/2026-11-26/morning.md"
        records = {
            correction: {"ref": "c:" + correction, "text": json.dumps({
                "date": day, "id": "BREADTH", "original_ref": "m:" + morning,
            })},
            morning: {"ref": "m:" + morning, "text": "immutable"},
            evening: {"ref": "e:" + evening, "text": "BREADTH"},
            next_morning: {"ref": "n:" + next_morning, "text": "parent e:" + evening},
        }
        with patch("report_handoff.git", return_value=correction), patch(
            "report_handoff.original", side_effect=lambda ref, path: records.get(path)
        ):
            self.assertEqual(correction_handoffs("ref", day, [next_morning])["status"],
                             "EVENING_CORRECTION_REF_MISSING")
            records[evening]["text"] = "adopt c:" + correction
            self.assertEqual(correction_handoffs("ref", day, [next_morning])["status"],
                             "NEXT_MORNING_REF_MISSING")
            records[next_morning]["text"] = "[RESEARCH_STATE]\nparent e:" + evening
            self.assertEqual(correction_handoffs("ref", day, [next_morning])["status"], "VERIFIED")
