"""Overlay snapshots while keeping timely report packages ahead of late retries.

This records a pre-push check, not a delivery or publication acknowledgment.
Consumers must also check the data-branch commit time against the report cutoff.
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo

TW = ZoneInfo('Asia/Taipei')


def timestamp(value):
    try:
        stamp = datetime.fromisoformat(value)
        return stamp if stamp.tzinfo else None
    except (TypeError, ValueError):
        return None


def rank(report):
    readiness = report.get('readiness', {})
    cutoff = timestamp(readiness.get('cutoff_taipei'))
    generated = timestamp(report.get('generated_at_taipei'))
    checked = timestamp(report.get('publication_check_at_taipei'))
    timely = bool(cutoff and generated and checked and generated <= checked <= cutoff
                  and readiness.get('sections', {}).get('cutoff', {}).get('status') == 'PASS'
                  and report.get('execution_kind') != 'CURRENT_TIME_PREVIEW')
    passed = sum(s.get('status') == 'PASS' for s in readiness.get('sections', {}).values())
    return timely, passed, generated.isoformat() if generated else ''


def overlay(source, target, now=None):
    now = now or datetime.now(TW)
    for path in sorted(source.rglob('*.json')):
        relative = path.relative_to(source)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        canonical = len(relative.parts) == 3 and relative.parts[0] == 'reports' and relative.name in ('morning.json', 'evening.json')
        if not canonical:
            shutil.copyfile(path, destination)
            continue
        incoming = json.loads(path.read_text())
        incoming['publication_check_at_taipei'] = now.isoformat()
        incoming['publication_status'] = 'PENDING_PUSH_AND_READBACK'
        incoming['timing_eligible_at_publish_check'] = rank(incoming)[0]
        incoming['formal_sample_eligible'] = False
        incoming['formal_sample_note'] = 'Require original pre-open ledger, qualified inputs, and data-branch commit timestamp <= cutoff; pipeline alone does not certify a prediction.'
        body = json.dumps(incoming, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        archive = destination.parent / 'publication-observations' / destination.stem
        archive.mkdir(parents=True, exist_ok=True)
        (archive / (uuid4().hex + '.json')).write_text(body)
        existing = json.loads(destination.read_text()) if destination.exists() else None
        if existing is None or rank(incoming) >= rank(existing):
            destination.write_text(body)
            print('REPORT_SELECTED', relative, 'timely=', rank(incoming)[0])
        else:
            print('REPORT_PRESERVED', relative, 'late/weaker retry archived')


if __name__ == '__main__':
    overlay(Path(sys.argv[1]), Path(sys.argv[2]))
