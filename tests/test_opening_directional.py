import unittest
from opening_baseline import forecast

class DirectionalTest(unittest.TestCase):
    def test_proxy(self):
        b = {"target_session_date":"2026-11-23","market_context":{"TAIEX":{"status":"PASS","source_date":"2026-11-23","close":36811.89}},"futures":{"TXFR1":{"price":39829,"status":"COMPLETED_NIGHT_LAST_OBSERVATION","is_live":False}},"readiness":{"sections":{"tx_completed_night":{"status":"PASS"}}}}
        self.assertEqual(forecast(b)["models"]["V1-TX-ZERO-BASIS"]["center"],39829)
        b["readiness"]["sections"]["tx_completed_night"]["status"]="STALE"
        self.assertNotIn("V1-TX-ZERO-BASIS",forecast(b)["models"])
