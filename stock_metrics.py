"""Deterministic same-provider metrics; missing inputs never become zero."""
from math import isfinite


def number(value):
    try:
        parsed = float(value)
        return parsed if isfinite(parsed) else None
    except (TypeError, ValueError, OverflowError):
        return None


def rows_to(item, target):
    rows = item.get("history") or ([item["data"]] if item.get("data") else [])
    # Last duplicate wins, as in the existing historical preparation code.
    unique = {row["date"]:row for row in rows if isinstance(row, dict)
              and isinstance(row.get("date"), str) and target and row["date"] <= target}
    return [unique[day] for day in sorted(unique)]


def delta(row, buy, sell):
    a, b = number(row.get(buy)), number(row.get(sell))
    return a - b if a is not None and b is not None else None


def flows(row):
    foreign_investor = delta(row, "Foreign_Investor_buy", "Foreign_Investor_sell")
    foreign_dealer = delta(row, "Foreign_Dealer_Self_buy", "Foreign_Dealer_Self_sell")
    foreign = foreign_investor + foreign_dealer if None not in (foreign_investor, foreign_dealer) else None
    trust = delta(row, "Investment_Trust_buy", "Investment_Trust_sell")
    own = delta(row, "Dealer_self_buy", "Dealer_self_sell")
    hedge = delta(row, "Dealer_Hedging_buy", "Dealer_Hedging_sell")
    aggregate = delta(row, "Dealer_buy", "Dealer_sell")
    dealer = own + hedge if own is not None and hedge is not None else aggregate
    conflict = aggregate not in (None, 0) and dealer is not None and aggregate != dealer
    total = foreign + trust + dealer if None not in (foreign, trust, dealer) and not conflict else None
    return {"foreign_net_shares":foreign, "foreign_investor_net_shares":foreign_investor,
            "foreign_dealer_net_shares":foreign_dealer, "trust_net_shares":trust,
            "dealer_net_shares":dealer, "total_net_shares":total,
            "dealer_components_conflict":conflict}


def metrics(stock, target):
    price_rows = rows_to(stock.get("daily_ohlcv", {}), target)
    flow_rows = rows_to(stock.get("institutional", {}), target)
    credit_rows = rows_to(stock.get("margin", {}), target)
    current = price_rows[-1] if price_rows and price_rows[-1]["date"] == target else {}
    prior = price_rows[-2] if current and len(price_rows) > 1 else {}
    previous_close = number(prior.get("close"))
    volume = number(current.get("Trading_Volume"))
    result = {"source_date":current.get("date"), "source":"FinMind TaiwanStockPrice",
              "previous_close":previous_close, "volume_shares":volume,
              "turnover_twd":number(current.get("Trading_money")),
              "amplitude_pct":None, "volume_ratio_5d":None, "volume_ratio_20d":None}
    high, low = number(current.get("max")), number(current.get("min"))
    if previous_close and None not in (high, low):
        result["amplitude_pct"] = (high - low) / previous_close * 100
    for n in (5, 20):
        previous_volumes = [number(r.get("Trading_Volume")) for r in price_rows[-n-1:-1]] if current else []
        if volume is not None and len(previous_volumes) == n and None not in previous_volumes and sum(previous_volumes) > 0:
            result[f"volume_ratio_{n}d"] = volume / (sum(previous_volumes)/n)
    flow = flow_rows[-1] if flow_rows and flow_rows[-1]["date"] == target else {}
    result["institutional"] = {"source_date":flow.get("date"), **flows(flow), "net_5d_shares":None}
    if flow and len(flow_rows) >= 5:
        recent = [flows(r)["total_net_shares"] for r in flow_rows[-5:]]
        if None not in recent:
            result["institutional"]["net_5d_shares"] = sum(recent)
    credit = credit_rows[-1] if credit_rows and credit_rows[-1]["date"] == target else {}
    result["credit"] = {"source_date":credit.get("date"), "units":"provider-native lots"}
    for prefix, field in (("margin", "MarginPurchase"), ("short", "ShortSale")):
        result["credit"][prefix + "_balance"] = number(credit.get(field + "TodayBalance"))
        result["credit"][prefix + "_change"] = delta(credit, field + "TodayBalance", field + "YesterdayBalance")
        result["credit"][prefix + "_change_5d"] = None
        if credit and len(credit_rows) >= 5:
            changes = [delta(r, field + "TodayBalance", field + "YesterdayBalance") for r in credit_rows[-5:]]
            if None not in changes:
                result["credit"][prefix + "_change_5d"] = sum(changes)
    return result
