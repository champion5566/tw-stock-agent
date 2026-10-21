#!/usr/bin/env python3
"""Read public Telegram channel pages without credentials; fail closed on stale data.

Probe only: this is NOT a guarantee that the public HTML contains all messages.
Outputs metadata and short excerpts, not a full-text copyrighted archive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

CHANNEL = "IEObserve"
BASE = f"https://t.me/s/{CHANNEL}"
TAIPEI = timezone(timedelta(hours=8))
USER_AGENT = "Mozilla/5.0 (compatible; IEObservePublicPageProbe/1.0)"
MAX_PAGES = 15


def parse_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    records = []
    for box in soup.select(".tgme_widget_message[data-post]"):
        post = box.get("data-post", "")
        match = re.fullmatch(r"(?i:ieobserve)/(\d+)", post)
        if not match:
            continue
        date_el = box.select_one("time[datetime]")
        if date_el is None:
            continue
        try:
            published = datetime.fromisoformat(date_el["datetime"].replace("Z", "+00:00"))
            if published.tzinfo is None:
                continue
            published = published.astimezone(timezone.utc)
        except (ValueError, KeyError):
            continue
        text_el = box.select_one(".tgme_widget_message_text")
        body = text_el.get_text("\n", strip=True) if text_el else ""
        message_id = int(match.group(1))
        records.append({
            "message_id": message_id,
            "published_at_utc": published.isoformat(),
            "published_at_taipei": published.astimezone(TAIPEI).isoformat(),
            "url": f"https://t.me/{CHANNEL}/{message_id}",
            "excerpt": body[:240],
            "text_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest() if body else None,
            "has_text": bool(body),
        })
    return sorted({r["message_id"]: r for r in records}.values(), key=lambda r: r["message_id"], reverse=True)


def fetch_page(session: requests.Session, before: int | None) -> list[dict]:
    url = BASE if before is None else BASE + "?" + urlencode({"before": before})
    response = session.get(url, timeout=25, headers={"User-Agent": USER_AGENT, "Cache-Control": "no-cache"})
    response.raise_for_status()
    if "tgme_widget_message" not in response.text:
        raise RuntimeError("Telegram returned no recognizable public message markup")
    return parse_page(response.text)


def collect(now: datetime, hours: int, session: requests.Session, max_pages: int) -> dict:
    cutoff = now - timedelta(hours=hours)
    seen = {}
    pages = 0
    before = None
    last_oldest = None
    errors = []
    stopped_by_cutoff = False
    while pages < max_pages:
        try:
            batch = fetch_page(session, before)
        except Exception as exc:
            errors.append(f"{type(exc).__name__}: {exc}")
            break
        pages += 1
        if not batch:
            errors.append("EMPTY_PAGE: no valid dated messages")
            break
        for rec in batch:
            seen[rec["message_id"]] = rec
        oldest = min(batch, key=lambda rec: rec["message_id"])
        oldest_time = datetime.fromisoformat(oldest["published_at_utc"])
        if oldest_time < cutoff:
            stopped_by_cutoff = True
            break
        if last_oldest is not None and oldest["message_id"] >= last_oldest:
            errors.append("PAGINATION_STALLED: message ID did not decrease")
            break
        last_oldest = oldest["message_id"]
        before = oldest["message_id"]
        time.sleep(0.4)
    records = sorted(seen.values(), key=lambda r: r["message_id"], reverse=True)
    latest = records[0] if records else None
    latest_time = datetime.fromisoformat(latest["published_at_utc"]) if latest else None
    window = [r for r in records if cutoff <= datetime.fromisoformat(r["published_at_utc"]) <= now]
    keywords = {
        "SPCX_or_SpaceX": ["spcx", "spacex"],
        "Netflix": ["netflix", "網飛", "奈飛"],
    }
    keyword_matches = {name: [r["url"] for r in window if any(term in r["excerpt"].lower() for term in terms)]
                       for name, terms in keywords.items()}
    # A fresh latest message does not establish completeness, but stale latest definitively fails.
    freshness = latest_time is not None and latest_time >= cutoff
    if not records:
        status = "FAIL"
    elif not freshness:
        status = "STALE"
    elif errors or not stopped_by_cutoff:
        status = "PARTIAL"
    else:
        status = "PASS_WITH_LIMITATIONS"
    return {
        "channel": CHANNEL,
        "source": BASE,
        "checked_at_utc": now.isoformat(),
        "window_start_utc": cutoff.isoformat(),
        "status": status,
        "completeness_guaranteed": False,
        "note": "Public Telegram HTML may omit messages. PASS_WITH_LIMITATIONS means a fresh window was paginated past its cutoff, not guaranteed X/Telegram parity.",
        "latest_message_id": latest["message_id"] if latest else None,
        "latest_message_at_taipei": latest["published_at_taipei"] if latest else None,
        "pages_read": pages,
        "messages_seen": len(records),
        "messages_in_window": len(window),
        "reached_before_window": stopped_by_cutoff,
        "keyword_matches_in_window": keyword_matches,
        "errors": errors,
        "messages": window,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=48)
    parser.add_argument("--max-pages", type=int, default=MAX_PAGES)
    parser.add_argument("--out", default="out/kol/ieobserve-telegram-probe.json")
    args = parser.parse_args()
    if not (1 <= args.hours <= 168 and 1 <= args.max_pages <= 30):
        parser.error("hours must be 1..168 and max-pages 1..30")
    now = datetime.now(timezone.utc)
    with requests.Session() as session:
        result = collect(now, args.hours, session, args.max_pages)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "messages"}, ensure_ascii=False, indent=2))
    print(f"Output: {output}")
    return 0 if result["status"] == "PASS_WITH_LIMITATIONS" else 2


if __name__ == "__main__":
    sys.exit(main())
