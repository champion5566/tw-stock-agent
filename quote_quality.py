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
        return datetime.fromtimestamp(seconds, timezone.utc).replace(tzinfo=TW)
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
    if trade.date() != checked.date():
        return "PRIOR_SESSION"
    age = (checked - trade).total_seconds() / 60
    if age < -2:
        return "FUTURE_TIMESTAMP"
    if age > max_age_minutes:
        return "STALE"
    return "PASS"
