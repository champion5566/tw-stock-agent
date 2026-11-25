"""Evaluate prospective, non-overlapping long-only opening-auction simulations."""
from datetime import date, datetime, time
from math import isfinite
from zoneinfo import ZoneInfo

TW = ZoneInfo("Asia/Taipei")


def positive(value):
    return type(value) in (int, float) and isfinite(value) and value > 0


def opening(bar):
    # A daily opening print can support a conservative auction proxy only.
    # One-price sessions and missing/zero-volume bars are ambiguous.
    if not bar or not bar.get("ref") or not all(positive(bar.get(k)) for k in
                                               ("open", "high", "low", "volume")):
        return None
    if not bar["low"] <= bar["open"] <= bar["high"] or bar["high"] == bar["low"]:
        return None
    return bar["open"]


def evaluate(action, published, quote, as_of):
    result = {"id": action.get("id"), "entry_day": action.get("entry_day"),
              "exit_day": action.get("exit_day"), "status": "INVALID_RULE"}
    try:
        entry = date.fromisoformat(action["entry_day"])
        exit_day = date.fromisoformat(action["exit_day"])
        if type(action.get("version")) is not str or not action["version"]:
            return result
        if published.tzinfo is None:
            return result
        start = datetime.fromisoformat(action["earliest_at"])
        if start.tzinfo is None:
            return result
        opening_time = datetime.combine(entry, time(9), TW)
        symbol = action["symbol"]
        if (not action["id"] or action["rule"] != "PREPLACED_BUY_LIMIT_OPEN_TO_OPEN"
                or not published <= start <= opening_time or published >= opening_time
                or exit_day <= entry or symbol not in ("0050", "006208", "00631L", "2330", "3707", "5483")
                or not positive(action["limit"])
                or action["invalidation"] != "CANCEL_IF_ENTRY_AUCTION_MISSED"
                or action["benchmark"] != "0050"):
            return result
        costs = action["costs"]
        if (not costs.get("version") or costs.get("trade_method") != "cash_swing"
                or costs.get("instrument_type") != ("stock" if symbol in ("2330", "3707", "5483") else "etf")
                or any(type(costs[k]) not in (int, float) or not isfinite(costs[k]) or not 0 <= costs[k] < 10000
                       for k in ("fee_bps_per_side", "sell_tax_bps", "slippage_bps_per_side"))):
            return result
        buy_bar = quote(symbol, entry.isoformat())
        buy = opening(buy_bar)
        if entry.isoformat() > as_of:
            return {**result, "status": "PENDING"}
        if buy is None:
            return {**result, "status": "NO_EXECUTION_EVIDENCE"}
        result["entry_ref"] = buy_bar["ref"]
        if buy >= action["limit"]:
            return {**result, "status": "NOT_TRIGGERED" if buy > action["limit"] else "FILL_UNCERTAIN_AT_LIMIT"}
        if exit_day.isoformat() > as_of:
            return {**result, "status": "PENDING_EXIT"}
        sell_bar = quote(symbol, exit_day.isoformat())
        sell = opening(sell_bar)
        benchmark_buy = opening(quote(action["benchmark"], entry.isoformat()))
        benchmark_sell = opening(quote(action["benchmark"], exit_day.isoformat()))
        if None in (sell, benchmark_buy, benchmark_sell):
            return {**result, "status": "NO_EXIT_OR_BENCHMARK_EVIDENCE"}
        fee = costs["fee_bps_per_side"] / 10000
        tax = costs["sell_tax_bps"] / 10000
        slip = costs["slippage_bps_per_side"] / 10000
        # A worse modeled fill that violates the preplaced limit is unscorable.
        if buy * (1 + slip) > action["limit"]:
            return {**result, "status": "FILL_UNCERTAIN_AFTER_SLIPPAGE"}
        if fee + tax >= 1:
            return result
        net = sell * (1 - slip) * (1 - fee - tax) / (buy * (1 + slip) * (1 + fee)) - 1
        return {**result, "status": "SIMULATED", "entry_open": buy, "exit_open": sell,
                "exit_ref": sell_bar["ref"], "costs": costs,
                "net_return": net, "benchmark_gross_return": benchmark_sell / benchmark_buy - 1}
    except (KeyError, TypeError, ValueError):
        return result


def summarize(rows):
    equity = peak = 1.0
    benchmark = 1.0
    drawdown = 0.0
    end = ""
    n = 0
    for row in sorted(rows, key=lambda item: (item.get("entry_day") or "", item.get("id") or "")):
        if row["status"] != "SIMULATED":
            continue
        if row["entry_day"] <= end:
            row["status"] = "OVERLAPPING_EXCLUDED"
            continue
        end = row["exit_day"]
        equity *= 1 + row["net_return"]
        benchmark *= 1 + row["benchmark_gross_return"]
        peak = max(peak, equity)
        drawdown = max(drawdown, 1 - equity / peak)
        n += 1
    return {"n": n, "net_return": equity - 1 if n else None,
            "benchmark_gross_return": benchmark - 1 if n else None,
            "max_closed_trade_drawdown": drawdown if n else None}
