#!/usr/bin/env python3
"""One-shot evidence audit for public IEObserve sources (no credentials or scraping bypass)."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

SOURCES = {
    "sotwe": "https://www.sotwe.com/ieobserve",
    "twstalker": "https://site.twstalker.com/IEObserve",
    "twstalker_alt": "https://twstalker.com/IEObserve",
    "x_official": "https://x.com/IEObserve",
    "vocus_official": "https://vocus.cc/user/%40ieobserve",
    "patreon_official": "https://www.patreon.com/ieo",
    "ieobserve_site": "https://ieobserve.com/",
    "telegram_official": "https://t.me/s/IEObserve",
}
NEEDLES = {
    "SpaceX_Q3": ["營收年增161", "spacex q3"],
    "Netflix_Q3": ["netflix q3", "廣告收入下修"],
    "Ken_Griffin_GPU": ["ken griffin", "gpu過剩"],
    "PHP_AI_Japan": ["php漏洞", "日本首相要轉發"],
}
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/129.0.0.0 Safari/537.36"


def inspect(session, name, url):
    item = {"name": name, "url": url}
    try:
        r = session.get(url, headers={"User-Agent": UA}, timeout=22, allow_redirects=True)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        visible = " ".join(soup.stripped_strings)
        lower = visible.lower().replace(" ", "")
        item.update({
            "http_status": r.status_code,
            "final_host": urlparse(r.url).hostname,
            "html_bytes": len(r.content),
            "visible_chars": len(visible),
            "title": soup.title.get_text(" ", strip=True)[:150] if soup.title else "",
            "challenge_detected": any(s in lower for s in ["justamoment", "checkingyourbrowser", "verifyyouarehuman", "attentionrequired"]),
            "matches": {key: any(term.replace(" ", "") in lower for term in terms) for key, terms in NEEDLES.items()},
            "outbound_post_links": sorted(set(re.findall(r"https?://(?:www\\.)?(?:x\\.com|twitter\\.com)/IEObserve/status/\\d+", r.text, flags=re.I)))[:10],
        })
    except Exception as exc:
        item["error"] = f"{type(exc).__name__}: {str(exc)[:220]}"
    return item


def main():
    with requests.Session() as session:
        results = [inspect(session, name, url) for name, url in SOURCES.items()]
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "results": results,
              "caveat": "Keyword matches in public HTML are NOT proof of full 48-hour coverage. No anti-bot bypass attempted."}
    path = Path("out/kol/ieobserve-source-audit.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
