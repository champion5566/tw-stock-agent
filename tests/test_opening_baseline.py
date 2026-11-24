import unittest
from opening_baseline import forecast, settle

class OpeningBaselineTests(unittest.TestCase):
    def test_valid(self):
        b = {"target_session_date":"2026-11-23","market_context":{"TAIEX":{"status":"PASS","source_date":"2026-11-23","close":36811.89}}}
        self.assertEqual(forecast(b)["models"]["V0-CARRY"]["center"],36811.89)
        self.assertFalse(forecast(b)["formal_sample_eligible"])
        b["market_context"]["TAIEX"]["source_date"]="2026-11-20"
        self.assertEqual(forecast(b)["models"],{})
    def test_missing(self):
        self.assertEqual(forecast({})["models"],{})
    def test_settle(self):
        self.assertEqual(settle(100,110,100),{"signed_error":-10,"absolute_error":10,"direction_match":False})
