import unittest
from datetime import datetime

from scripts.preparation_gate import decision
from scripts.publish_overlay import rank


def moment(day, clock):
    return datetime.fromisoformat(f"{day}T{clock}+08:00")


class PreparationGateTests(unittest.TestCase):
    def setUp(self):
        self.day = "2026-11-25"
        self.ready = {
            "scenario": "morning", "execution_kind": "REPORT",
            "generated_at_taipei": "2026-11-25T08:28:16+08:00",
            "readiness": {"data_readiness": "DATA_READY", "sections": {"cutoff": {"status": "PASS"}}},
        }

    def test_retries_resume_from_a_committed_complete_bundle(self):
        now = moment(self.day, "08:34:00")
        committed = "2026-11-25T00:28:24+00:00"
        for kind in ("REQUEST_PREPARATION", "SCHEDULED_PREPARATION"):
            result = decision("morning", kind, now, self.ready, committed)
            self.assertEqual(result, "SKIP_DUPLICATE_READY")
        for invalid in (None, "2026-11-25T00:39:00+00:00", "2026-11-24T00:28:00+00:00"):
            self.assertEqual(decision("morning", "SCHEDULED_PREPARATION", now, self.ready, invalid), "COLLECT")

    def test_stale_source_keeps_backup_eligible(self):
        self.ready["readiness"]["data_readiness"] = "DATA_PARTIAL"
        self.assertEqual(decision("morning", "SCHEDULED_PREPARATION", moment(self.day, "08:34:00"),
                                  self.ready, "2026-11-25T00:28:24+00:00"), "COLLECT")

    def test_cross_midnight_scheduled_run_cannot_collect_next_day(self):
        start = moment("2026-11-17", "00:27:33")
        self.assertEqual(decision("evening", "SCHEDULED_PREPARATION", start), "SKIP_OUTSIDE_WINDOW")
        self.assertEqual(decision("evening", "PREVIEW", start), "COLLECT")
        self.assertEqual(decision("evening", "REQUEST_PREPARATION", moment(self.day, "22:58:01")),
                         "SKIP_OUTSIDE_WINDOW")

    def test_early_evening_cannot_rank_as_timely_even_if_legacy_cutoff_passed(self):
        record = {**self.ready, "scenario": "evening", "generated_at_taipei": "2026-11-25T07:41:40+08:00",
                  "publication_check_at_taipei": "2026-11-25T07:41:43+08:00"}
        record["readiness"]["cutoff_taipei"] = "2026-11-25T22:58:00+08:00"
        self.assertFalse(rank(record)[0])
