"""Deterministic daily-close rendering and draft checks; no model grading."""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re

from instruments import REPORT_STOCKS


def canonical_closes(bundle):
    output = {}
    target = bundle.get('target_session_date')
    for code in REPORT_STOCKS:
        section = bundle.get('stocks', {}).get(code, {}).get('daily_ohlcv', {})
        row = section.get('data') or {}
        if section.get('status') != 'PASS' or section.get('source_date') != target or row.get('date') != target:
            continue
        try:
            value = Decimal(str(row.get('close')))
            if value.is_finite() and value > 0 and str(row.get('stock_id')) == code:
                output[code] = value
        except InvalidOperation:
            continue
    return output


def render_close_table(bundle):
    values = canonical_closes(bundle)
    lines = ['| 代號 | 收盤 |', '|---|---:|']
    lines += [f'| {code} | {values[code]:.2f} |' if code in values
              else f'| {code} | N/A |' for code in REPORT_STOCKS]
    return '\n'.join(lines)


US_DISPLAY_ORDER = ("SP500", "NASDAQ", "SOX", "TSM_ADR", "NVDA", "AMD", "AVGO", "MU", "VIX")


def render_us_regular_close_table(bundle):
    """Use dated, same-provider completed US regular bars; never mix live/extended quotes."""
    if bundle.get('scenario') != 'morning':
        return ''
    rows = ['| 指標 | 前收日期 | 前收 | 收盤日期 | 收盤 | 日報酬 |',
            '|---|---|---:|---|---:|---:|']
    for code in US_DISPLAY_ORDER:
        obs = bundle.get('us_regular_close', {}).get(code, {})
        previous_date, current_date = obs.get('previous_source_date'), obs.get('source_date')
        try:
            previous = Decimal(str(obs.get('previous_close')))
            current = Decimal(str(obs.get('price')))
            change = Decimal(str(obs.get('change_pct')))
            valid = (obs.get('status') == 'PASS' and obs.get('change_status') == 'PASS'
                     and obs.get('session_completed') is True
                     and previous.is_finite() and current.is_finite() and change.is_finite()
                     and previous > 0 and current > 0
                     and isinstance(previous_date, str) and isinstance(current_date, str)
                     and re.fullmatch(r'\\d{4}-\\d{2}-\\d{2}', previous_date)
                     and re.fullmatch(r'\\d{4}-\\d{2}-\\d{2}', current_date)
                     and previous_date < current_date)
        except (InvalidOperation, TypeError, ValueError):
            valid = False
        if valid:
            rows.append(f'| {code} | {previous_date} | {previous:.2f} | {current_date} | {current:.2f} | {change:+.2f}% |')
        else:
            rows.append(f'| {code} | N/A | N/A | N/A | N/A | N/A |')
    return '\\n'.join(rows)


def check_close_table(bundle, markdown):
    expected = canonical_closes(bundle)
    active, table_seen, found, errors, missing, seen = False, False, {}, [], [], set()
    for line in markdown.splitlines():
        if not line.strip().startswith('|'):
            active = False
            continue
        cells = [x.strip().strip('*') for x in line.strip().strip('|').split('|')]
        if len(cells) < 2:
            continue
        if cells[0] not in REPORT_STOCKS:
            if not re.fullmatch(r'[-: ]+', cells[0]):
                active = ('收盤' in cells[1] and not any(x in cells[1] for x in ('預測', '前收', '目標', '成本')))
                table_seen = table_seen or active
            continue
        if not active:
            continue
        code = cells[0]
        if code in seen:
            errors.append({'code': code, 'reason': 'DUPLICATE_CLOSE_ROW'})
        seen.add(code)
        if cells[1] in ('N/A', '—') and code not in expected:
            missing.append(code)
            continue
        try:
            value = Decimal(cells[1].replace(',', ''))
        except InvalidOperation:
            errors.append({'code': code, 'reason': 'REPORTED_CLOSE_NOT_NUMERIC'})
            continue
        found[code] = str(value)
        if code not in expected:
            errors.append({'code': code, 'reason': 'NO_CURRENT_CANONICAL_CLOSE'})
        elif value != expected[code]:
            errors.append({'code': code, 'reason': 'CLOSE_MISMATCH', 'reported': str(value),
                           'expected': str(expected[code]), 'field': f"$.stocks['{code}'].daily_ohlcv.data.close"})
    if table_seen:
        errors.extend({'code': code, 'reason': 'REQUIRED_CLOSE_ROW_MISSING'}
                      for code in REPORT_STOCKS if code not in seen)
    return {'status': 'FAIL' if errors else 'PARTIAL' if missing else 'PASS' if found else 'NOT_CHECKED_NO_CLOSE_TABLE',
            'target_session': bundle.get('target_session_date'), 'checked': len(found), 'errors': errors,
            'missing_source_closes': missing,
            'scope': 'Displayed daily-close table only; no claim of full text or source correctness.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', required=True)
    parser.add_argument('--report')
    args = parser.parse_args()
    bundle = json.loads(Path(args.bundle).read_text(encoding='utf-8'))
    if args.report:
        result = check_close_table(bundle, Path(args.report).read_text(encoding='utf-8'))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(1 if result['status'] == 'FAIL' else 0)
    print(render_close_table(bundle))
