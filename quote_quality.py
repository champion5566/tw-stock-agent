"""Shared market quote validation. Source time is never inferred from fetch time."""
from datetime import datetime, timezone
from math import isfinite
from zoneinfo import ZoneInfo

TW = ZoneInfo("Asia/Taipei")

def positive_price(value):
    try:
        result = float(value)
        return result if isfinite(result) and result > 0 else None
    except (TypeError, ValueError, OverflowError):
        return None

def shioaji_snapshot_time(value):
    """Shioaji snapshot ts is a Taiwan wall-clock encoded as epoch-like nanoseconds.

    The observed SDK snapshot ts must not receive a second UTC->Taipei +8h shift.
    Explicit datetime values keep their own timezone. A naive datetime is Taiwan-local.
    """
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=TW)
    if isinstance(value, (int, float)) and isfinite(value) and value > 0:
        seconds = value / 1_000_000_000 if value > 1e12 else value
        try:
            return datetime.fromtimestamp(seconds, timezone.utc).replace(tzinfo=TW)
        except (OverflowError, OSError, ValueError):
            return None
    return None

def quote_status(price, trade_time, checked_at, max_age_minutes=10):
    """Distinguish missing price, missing time, stale trade and future timestamps."""
    if positive_price(price) is None:
        return "NO_LAST_TRADE"
    if not isinstance(trade_time, datetime):
        return "NO_TIMESTAMP"
    trade = trade_time if trade_time.tzinfo else trade_time.replace(tzinfo=TW)
    checked = checked_at if checked_at.tzinfo else checked_at.replace(tzinfo=TW)
    trade, checked = trade.astimezone(TW), checked.astimezone(TW)
    age = (checked - trade).total_seconds() / 60
    if age < -2:
        return "FUTURE_TIMESTAMP"
    if trade.date() != checked.date() and age > max_age_minutes:
        return "PRIOR_SESSION"
    if age > max_age_minutes:
        return "STALE"
    return "PASS"


def parse_source_time(source_date, source_time):
    """An absent source clock cannot be replaced by collection time."""
    if not source_date or not source_time:
        return None
    try:
        stamp = datetime.fromisoformat(f"{source_date}T{source_time}")
        return stamp if stamp.tzinfo else stamp.replace(tzinfo=TW)
    except (ValueError, TypeError):
        return None


def daily_status(source_date, asof, max_age_days=4):
    from datetime import date
    try:
        age = (asof - date.fromisoformat(source_date)).days
    except (ValueError, TypeError):
        return "FAIL"
    if age < 0:
        return "FUTURE_TIMESTAMP"
    return "PASS" if age == 0 else "PRIOR_SESSION" if age <= max_age_days else "STALE"


def select_stock_quote(primary, fallback):
    """Select one complete observation; retain other fields only as diagnostics."""
    if primary and primary.get("status") == "PASS":
        return dict(primary)
    if fallback.get("status") == "PASS":
        return {**fallback, "mis_diagnostic": primary}
    return dict(primary or fallback)


def select_observation(yahoo, iex):
    """Keep Yahoo bar OHLC and clocks out of a selected IEX trade."""
    if iex.get("status") != "PASS":
        return dict(yahoo)
    stamp = datetime.fromisoformat(iex["trade_time_utc"].replace("Z", "+00:00"))
    return {**iex, "fallback_yahoo": dict(yahoo),
            "latest_bar_utc": stamp.astimezone(timezone.utc).isoformat(),
            "latest_bar_at_taipei": stamp.astimezone(TW).isoformat(),
            "age_minutes": round(iex["age_seconds"] / 60, 2),
            "data_kind": "trade", "is_formal_close": False}
