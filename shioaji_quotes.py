"""One read-only SDK session for stocks and TX ticks; no trading operations."""
import os
import time
from datetime import datetime

from quote_quality import TW, positive_price, quote_status, shioaji_snapshot_time


def collect_quotes(stock_codes=(), wait_seconds=25, *, sdk=None, clock=None, wait=None):
    clock = clock or (lambda: datetime.now(TW))
    wait = wait or time.sleep
    result = {"provider": "Shioaji", "source": "Shioaji", "instrument": "TXFR1",
              "checked_at_taipei": clock().isoformat(),
              "status": "NOT_CONFIGURED", "is_live": False}
    key, secret = os.getenv("SHIOAJI_API_KEY"), os.getenv("SHIOAJI_SECRET_KEY")
    if not key or not secret:
        return result
    api, contract, subscribed = None, None, False
    try:
        if sdk is None:
            import shioaji as sdk
        api = sdk.Shioaji(simulation=False)
        api.login(api_key=key, secret_key=secret)
        if stock_codes:
            result["stock_snapshots"] = {}
            try:
                contracts = [api.Contracts.Stocks[code] for code in stock_codes]
                for snap in api.snapshots(contracts):
                    stamp = shioaji_snapshot_time(getattr(snap, "ts", None))
                    price = positive_price(getattr(snap, "close", None))
                    status = quote_status(price, stamp, clock())
                    result["stock_snapshots"][str(snap.code)] = {
                        "source": "Shioaji_snapshot", "price": price,
                        "trade_time": stamp.isoformat() if stamp else None,
                        "status": status, "is_live": status == "PASS",
                        "data_kind": "snapshot", "units": {"price": "TWD/share"}}
            except Exception as exc:
                result["stock_snapshots"]["error_type"] = type(exc).__name__
        contract = api.Contracts.Futures.TXF.TXFR1
        result["contract_code"] = str(contract.code)
        ticks = []

        def on_tick(exchange, tick):
            try:
                price = positive_price(getattr(tick, "close", None))
                stamp = datetime.fromisoformat(str(getattr(tick, "datetime", "")))
                if stamp.tzinfo is None:
                    stamp = stamp.replace(tzinfo=TW)
                if price is not None:
                    ticks.append((price, stamp, str(getattr(tick, "volume", ""))))
            except (TypeError, ValueError):
                pass

        api.quote.set_on_tick_fop_v1_callback(on_tick)
        api.quote.subscribe(contract, quote_type=sdk.constant.QuoteType.Tick,
                            version=sdk.constant.QuoteVersion.v1)
        subscribed = True
        wait(wait_seconds)
        result["status"] = "NO_TICKS_IN_WINDOW"
        if ticks:
            price, stamp, volume = ticks[-1]
            status = quote_status(price, stamp, clock())
            result.update({"price": price, "trade_time": stamp.isoformat(),
                           "volume": volume, "ticks_observed": len(ticks),
                           "status": status, "is_live": status == "PASS",
                           "age_minutes": round((clock() - stamp).total_seconds() / 60, 2),
                           "data_kind": "tick", "units": {"price": "index_points"}})
    except Exception as exc:
        result.update({"status": "ERROR", "error_type": type(exc).__name__, "is_live": False})
    finally:
        if subscribed:
            try:
                api.quote.unsubscribe(contract, quote_type=sdk.constant.QuoteType.Tick,
                                      version=sdk.constant.QuoteVersion.v1)
            except Exception:
                pass
        if api is not None:
            try:
                api.logout()
            except Exception:
                pass
    return result
