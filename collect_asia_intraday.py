"""Read-only Taiwan/Japan/Korea intraday observations with source timestamps.
Not a streaming feed; scheduled GitHub Actions can start late.
"""
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import yfinance as yf
from snapshot_io import write_snapshot
from quote_quality import positive_price
from collect_intraday import mis

TW = ZoneInfo("Asia/Taipei")
SYMBOLS = {
    "JP": {"NIKKEI225": "^N225", "TOPIX": "^TOPX", "ADVANTEST": "6857.T", "TOKYO_ELECTRON": "8035.T"},
    "KR": {"KOSPI": "^KS11", "KOSDAQ": "^KQ11", "SAMSUNG": "005930.KS", "SK_HYNIX": "000660.KS"},
}
MAX_AGE_MINUTES = 10

def yahoo_quote(ticker, now):
    try:
        bars = yf.Ticker(ticker).history(period="1d", interval="1m", auto_adjust=False, prepost=False)
        if bars.empty:
            return {"status": "MISSING", "ticker": ticker}
        stamp = bars.index[-1]
        if stamp.tzinfo is None:
            return {"status": "NO_TIMESTAMP", "ticker": ticker}
        ts = stamp.to_pydatetime().astimezone(TW)
        price = positive_price(bars.iloc[-1]["Close"])
        age = (now - ts).total_seconds() / 60
        status = "PASS" if price and 0 <= age <= MAX_AGE_MINUTES and ts.date() == now.date() else (
            "FUTURE_TIMESTAMP" if age < -2 else "STALE" if price else "NO_LAST_TRADE")
        return {"ticker": ticker, "source": "Yahoo/yfinance 1m bar (potentially delayed)",
                "price": price, "source_time_taipei": ts.isoformat(),
                "age_minutes_at_collection": round(age, 2), "status": status,
                "is_live": False, "data_kind": "minute_bar", "delay_not_guaranteed": True}
    except Exception as exc:
        return {"ticker": ticker, "status": "ERROR", "error_type": type(exc).__name__}

def main():
    now = datetime.now(TW)
    output = {"schema_version": "asia-intraday-v1", "collected_at_taipei": now.isoformat(),
              "max_age_minutes": MAX_AGE_MINUTES, "is_streaming": False,
              "markets": {"TW": {}, "JP": {}, "KR": {}}, "errors": []}
    try:
        observations = mis()
        for name in ("TAIEX", "TPEX"):
            quote = observations.get(name, {"status": "MISSING"})
            output["markets"]["TW"][name] = quote
    except Exception as exc:
        output["errors"].append({"provider": "TWSE_MIS", "error_type": type(exc).__name__})
        for name in ("TAIEX", "TPEX"):
            output["markets"]["TW"][name] = {"status": "MISSING"}
    for market, tickers in SYMBOLS.items():
        for name, ticker in tickers.items():
            output["markets"][market][name] = yahoo_quote(ticker, datetime.now(TW))
    output["completed_at_taipei"] = datetime.now(TW).isoformat()
    output["status"] = "PASS" if all(
        output["markets"][market].get(key, {}).get("status") == "PASS"
        for market, key in (("TW", "TAIEX"), ("JP", "NIKKEI225"), ("JP", "TOPIX"), ("KR", "KOSPI"))
    ) else "PARTIAL"
    path = write_snapshot(output, now.date().isoformat(), "asia-intraday")
    print(json.dumps({"path": str(path), "status": output["status"],
                      "markets": {m: {k: v.get("status") for k,v in q.items()} for m,q in output["markets"].items()}}, ensure_ascii=False))

if __name__ == "__main__":
    main()
