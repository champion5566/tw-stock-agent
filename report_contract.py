"""Explicit data readiness, deadlines and independent delivery state."""
from datetime import datetime, time, timedelta

from instruments import REPORT_STOCKS
from quote_quality import TW, positive_price
from session_calendar import completed_session
from stock_metrics import number

CONTRACT_VERSION = "report-contract-v1"
DELIVERY_TIMES = {"morning":time(8, 50), "evening":time(23, 0)}
CUTOFF_TIMES = {"morning":time(8, 45), "evening":time(22, 58)}
US_REQUIRED = ("SP500", "NASDAQ", "SOX", "VIX", "TSM_ADR", "NVDA", "AMD", "AVGO", "MU")
ASIA_REQUIRED = {"jp":("NIKKEI225", "TOPIX", "ADVANTEST", "TOKYO_ELECTRON"),
                 "kr":("KOSPI", "KOSDAQ", "SAMSUNG", "SK_HYNIX")}


def parse_time(value):
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.replace(tzinfo=TW) if result.tzinfo is None else result
    except (AttributeError, ValueError, TypeError):
        return None


def age_status(observation, checked, maximum):
    stamp = parse_time(observation.get("trade_time") or observation.get("latest_bar_at_taipei"))
    if positive_price(observation.get("price")) is None or stamp is None:
        return "MISSING"
    age = (checked-stamp).total_seconds()/60
    return "FUTURE_TIMESTAMP" if age < -2 else "PASS" if age <= maximum else "DELAYED" if age <= 30 else "STALE"


def section(statuses):
    return {"status":"PASS" if statuses and all(x == "PASS" for x in statuses.values()) else "PARTIAL",
            "items":statuses}


