import unittest
from opening_baseline import forecast
class BlendTest(unittest.TestCase):
    def test_blend(self):
        b={"target_session_date":"2026-11-23","market_context":{"TAIEX":{"status":"PASS","source_date":"2026-11-23","close":100}},"us_regular_close":{"SOX":{"change_status":"PASS","change_pct":10}},"cross_market":{"jp":{"TOPIX":{"change_pct":2}},"kr":{"KOSPI":{"change_pct":4}}},"readiness":{"sections":{"us_regular_close":{"items":{"SOX":"PASS"}},"asia_open":{"items":{"jp/TOPIX":"STALE","kr/KOSPI":"PASS"}}}}}
        m=forecast(b)["models"]["V2-CROSS-BLEND"]
        self.assertAlmostEqual(m["center"],107.6)
        self.assertNotIn("TOPIX",m["inputs"])
        self.assertAlmostEqual(sum(m["weights"].values()),1)
