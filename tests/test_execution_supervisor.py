import unittest
from execution_supervisor import supervise

class SupervisorTest(unittest.TestCase):
    def test_pending(self):
        self.assertEqual(supervise([{"id":"a","stage":"OPEN","priority":1}])["next"]["next"],"reproduce_and_patch")
    def test_missing_evidence(self):
        with self.assertRaises(ValueError):
            supervise([{"id":"a","stage":"MERGED","priority":1}])
    def test_blocked(self):
        self.assertEqual(supervise([{"id":"a","stage":"OPEN","priority":1,"blocked":"external"}])["status"],"BLOCKED")
    def test_complete(self):
        self.assertEqual(supervise([])["status"],"COMPLETE")
