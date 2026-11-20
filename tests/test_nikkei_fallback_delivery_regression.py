"""Reproduce the 08:12 Nikkei stale-primary failure without network access."""
import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from regional_quotes import select_regional

TW = ZoneInfo("Asia/Taipei")


def quote(source, minute, status="PASS"):
    return {
        "source": source,
        "status": status,
        "price": 59000.0,
        "trade_time": f"2026-11-20T08:{minute:02d}:00+08:00",
    }


class NikkeiDeliveryFallbackTests(unittest.TestCase):
    def setUp(self):
        self.checked = datetime(2026, 11, 20, 8, 28, tzinfo=TW)
        self.primary = quote("Yahoo Japan regional page", 12, "STALE")

    def test_fresh_independent_fallback_selected(self):
        selected = select_regional(self.primary, quote("Naver world index quote", 26), self.checked)
        self.assertEqual(selected["source"], "Naver world index quote")
        self.assertTrue(selected["regional_selection"]["selected_qualified_through_delivery"])
        self.assertTrue(selected["regional_selection"]["fallback_qualified_through_delivery"])

    def test_fallback_pass_at_fetch_but_expired_at_delivery(self):
        selected = select_regional(self.primary, quote("Naver world index quote", 23), self.checked)
        self.assertFalse(selected["regional_selection"]["selected_qualified_through_delivery"])
        self.assertFalse(selected["regional_selection"]["fallback_qualified_through_delivery"])
        self.assertEqual(selected["regional_selection"]["fallback_rejection_reason"], "NOT_FRESH_THROUGH_DELIVERY")

    def test_missing_fallback_timestamp_cannot_qualify(self):
        fallback = {"source": "Yahoo/global", "status": "PASS", "price": 59000.0}
        selected = select_regional(self.primary, fallback, self.checked)
        self.assertFalse(selected["regional_selection"]["fallback_qualified_through_delivery"])
        self.assertEqual(selected["regional_selection"]["fallback_rejection_reason"], "NO_VERIFIABLE_TIMESTAMP")


if __name__ == "__main__":
    unittest.main()
