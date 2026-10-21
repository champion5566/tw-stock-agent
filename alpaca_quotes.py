"""Optional Alpaca Basic IEX US stock quotes. Read-only market data.

Requires ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY as GitHub Actions secrets.
No brokerage trading endpoints or order submission.
IEX is only one exchange: volume and OHLC must not be called consolidated.
"""
import json
import os
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ENDPOINT = "https://data.alpaca.markets/v2/stocks/snapshots"


def fetch_iex_snapshots(symbols):
    key = os.getenv("ALPACA_API_KEY_ID")
    secret = os.getenv("ALPACA_API_SECRET_KEY")
    if not key or not secret:
        return {"status": "NOT_CONFIGURED", "reason": "Alpaca API keys absent"}
    symbols = sorted(set(symbols))
    url = ENDPOINT + "?" + urlencode({"symbols": ",".join(symbols), "feed": "iex"})
    req = Request(url, headers={"APCA-API-KEY-ID": key,
                                "APCA-API-SECRET-KEY": secret,
                                "Accept": "application/json"})
    with urlopen(req, timeout=18) as resp:
        payload = json.load(resp)
    result = {}
    now = datetime.now(timezone.utc)
    for symbol in symbols:
        snap = payload.get(symbol, {})
        trade = snap.get("latestTrade") or {}
        minute = snap.get("minuteBar") or {}
        daily = snap.get("dailyBar") or {}
        previous = snap.get("prevDailyBar") or {}
        raw_ts = trade.get("t")
        timestamp = None
        age_seconds = None
        if raw_ts:
            timestamp = datetime.fromisoformat(raw_ts.replace("Z", "+00:00"))
            age_seconds = round((now - timestamp).total_seconds(), 1)
        price = trade.get("p")
        if price is None:
            status = "NO_TRADE"
        elif age_seconds is None or age_seconds < -60 or age_seconds > 1200:
            status = "STALE"
        else:
            status = "PASS"
        result[symbol] = {
            "status": status, "ticker": symbol, "price": price,
            "trade_time_utc": raw_ts, "age_seconds": age_seconds,
            "source": "Alpaca Basic IEX-only (not consolidated SIP)",
            "market_coverage": "IEX_ONLY",
            "last_trade_size": trade.get("s"),
            "minute_bar": minute,
            "daily_bar_iex": daily,
            "previous_daily_bar_iex": previous,
            "note": "IEX-only OHLCV; do not interpret as US consolidated market volume or NBBO",
        }
    return {"status": "PASS", "quotes": result}
