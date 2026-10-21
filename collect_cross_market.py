"""Cross-market *observations*; exchange session and source timestamps mandatory.

Reuse yfinance and the established TWSE/TAIFEX MCP. No scraping or
reconstructing missing futures ticks from prior settlement values.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import yfinance as yf
from alpaca_quotes import fetch_iex_snapshots

from collect_market import mcp, attempt, http_json

TW = ZoneInfo("Asia/Taipei")
ASSETS = {
    "us": {
        "indices": {"SP500":"^GSPC", "NASDAQ":"^IXIC", "SOX":"^SOX", "VIX":"^VIX"},
        "semiconductors": {"NVDA":"NVDA", "AMD":"AMD", "AVGO":"AVGO",
                            "MU":"MU", "TSM_ADR":"TSM"},
        # Holdings explicitly supplied by the user in two brokerage screenshots.
        # SPCX ticker identity must be verified against the current security master.
        "user_holdings": {
            "AMZN": "AMZN", "BRK.B": "BRK-B", "GOOG": "GOOG",
            "META": "META", "MU": "MU", "QCOM": "QCOM",
            "SPCX": "SPCX", "TLT": "TLT", "TSLA": "TSLA",
            "AVGO": "AVGO", "QQQ": "QQQ",
        },
    },
    "jp": {
        "indices": {"NIKKEI225":"^N225", "TOPIX_ETF_PROXY":"1306.T"},
        "semiconductors": {"ADVANTEST":"6857.T", "TOKYO_ELECTRON":"8035.T"},
    },
    "kr": {
        "indices": {"KOSPI":"^KS11", "KOSDAQ":"^KQ11"},
        "semiconductors": {"SAMSUNG":"005930.KS", "SK_HYNIX":"000660.KS"},
    },
}


def observe(ticker):
    obj = yf.Ticker(ticker)
    hist = obj.history(period="5d", interval="5m", auto_adjust=False,
                       prepost=True, raise_errors=True)
    if hist.empty:
        return {"status": "EMPTY", "ticker": ticker}
    row = hist.iloc[-1]
    ts = hist.index[-1]
    if ts.tzinfo is None:
        raise ValueError("Missing exchange timezone in last bar")
    close = float(row["Close"])
    volume = float(row["Volume"]) if row["Volume"] == row["Volume"] else None
    return {
        "status": "PASS",
        "ticker": ticker,
        "source": "yfinance/Yahoo Finance; research only, may be delayed",
        "price": close,
        "open": float(row["Open"]), "high": float(row["High"]),
        "low": float(row["Low"]), "volume_bar": volume,
        "interval": "5m", "latest_bar_at_exchange": ts.isoformat(),
        "latest_bar_at_taipei": ts.tz_convert("Asia/Taipei").isoformat(),
        "latest_bar_utc": ts.tz_convert("UTC").isoformat(),
        "is_formal_close": False,
        "note": "Last bar is NOT a confirmed regular-session close; inspect session before use.",
    }


def main():
    now = datetime.now(TW)
    slot = os.environ.get("REPORT_SLOT", "evening")
    out = {"schema_version":"1.0", "fetched_at_taipei":now.isoformat(),
           "date_taipei":now.date().isoformat(), "slot":slot,
           "assets":{}, "taifex":{},
           "limitations":["Yahoo is not an official realtime provider",
                          "Futures daily settlement is not a live night-session quote",
                          "Bar time is not necessarily official session close"]}
    # Free IEX quote overlay; retain Yahoo observation as historical/fallback.
    us_symbols = [ticker for group in ASSETS["us"].values()
                  for ticker in group.values() if not ticker.startswith("^")]
    iex = attempt(lambda: fetch_iex_snapshots(us_symbols))
    iex_payload = iex.get("data", {}) if iex.get("status") == "PASS" else {}
    iex_quotes = iex_payload.get("quotes", {}) if iex_payload.get("status") == "PASS" else {}
    out["us_iex_status"] = {"status": iex_payload.get("status", iex.get("status")),
                             "reason": iex_payload.get("reason", iex.get("error")),
                             "feed": "IEX_ONLY"}
    for area, sectors in ASSETS.items():
        out["assets"][area] = {}
        for sector, tickers in sectors.items():
            for name, ticker in tickers.items():
                obs = attempt(lambda t=ticker: observe(t))
                if obs["status"] == "PASS":
                    obs = obs["data"]
                    age_min = (now.astimezone(timezone.utc)
                               - datetime.fromisoformat(obs["latest_bar_utc"])).total_seconds()/60
                    obs["age_minutes"] = round(age_min, 1)
                    if age_min < -10 or age_min > 90:
                        obs["status"] = "HISTORICAL_BAR"
                if area == "us" and ticker in iex_quotes:
                    iex_quote = iex_quotes[ticker]
                    obs["alpaca_iex"] = iex_quote
                    if iex_quote["status"] == "PASS":
                        # Do not mix IEX daily bar OHLCV with Yahoo consolidated bars.
                        obs["fallback_yahoo"] = dict(obs)
                        obs["price"] = iex_quote["price"]
                        obs["status"] = "PASS"
                        obs["source"] = iex_quote["source"]
                        obs["latest_bar_utc"] = iex_quote["trade_time_utc"]
                        obs["age_minutes"] = round(iex_quote["age_seconds"] / 60, 2)
                        obs["market_coverage"] = "IEX_ONLY"
                out["assets"][area][name] = obs
                print("QUOTE", area, name, ticker, obs["status"],
                      obs.get("latest_bar_at_taipei"), flush=True)

    official = attempt(lambda: http_json("https://openapi.taifex.com.tw/v1/DailyMarketReportFut"))
    if official["status"] == "PASS":
        rows = official["data"]
        if not isinstance(rows, list):
            official = {"status":"FAIL", "error":"TAIFEX daily report response is not a list"}
        else:
            tx = [x for x in rows if str(x.get("Contract","")).strip() == "TX"]
            official["data"] = tx
            official["total_api_rows"] = len(rows)
            official["tx_rows"] = len(tx)
            official["sessions"] = sorted(set(str(x.get("TradingSession")) for x in tx))
            if not tx: official["status"] = "EMPTY"
    out["taifex"]["official_daily_market_futures"] = official
    print("TAIFEX official_daily_market_futures", official["status"], official.get("sessions"), official.get("tx_rows"), flush=True)

    init = attempt(lambda: mcp("initialize", {"protocolVersion":"2025-06-18",
                    "capabilities":{}, "clientInfo":{"name":"tw-stock-agent-cross-market",
                    "version":"1.0"}}, 1))
    out["taifex"]["mcp_init"] = {"status":init["status"],
                                  "error":init.get("error")}
    if init["status"] == "PASS":
        for tool, args in (
            ("snapshot.futures", {"contract":"TX"}),
            ("snapshot.market", {"scope":"futures"}),
        ):
            out["taifex"][tool] = attempt(
                lambda t=tool, a=args: mcp("tools/call",
                                          {"name":t, "arguments":a}, 2))
            print("TAIFEX", tool, out["taifex"][tool]["status"], flush=True)
    path = Path("out") / now.date().isoformat() / ("cross-" + slot + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str)+"\n",
                    encoding="utf-8")
    print("OUTPUT_PATH", path, "BYTES", path.stat().st_size)


if __name__ == "__main__":
    main()
