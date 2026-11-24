import unittest

from market_context import official_credit_rows


class OfficialStockCreditTest(unittest.TestCase):
    def test_preserves_exact_date_and_margin_short_columns(self):
        response = {
            "date": "20261124",
            "tables": [{
                "fields": ["股票代號", "股票名稱", "前日餘額", "今日餘額", "前日餘額", "今日餘額"],
                "data": [
                    ["00631L", "ETF", "1,024", "1,120", "17", "15"],
                    ["0050", "ETF", "--", "10", "8", "8"],
                ],
            }],
        }
        self.assertEqual(official_credit_rows(response, "2026-11-24"), {
            "00631L": {"date": "2026-11-24", "MarginPurchaseYesterdayBalance": 1024,
                       "MarginPurchaseTodayBalance": 1120, "ShortSaleYesterdayBalance": 17,
                       "ShortSaleTodayBalance": 15},
        })
        self.assertEqual(official_credit_rows(response, "2026-11-25"), {})