def evaluate(report, market, cross, checked, experiment):
    mode = report["scenario"]
    if mode == "intraday":
        stocks = {code:report["stocks"].get(code, {}).get("status", "MISSING") for code in REPORT_STOCKS}
        future = report["futures"].get("TXFR1", {})
        sections = {"required_stock_quotes":section(stocks),
                    "tx_live":section({"TXFR1":"PASS" if future.get("is_live") else "MISSING_OR_STALE"})}
        return {"version":CONTRACT_VERSION, "data_readiness":"DATA_READY" if all(s["status"] == "PASS" for s in sections.values()) else "DATA_PARTIAL",
                "sections":sections, "delivery_status":"NOT_ACKNOWLEDGED", "parent_ledger_status":"NOT_CHECKED"}
    cutoff = datetime.combine(checked.date(), CUTOFF_TIMES[mode], TW)
    delivery = datetime.combine(checked.date(), DELIVERY_TIMES[mode], TW)
    stock_items = {}
    for code in REPORT_STOCKS:
        item = report["stocks"].get(code, {})
        daily = item.get("daily_ohlcv", {})
        row = daily.get("data") or {}
        feature = item.get("metrics", {})
        needed = [row.get(k) for k in ("open", "max", "min", "close", "Trading_Volume", "Trading_money")]
        needed += [feature.get(k) for k in ("previous_close", "amplitude_pct", "volume_ratio_5d", "volume_ratio_20d")]
        inst = feature.get("institutional", {})
        credit = feature.get("credit", {})
        needed += [inst.get(k) for k in ("foreign_net_shares", "trust_net_shares", "dealer_net_shares", "total_net_shares", "net_5d_shares")]
        needed += [credit.get(k) for k in ("margin_balance", "margin_change", "margin_change_5d", "short_balance", "short_change", "short_change_5d")]
        valid = all(item.get(key, {}).get("status") == "PASS" for key in ("daily_ohlcv", "institutional", "margin"))
        valid = valid and all(number(x) is not None for x in needed) and all(positive_price(row.get(key)) is not None for key in ("open", "max", "min", "close")) and not inst.get("dealer_components_conflict", False)
        stock_items[code] = "PASS" if valid else "MISSING_OR_INVALID_FIELDS"
    sections = {"required_stock_data":section(stock_items)}
    context = market.get("market_context", {})
    required_context = {"TAIEX":("open", "high", "low", "close", "volume", "turnover"),
                        "TPEX":("open", "high", "low", "close", "volume", "turnover"),
                        "breadth":("advances", "declines"),
                        "institutional_totals":("foreign_net_twd", "trust_net_twd", "dealer_net_twd", "total_net_twd"),
                        "margin_totals":("margin_balance", "margin_change", "short_balance", "short_change"),
                        "futures_positioning":("foreign_net_contracts",)}
    sections["market_context"] = section({name:"PASS" if context.get(name, {}).get("status") == "PASS"
        and context[name].get("source_date") == report.get("target_session_date")
        and all(number(context[name].get(key)) is not None for key in keys)
        else "NOT_COLLECTED_OR_WRONG_SESSION" for name, keys in required_context.items()})
    if mode == "morning":
        expected_us = completed_session("XNYS", cutoff)["date"]
        close_items = {}
        for name in US_REQUIRED:
            obs = cross.get("us_regular_close", {}).get(name, {})
            close_items[name] = "PASS" if obs.get("source_date") == expected_us and obs.get("session_completed") and positive_price(obs.get("price")) else "MISSING_COMPLETED_SESSION_BAR"
        sections["us_regular_close"] = section(close_items)
        sections["us_regular_close"]["target_session"] = expected_us
        sections["asia_open"] = section({f"{area}/{name}":age_status(cross.get("assets", {}).get(area, {}).get(name, {}), delivery, 15)
                                        for area, names in ASIA_REQUIRED.items() for name in names})
        tx = cross.get("taifex", {}).get("shioaji_session_tx", {})
        stamp = parse_time(tx.get("trade_time"))
        tw_previous = completed_session("XTAI", datetime.combine(checked.date(), time(8, 50), TW))["date"]
        night_end_day = datetime.fromisoformat(tw_previous).date() + timedelta(days=1)
        end = datetime.combine(night_end_day, time(5), TW)
        valid = stamp is not None and end-timedelta(minutes=10) <= stamp <= end and checked >= end and positive_price(tx.get("price"))
        sections["tx_completed_night"] = section({"TXFR1":"PASS" if valid else "MISSING_COMPLETED_NIGHT_OBSERVATION"})
        sections["tx_completed_night"].update({"night_end_taipei":end.isoformat(), "is_live":False,
                                               "note":"Broker last-trade observation near completed night end; not an exchange-certified settlement."})
    else:
        sections["us_intraday"] = section({name:age_status(cross.get("assets", {}).get("us", {}).get(name, {}), delivery, 15) for name in US_REQUIRED})
        tx = cross.get("taifex", {}).get("shioaji_live_tx", {})
        sections["tx_live"] = section({"TXFR1":age_status(tx, delivery, 10) if tx.get("data_kind") == "tick" else "MISSING_TICK"})
    timing = {}
    for key, payload in (("market", market), ("cross", cross)):
        stamp = parse_time(payload.get("fetched_at_taipei"))
        valid = stamp is not None and stamp.astimezone(TW).date() == checked.date() and stamp <= cutoff
        timing[key] = "PASS" if valid else "MISSING_OR_AFTER_CUTOFF"
    timing["generation"] = "PASS" if checked <= cutoff else "AFTER_CUTOFF"
    sections["cutoff"] = section(timing)
    ready = all(s["status"] == "PASS" for s in sections.values())
    return {"version":CONTRACT_VERSION, "data_readiness":"DATA_READY" if ready else "DATA_PARTIAL",
            "required_stocks":list(REPORT_STOCKS), "sections":sections,
            "cutoff_taipei":cutoff.isoformat(), "delivery_target_taipei":delivery.isoformat(),
            "execution_kind":"PREVIEW" if experiment else "SCHEDULED_PREPARATION",
            "parent_ledger_status":"NOT_CHECKED", "delivery_status":"NOT_ACKNOWLEDGED",
            "limitations":["GitHub/ChatGPT schedules are best effort; completion is not user delivery acknowledgment.",
                           "TOPIX_ETF_PROXY is an ETF proxy, not TOPIX index points.",
                           "Exchange calendars may omit ad-hoc closures; missing expected source data stays partial."]}
