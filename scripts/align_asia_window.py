"""Collect slow daily inputs early; align actual Asia quotes near report time."""
import os
import time
from datetime import datetime, time as clock
from zoneinfo import ZoneInfo

TW = ZoneInfo('Asia/Taipei')


def seconds_until_window(now, kind):
    if kind == 'PREVIEW': return 0
    target = datetime.combine(now.date(), clock(8, 28), TW)
    return max(0, min(480, (target-now).total_seconds()))


if __name__ == '__main__':
    now = datetime.now(TW)
    seconds = seconds_until_window(now, os.getenv('PREPARATION_KIND'))
    print('ASIA_FRESHNESS_ALIGNMENT', int(seconds), 'seconds; source clocks still validated', flush=True)
    while seconds > 0:
        time.sleep(min(30, seconds))
        seconds = seconds_until_window(datetime.now(TW), os.getenv('PREPARATION_KIND'))
