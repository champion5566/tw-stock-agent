import unittest
from scripts.repair_session import session

class RepairSessionTest(unittest.TestCase):
    def test_modes_share_gate(self):
        q=[{"id":"x","stage":"OPEN","priority":1}]
        a=session(q,[],"interactive")
        b=session(q,[],"scheduled")
        self.assertEqual(a["next"],b["next"])
        self.assertFalse(a["stop_allowed"])
        self.assertFalse(b["stop_allowed"])
