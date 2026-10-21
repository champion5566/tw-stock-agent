"""Read-only TX night-session quote snapshot using the validated Shioaji SDK.
No orders, no CA activation, no secret values in output.
"""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

TW = ZoneInfo("Asia/Taipei")


def main():
    now = datetime.now(TW)
    slot = os.getenv("REPORT_SLOT", "evening")
    path = Path("out") / now.date().isoformat() / ("cross-" + slot + ".json")
    if not path.exists():
        raise SystemExit("Cross-market snapshot must exist before quote enrichment")
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    result = {
        "provider": "Shioaji", "instrument": "TXFR1",
        "checked_at_taipei": now.isoformat(),
        "status": "NOT_CONFIGURED",
        "is_live": False,
    }
    key = os.getenv("SHIOAJI_API_KEY")
    secret = os.getenv("SHIOAJI_SECRET_KEY")
    if key and secret:
        api = None
        ticks = []
        try:
            import shioaji as sj
            api = sj.Shioaji(simulation=False)
            api.login(api_key=key, secret_key=secret)
            contract = api.Contracts.Futures.TXF.TXFR1
            result["contract_code"] = str(contract.code)

            def on_tick(exchange, tick):
                try:
                    price = float(getattr(tick, "close"))
                    stamp = str(getattr(tick, "datetime", ""))
                    if price > 0 and stamp:
                        ticks.append({"price": price, "trade_time": stamp,
                                      "volume": str(getattr(tick, "volume", ""))})
                except (TypeError, ValueError):
                    pass

            api.quote.set_on_tick_fop_v1_callback(on_tick)
            api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.Tick,
                                version=sj.constant.QuoteVersion.v1)
            time.sleep(35)
            if ticks:
                last = ticks[-1]
                result.update(last)
                result["ticks_observed"] = len(ticks)
                try:
                    dt = datetime.fromisoformat(last["trade_time"])
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=TW)
                    age = (datetime.now(TW) - dt.astimezone(TW)).total_seconds() / 60
                    result["age_minutes"] = round(age, 2)
                    result["status"] = "PASS" if -2 <= age <= 10 else "STALE"
                    result["is_live"] = result["status"] == "PASS"
                except ValueError:
                    result["status"] = "UNVERIFIED_TIMESTAMP"
            else:
                result["status"] = "NO_TICKS_IN_WINDOW"
            try:
                api.quote.unsubscribe(contract, quote_type=sj.constant.QuoteType.Tick,
                                      version=sj.constant.QuoteVersion.v1)
            except Exception:
                pass
        except Exception as exc:
            result["status"] = "ERROR"
            result["error_type"] = type(exc).__name__
        finally:
            if api is not None:
                try:
                    api.logout()
                except Exception:
                    pass
    snapshot.setdefault("taifex", {})["shioaji_live_tx"] = result
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print("SHIOAJI_TX", result["status"], result.get("price"),
          result.get("trade_time"), "age_min", result.get("age_minutes"))


if __name__ == "__main__":
    main()
