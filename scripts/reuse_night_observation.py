"""Reuse a prior collected night observation; never substitute a daytime snapshot."""
import json
from datetime import datetime, time, timedelta
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quote_quality import TW, positive_price
from report_contract import parse_time
from session_calendar import completed_session


def select(current, stored, now):
    previous = completed_session('XTAI', datetime.combine(now.date(), time(8, 40), TW))['date']
    end = datetime.combine(datetime.fromisoformat(previous).date()+timedelta(days=1), time(5), TW)
    receipt = parse_time(stored.get('collection_completed_at_taipei') or stored.get('fetched_at_taipei'))
    quote = stored.get('taifex', {}).get('shioaji_session_tx', {})
    stamp = parse_time(quote.get('trade_time'))
    if receipt is not None and receipt <= now and stamp is not None and end-timedelta(minutes=10) <= stamp <= end <= now and positive_price(quote.get('price')):
        current.setdefault('taifex', {})['shioaji_session_tx'] = quote
        current['completed_night_input'] = {'collected_at_taipei':receipt.isoformat(), 'original_trade_time':stamp.isoformat()}
    return current


def main():
    now = datetime.now(TW)
    day = now.date().isoformat()
    current = Path('out') / day / 'cross-morning.json'
    prior = Path('stored-snapshots') / day / 'cross-nightclose.json'
    if prior.exists():
        payload = select(json.loads(current.read_text()), json.loads(prior.read_text()), now)
        payload['collection_completed_at_taipei'] = now.isoformat()
        current.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
        print('COMPLETED_NIGHT_REUSE', bool(payload.get('completed_night_input')))
    else:
        print('COMPLETED_NIGHT_REUSE MISSING; current source retained and validated')


if __name__ == '__main__': main()
