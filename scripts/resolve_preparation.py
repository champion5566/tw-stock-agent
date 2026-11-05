"""Resolve native cron/dispatch/request-file events without executing request text."""
import json
import os
import subprocess
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

TW = ZoneInfo('Asia/Taipei')
SLOTS = {'35 21 * * 1-5':'nightclose', '30 0 * * 1-5':'morning',
         '35 0 * * 1-5':'morning', '52 14 * * 1-5':'evening'}


def resolve(event, event_name, now, changed=()):
    slot = event.get('inputs', {}).get('slot') or SLOTS.get(event.get('schedule'))
    kind = 'SCHEDULED_PREPARATION' if event_name == 'schedule' else 'PREVIEW'
    # Only a push represents a newly submitted request. Cron/dispatch may run
    # with a request-file commit at HEAD; that does not resubmit the old request.
    requests = [p for p in changed if p.startswith('preparation/requests/') and p.endswith('.json')] if event_name == 'push' else []
    if requests:
        if len(requests) != 1:
            raise ValueError('Exactly one preparation request per push')
        path = Path(requests[0])
        request = json.loads(path.read_text())
        slot = request.get('slot')
        expected = f'preparation/requests/{now.date().isoformat()}/{slot}.json'
        stamp = datetime.fromisoformat(request['requested_at_taipei'])
        if stamp.tzinfo is None or not (0 <= (now-stamp).total_seconds() <= 3600):
            raise ValueError('Request timestamp must be recent, timezone-aware and not future')
        if str(path) != expected or request.get('schema_version') != 'preparation-request-v1':
            raise ValueError('Request date/path/schema mismatch')
        kind = 'REQUEST_PREPARATION'
    slot = slot or ('morning' if 8 <= now.hour < 12 else 'evening')
    if slot not in ('morning', 'evening', 'nightclose'):
        raise ValueError('Unsupported slot')
    if slot == 'morning' and now.time() < time(8, 20):
        raise ValueError('Morning collection cannot begin before 08:20 Taipei')
    return slot, kind


def main():
    now = datetime.now(TW)
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    changed = subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'], text=True).splitlines()
    slot, kind = resolve(event, os.getenv('GITHUB_EVENT_NAME'), now, changed)
    with open(os.environ['GITHUB_ENV'], 'a') as stream:
        stream.write(f'REPORT_SLOT={slot}\nPREPARATION_KIND={kind}\nPREPARATION_STARTED_AT={now.isoformat()}\n')
    print('PREPARATION_RESOLVED', slot, kind, now.isoformat())


if __name__ == '__main__':
    main()
