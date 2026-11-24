import unittest
from execution_supervisor import stop_gate

class StopGateTest(unittest.TestCase):
    def test_pr_not_done(self):
        q=[{"id":"a","stage":"PR","priority":1,"evidence":{"PR":"51"}}]
        self.assertFalse(stop_gate(q,[])["stop_allowed"])
        self.assertFalse(stop_gate(q,[{"id":"a","outcome":"PROGRESS"}])["stop_allowed"])
    def test_wait_does_not_skip_independent_work(self):
        q=[{"id":"a","stage":"OPEN","priority":1},{"id":"b","stage":"OPEN","priority":2}]
        a={"id":"a","action":"reproduce_and_patch","outcome":"EXTERNAL_BLOCKER","evidence":"provider unavailable","retry_condition":"provider restored"}
        self.assertEqual(stop_gate(q,[a])["next"]["id"],"b")
        self.assertTrue(stop_gate(q[:1],[a])["stop_allowed"])
    def test_stale_blocker(self):
        self.assertFalse(stop_gate([{"id":"a","stage":"OPEN","priority":1,"blocked":"old"}],[])["stop_allowed"])
    def test_empty(self):
        self.assertTrue(stop_gate([],[])["stop_allowed"])
