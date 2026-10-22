"""Use maintained exchange calendars rather than inferring dates from source availability."""
from datetime import datetime
from functools import lru_cache

import exchange_calendars as xcals
import pandas as pd


@lru_cache(maxsize=4)
def calendar(name):
    return xcals.get_calendar(name)


def completed_session(name, checked_at):
    cal = calendar(name)
    closed = cal.previous_close(pd.Timestamp(checked_at))
    session = closed.tz_convert(cal.tz).date().isoformat()
    return {"date": session, "closed_at": closed.to_pydatetime().isoformat(),
            "calendar": name, "calendar_library_version": xcals.__version__}


def session_close(name, session):
    return calendar(name).session_close(session).to_pydatetime()
