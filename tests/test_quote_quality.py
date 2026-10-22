import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from quote_quality import positive_price, quote_status, shioaji_snapshot_time

TW = ZoneInfo("Asia/Taipei")

class QuoteQualityTests(unittest.TestCase):
    def test_invalid_prices(self):
        for raw in ("-", None, "nan", "inf", "-1", 0):
            self.assertIsNone(positive_price(raw))
        self.assertEqual(positive_price("2405"), 2405.0)

    def test_shioaji_epoch_wall_clock(self):
        # Recorded Shioaji ts displayed +8h under ordinary fromtimestamp(TW).
        intended = datetime(2026, 10, 22, 11, 3, 21, tzinfo=TW)
        wall_clock_encoded = datetime(2026, 10, 22, 11, 3, 21, tzinfo=timezone.utc).timestamp() * 1e9
        self.assertEqual(shioaji_snapshot_time(wall_clock_encoded), intended)

    def test_datetime_input(self):
        aware = datetime(2026, 10, 22, 11, 3, tzinfo=TW)
        self.assertEqual(shioaji_snapshot_time(aware), aware)
        self.assertEqual(shioaji_snapshot_time(aware.replace(tzinfo=None)), aware)

    def test_source_quality(self):
        checked = datetime(2026, 10, 22, 11, 5, tzinfo=TW)
        self.assertEqual(quote_status("-", checked, checked), "NO_LAST_TRADE")
        self.assertEqual(quote_status(100, None, checked), "NO_TIMESTAMP")
        self.assertEqual(quote_status(100, checked-timedelta(minutes=3), checked), "PASS")
        self.assertEqual(quote_status(100, checked-timedelta(minutes=11), checked), "STALE")
        self.assertEqual(quote_status(100, checked+timedelta(minutes=3), checked), "FUTURE_TIMESTAMP")
        self.assertEqual(quote_status(100, checked-timedelta(days=1), checked), "PRIOR_SESSION")

if __name__ == "__main__":
    unittest.main()
