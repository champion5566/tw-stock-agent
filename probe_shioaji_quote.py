"""Read-only Shioaji futures quote probe. Never places orders or activates CA."""
import json, os, time
from datetime import datetime, timezone
from pathlib import Path

result = {"status": "UNKNOWN", "provider": "Shioaji", "contract": "TXFR1", "quotes": []}
key = os.environ.get("SHIOAJI_API_KEY")
secret = os.environ.get("SHIOAJI_SECRET_KEY")
if not key or not secret:
    result["status"] = "NOT_CONFIGURED"
else:
    api = None
    try:
        import shioaji as sj
        result["stage"] = "create_client"
        api = sj.Shioaji(simulation=False)
        result["stage"] = "login"
        api.login(api_key=key, secret_key=secret)
        result["status"] = "LOGGED_IN"
        result["stage"] = "resolve_contract"
        contract = api.Contracts.Futures.TXF.TXFR1
        result["contract_code"] = str(contract.code)
        def on_tick(exchange, tick):
            if len(result["quotes"]) < 3:
                result["quotes"].append({
                    "price": str(getattr(tick, "close", "")),
                    "datetime": str(getattr(tick, "datetime", "")),
                    "volume": str(getattr(tick, "volume", "")),
                })
        result["stage"] = "set_callback"
        api.quote.set_on_tick_fop_v1_callback(on_tick)
        result["stage"] = "subscribe"
        api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.Tick, version=sj.constant.QuoteVersion.v1)
        result["status"] = "SUBSCRIBED_WAITING_FOR_TICKS"
        time.sleep(35)
        result["status"] = "RECEIVED_TICKS" if result["quotes"] else "NO_TICKS_IN_WINDOW"
        api.quote.unsubscribe(contract, quote_type=sj.constant.QuoteType.Tick, version=sj.constant.QuoteVersion.v1)
    except Exception as exc:
        result["status"] = "ERROR"
        result["error_type"] = type(exc).__name__
        # Do not print exception text; SDK errors can contain sensitive request context.
    finally:
        if api is not None:
            try: api.logout()
            except Exception: pass
out = Path("out/shioaji-quote-probe.json")
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
print("SHIOAJI_RESULT", json.dumps(result, ensure_ascii=False))
