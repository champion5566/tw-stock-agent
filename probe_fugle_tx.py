"""Official Fugle TX quote opt-in; no credentials stored in source."""
import json
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

TW = ZoneInfo("Asia/Taipei")

def run():
    now = datetime.now(TW)
    result = {"provider": "Fugle official futopt REST SDK",
              "instrument": "TXF1!", "requested_session": "afterhours",
              "checked_at_taipei": now.isoformat(), "status": "NOT_CONFIGURED"}
    key = os.getenv("FUGLE_API_KEY")
    if key:
        try:
            from fugle_marketdata import RestClient
            quote = RestClient(api_key=key).futopt.intraday.quote(
                symbol="TXF1!", session="afterhours")
            result["raw_quote"] = quote
            result["status"] = "RECEIVED_UNVERIFIED"
            if isinstance(quote, dict):
                result["contract"] = quote.get("symbol")
                result["price"] = quote.get("lastPrice")
                result["quote_date"] = quote.get("date")
                stamp = quote.get("lastUpdated")
                if stamp is not None:
                    instant = datetime.fromtimestamp(int(stamp)/1000000,
                                                     timezone.utc).astimezone(TW)
                    age = (now - instant).total_seconds()/60
                    result["trade_time_taipei"] = instant.isoformat()
                    result["age_minutes"] = round(age, 1)
                    result["status"] = "PASS" if -2 <= age <= 10 and quote.get("lastPrice") is not None else "STALE"
        except Exception as exc:
            result["status"] = "FAIL"
            result["error"] = type(exc).__name__ + ": " + str(exc)[:250]
    else:
        result["reason"] = "Missing FUGLE_API_KEY; no request sent"
    path = Path("out")/now.date().isoformat()/"fugle-tx-probe.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str)+"\n")
    print("FUGLE_TX",result["status"],result.get("trade_time_taipei"))
    print("OUTPUT_PATH",path)

if __name__ == "__main__":
    run()
