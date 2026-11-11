from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from session_calendar import completed_session, session_close

TW = ZoneInfo("Asia/Taipei")

@pytest.mark.parametrize("date", ["2026-10-23", "2026-10-26", "2026-10-27"])
def test_typhoon_and_holiday_resolve_to_last_actual_close(date):
    at = datetime.fromisoformat(date + "T08:50:00").replace(tzinfo=TW)
    result = completed_session("XTAI", at)
    assert result["date"] == "2026-10-22"

def test_exceptional_closed_session_cannot_be_treated_as_close():
    with pytest.raises(ValueError, match="closed exceptionally"):
        session_close("XTAI", "2026-10-23")
