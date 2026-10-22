"""Cross-market *observations*; exchange session and source timestamps mandatory.\n\nProvider fallback smoke test: FinMind daily -> Yahoo daily; Alpaca IEX -> Yahoo intraday.

Reuse yfinance and the established TWSE/TAIFEX MCP. No scraping or
reconstructing missing futures ticks from prior settlement values.
"""
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import yfinance as yf
from alpaca_quotes import fetch_iex_snapshots

from market_sources import mcp, attempt, http_json, finmind
from snapshot_io import write_snapshot
from quote_quality import select_observation

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
                        obs = select_observation(obs, iex_quote)
                if area == "us" and not ticker.startswith("^"):
                    # Auditable selection: missing IEX credentials or stale IEX
                    # leaves the Yahoo intraday bar in place.
                    obs["quote_selection"] = {
                        "selected_source": obs.get("source"),
                        "selected_status": obs.get("status"),
                        "bar_at_taipei": obs.get("latest_bar_at_taipei"),
                        "age_minutes": obs.get("age_minutes"),
                        "freshness": ("UNKNOWN" if obs.get("age_minutes") is None else
                                      "STALE" if obs["age_minutes"] > 30 else
                                      "DELAYED" if obs["age_minutes"] > 15 else "RECENT"),
                        "iex_status": (iex_quotes.get(ticker) or {}).get(
                            "status", out["us_iex_status"]["status"]),
                        "fallback_to_yahoo": obs.get("source", "").startswith(
                            "yfinance/"),
                        "note": "Yahoo 5m bar is not an exchange-certified realtime trade."
                    }
                out["assets"][area][name] = obs
                print("QUOTE", area, name, ticker, obs["status"],
                      obs.get("latest_bar_at_taipei"), flush=True)

    # US daily OHLCV: FinMind first, Yahoo daily history as fallback.
    # Keep each provider and its source date separate from intraday IEX trades.
    out["us_daily"] = {}
    symbols = sorted(set(t for group in ASSETS["us"].values()
                         for t in group.values() if not t.startswith("^")))
    start = (now.date() - timedelta(days=365)).isoformat()
    end = now.date().isoformat()
    for symbol in symbols:
        primary = attempt(lambda s=symbol: finmind("USStockPrice", s, start, end))
        rows = primary.get("data") if primary["status"] == "PASS" else None
        if isinstance(rows, list) and rows:
            rows.sort(key=lambda r: str(r.get("date", "")))
            out["us_daily"][symbol] = {
                "status": "PASS", "source": "FinMind USStockPrice",
                "source_date": rows[-1].get("date"), "row_count": len(rows),
                "history": rows, "latest": rows[-1],
                "note": "Daily OHLCV, not live; compare trade dates and adjustments."
            }
        else:
            # A provider error or missing ticker must not be represented as zero price.
            fallback = attempt(lambda s=symbol: yf.Ticker(s).history(
                period="1y", interval="1d", auto_adjust=False,
                raise_errors=True))
            if fallback["status"] == "PASS" and not fallback["data"].empty:
                df = fallback["data"]
                hist = [
                    {"date": idx.date().isoformat(),
                     "Open": float(row["Open"]), "High": float(row["High"]),
                     "Low": float(row["Low"]), "Close": float(row["Close"]),
                     "Volume": int(row["Volume"])}
                    for idx, row in df.iterrows()
                ]
                out["us_daily"][symbol] = {
                    "status": "FALLBACK", "source": "Yahoo/yfinance 1d",
                    "source_date": hist[-1]["date"], "row_count": len(hist),
                    "history": hist, "latest": hist[-1],
                    "finmind_status": primary["status"],
                    "finmind_error": primary.get("error"),
                    "note": "Yahoo fallback; verify splits and dividends before backtests."
                }
            else:
                out["us_daily"][symbol] = {
                    "status": "MISSING", "source": None,
                    "finmind_status": primary["status"],
                    "finmind_error": primary.get("error"),
                    "yahoo_error": fallback.get("error")
                }
        print("US_DAILY", symbol, out["us_daily"][symbol]["status"],
              out["us_daily"][symbol].get("source_date"), flush=True)
        time.sleep(0.15)

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
    path = write_snapshot(out, now.date().isoformat(), "cross-" + slot)
    print("OUTPUT_PATH", path, "BYTES", path.stat().st_size)


if __name__ == "__main__":
    main()
