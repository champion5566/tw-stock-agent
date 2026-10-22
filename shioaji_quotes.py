"""One bounded read-only SDK session: snapshots once, then event-driven ticks."""
import os
import time
from datetime import datetime

from quote_quality import TW, positive_price, quote_status, shioaji_snapshot_time


def tick_observation(tick, checked_at, *, source, units):
    # Indicative/simulated auction ticks are not executed trades.
    if getattr(tick, "simtrade", False):
        return None
    price = positive_price(getattr(tick, "close", None))
    try:
        stamp = datetime.fromisoformat(str(getattr(tick, "datetime", "")))
    except (TypeError, ValueError):
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=TW)
    if price is None:
        return None
    status = quote_status(price, stamp, checked_at)
    result = {"source": source, "price": price, "trade_time": stamp.isoformat(),
              "status": status, "is_live": status == "PASS", "data_kind": "tick",
              "units": {"price": units, "volume": "lots"},
              "volume": str(getattr(tick, "volume", ""))}
    for field in ("open", "high", "low"):
        result[field] = positive_price(getattr(tick, field, None))
    total_volume = getattr(tick, "total_volume", None)
    result["total_volume"] = int(total_volume) if total_volume is not None else None
    return result


def collect_quotes(stock_codes=(), wait_seconds=25, *, sdk=None, clock=None, wait=None, future_snapshot=False, stream=True):
    clock = clock or (lambda: datetime.now(TW))
    wait = wait or time.sleep
    result = {"provider": "Shioaji", "source": "Shioaji", "instrument": "TXFR1",
              "checked_at_taipei": clock().isoformat(),
              "status": "NOT_CONFIGURED", "is_live": False}
    key, secret = os.getenv("SHIOAJI_API_KEY"), os.getenv("SHIOAJI_SECRET_KEY")
    if not key or not secret:
        return result
    api, subscriptions = None, []
    stock_ticks, future_ticks = {}, []
    try:
        if sdk is None:
            import shioaji as sdk
        api = sdk.Shioaji(simulation=False)
        api.login(api_key=key, secret_key=secret)
        kwargs = {"quote_type": sdk.constant.QuoteType.Tick,
                  "version": sdk.constant.QuoteVersion.v1}

        def subscribe(contract):
            api.quote.subscribe(contract, **kwargs)
            subscriptions.append(contract)

        if stock_codes:
            snapshots = result["stock_snapshots"] = {}
            contracts = []
            for code in dict.fromkeys(stock_codes):
                try:
                    contracts.append(api.Contracts.Stocks[code])
                except Exception as exc:
                    snapshots[code] = {"source": "Shioaji_snapshot", "status": "ERROR",
                                       "error_type": type(exc).__name__, "is_live": False}
            try:
                for snap in api.snapshots(contracts) if contracts else []:
                    stamp = shioaji_snapshot_time(getattr(snap, "ts", None))
                    price = positive_price(getattr(snap, "close", None))
                    snapshots[str(snap.code)] = {
                        "source": "Shioaji_snapshot", "price": price,
                        "trade_time": stamp.isoformat() if stamp else None,
                        "status": quote_status(price, stamp, clock()), "is_live": False,
                        "data_kind": "snapshot", "units": {"price": "TWD/share", "volume": "lots"},
                        "open": positive_price(getattr(snap, "open", None)),
                        "high": positive_price(getattr(snap, "high", None)),
                        "low": positive_price(getattr(snap, "low", None)),
                        "total_volume": getattr(snap, "total_volume", None)}
            except Exception as exc:
                snapshots["error_type"] = type(exc).__name__

            def on_stock_tick(exchange, tick):
                try:
                    code = str(getattr(tick, "code", ""))
                    obs = tick_observation(tick, clock(), source="Shioaji_tick", units="TWD/share")
                    if code in stock_codes and obs is not None:
                        stock_ticks[code] = obs
                except (TypeError, ValueError, OverflowError):
                    pass

            try:
                api.quote.set_on_tick_stk_v1_callback(on_stock_tick)
                for contract in contracts:
                    try:
                        subscribe(contract)
                    except Exception as exc:
                        result.setdefault("stock_subscription_errors", {})[str(contract.code)] = type(exc).__name__
            except Exception as exc:
                result["stock_stream_error_type"] = type(exc).__name__

        def on_future_tick(exchange, tick):
            try:
                obs = tick_observation(tick, clock(), source="Shioaji", units="index_points")
                if obs is not None:
                    future_ticks.append(obs)
            except (TypeError, ValueError, OverflowError):
                pass

        try:
            contract = api.Contracts.Futures.TXF.TXFR1
            result["contract_code"] = str(contract.code)
            if future_snapshot:
                snaps = api.snapshots([contract])
                if snaps:
                    snap = snaps[-1]
                    stamp = shioaji_snapshot_time(getattr(snap, "ts", None))
                    price = positive_price(getattr(snap, "close", None))
                    result.update({"source":"Shioaji_futures_snapshot", "data_kind":"snapshot", "price":price,
                                   "trade_time":stamp.isoformat() if stamp else None,
                                   "status":quote_status(price, stamp, clock()), "is_live":False,
                                   "units":{"price":"index_points"},
                                   "note":"One request after session end; time/session must be validated by the report contract."})
            if stream:
                api.quote.set_on_tick_fop_v1_callback(on_future_tick)
                subscribe(contract)
        except Exception as exc:
            result.update({"status": "ERROR", "error_type": type(exc).__name__})
        if stream:
            wait(wait_seconds)
        if future_ticks:
            result.update(future_ticks[-1])
            result["ticks_observed"] = len(future_ticks)
            result["age_minutes"] = round((clock() - datetime.fromisoformat(result["trade_time"])).total_seconds()/60, 2)
        elif stream and result["status"] != "ERROR":
            result["status"] = "NO_TICKS_IN_WINDOW"
    except Exception as exc:
        result.update({"status": "ERROR", "error_type": type(exc).__name__, "is_live": False})
    finally:
        # Refresh freshness at selection time, including slow/no-tick windows.
        if stock_codes and api is not None:
            result["stock_ticks"] = stock_ticks
            selected = result["stock_quotes"] = {}
            for code in stock_codes:
                tick = stock_ticks.get(code)
                snapshot = result.get("stock_snapshots", {}).get(code)
                if tick:
                    tick["status"] = quote_status(tick["price"], datetime.fromisoformat(tick["trade_time"]), clock())
                    tick["is_live"] = tick["status"] == "PASS"
                selected[code] = dict(tick if tick and tick["status"] == "PASS" else snapshot or tick or {
                    "source": "Shioaji", "status": "MISSING", "is_live": False})
                if selected[code].get("trade_time") and selected[code].get("data_kind") == "snapshot":
                    selected[code]["status"] = quote_status(selected[code].get("price"),
                        datetime.fromisoformat(selected[code]["trade_time"]), clock())
        if api is not None:
            for contract in reversed(subscriptions):
                try:
                    api.quote.unsubscribe(contract, **kwargs)
                except Exception:
                    pass
            try:
                api.logout()
            except Exception:
                pass
    return result
