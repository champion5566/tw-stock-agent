"""Exchange calendar with audited exceptional Taiwan market closures.

exchange_calendars handles scheduled holidays. Exceptional typhoon closures are
explicitly maintained here; never infer a trading session from weekdays alone.
"""
from datetime import datetime, timedelta
from functools import lru_cache

import exchange_calendars as xcals
import pandas as pd

# Confirmed TWSE/TPEx exceptional full-day closures, separate from annual holidays.
# 2026-10-23: Typhoon Kong-rey? NO: Typhoon 薔琵 (2026-10-22 TWSE announcement).
# Official announcement: https://www.twse.com.tw/ ; contemporaneous CNA 2026-10-22.
EXCEPTIONAL_CLOSURES = {
    "XTAI": frozenset({"2026-10-23"}),
}


@lru_cache(maxsize=4)
def calendar(name):
    return xcals.get_calendar(name)


def completed_session(name, checked_at):
    cal = calendar(name)
    checked = pd.Timestamp(checked_at)
    closed = cal.previous_close(checked)
    session = closed.tz_convert(cal.tz).date().isoformat()
    skipped = []
    while session in EXCEPTIONAL_CLOSURES.get(name, frozenset()):
        skipped.append(session)
        closed = cal.previous_close(closed - pd.Timedelta(nanoseconds=1))
        session = closed.tz_convert(cal.tz).date().isoformat()
    return {
        "date": session,
        "closed_at": closed.to_pydatetime().isoformat(),
        "calendar": name,
        "calendar_library_version": xcals.__version__,
        "exceptional_closures_skipped": skipped,
    }


def session_close(name, session):
    if str(session) in EXCEPTIONAL_CLOSURES.get(name, frozenset()):
        raise ValueError(f"{name} closed exceptionally on {session}")
    return calendar(name).session_close(session).to_pydatetime()
