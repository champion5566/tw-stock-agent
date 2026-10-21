import unittest
from datetime import datetime, timezone

from probe_ieobserve_telegram import parse_page, collect


class FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


class FakeSession:
    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append(url)
        return FakeResponse(self.pages[len(self.calls) - 1])


def fixture(items):
    return '<div class="tgme_widget_message_wrap">' + ''.join(
        '<div class="tgme_widget_message" data-post="IEObserve/%d">'
        '<div class="tgme_widget_message_text">%s</div>'
        '<time datetime="%s"></time></div>' % (ident, body, dt)
        for ident, body, dt in items
    ) + '</div>'


class TelegramProbeTests(unittest.TestCase):
    def test_extract_id_timestamp_link_text(self):
        html = fixture([(3001, "SpaceX 測試", "2026-10-21T10:00:00+00:00")])
        result = parse_page(html)
        self.assertEqual(result[0]["message_id"], 3001)
        self.assertEqual(result[0]["url"], "https://t.me/IEObserve/3001")
        self.assertEqual(result[0]["published_at_taipei"], "2026-10-21T18:00:00+08:00")

    def test_paginate_until_older_than_48h(self):
        now = datetime(2026, 10, 22, 0, tzinfo=timezone.utc)
        session = FakeSession([
            fixture([(3003, "SpaceX", "2026-10-21T23:00:00+00:00"),
                     (3002, "Netflix", "2026-10-21T20:00:00+00:00")]),
            fixture([(3001, "old", "2026-10-18T20:00:00+00:00")]),
        ])
        result = collect(now, 48, session, 5)
        self.assertEqual(result["status"], "PASS_WITH_LIMITATIONS")
        self.assertEqual(result["messages_in_window"], 2)
        self.assertIn("before=3002", session.calls[1])
        self.assertEqual(len(result["keyword_matches_in_window"]["Netflix"]), 1)

    def test_stale_fails_closed(self):
        now = datetime(2026, 10, 22, 0, tzinfo=timezone.utc)
        session = FakeSession([fixture([(2000, "old", "2025-09-01T00:00:00+00:00")])])
        result = collect(now, 48, session, 3)
        self.assertEqual(result["status"], "STALE")
        self.assertFalse(result["completeness_guaranteed"])


if __name__ == "__main__":
    unittest.main()
