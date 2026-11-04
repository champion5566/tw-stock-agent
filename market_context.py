"""Market-wide official sources selected from maintained TWSE/TPEx projects.

Thin adapters retain source dates, names and units; a failed item does not hide
independent successes. Latest-only endpoints are checked before dated fallback.
"""
import csv
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import requests

from quote_quality import TW
from session_calendar import completed_session
from report_contract import DELIVERY_TIMES
from snapshot_io import write_snapshot
from market_sources import finmind

HEADERS = {'User-Agent':'Mozilla/5.0 (compatible; tw-stock-agent public market research)', 'Accept':'application/json,text/csv'}


def num(value):
    try: return float(str(value).replace(',', '').strip())
    except (TypeError, ValueError): return None


def day(value):
    value = str(value or '').replace('/', '').replace('-', '')
    try:
        if len(value) == 7: value = str(int(value[:3])+1911)+value[3:]
        return datetime.strptime(value, '%Y%m%d').date().isoformat()
    except ValueError: return None


def fetch(url, **kwargs):
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    with requests.Session() as session:
        session.mount('https://', HTTPAdapter(max_retries=Retry(total=1, backoff_factor=0.5,
            status_forcelist=(429,500,502,503,504), allowed_methods=('GET','POST'), respect_retry_after_header=False)))
        response = session.request('POST' if 'data' in kwargs else 'GET', url, headers=HEADERS, timeout=(8,15), **kwargs)
        response.raise_for_status()
    try: return response.json()
    except ValueError:
        raw = response.content
        text = raw.decode('utf-8-sig', errors='replace')
        if '\ufffd' in text: text = raw.decode('cp950')
        if '<html' in text.lower() or '<!doctype' in text.lower(): raise ValueError('Upstream returned HTML, not market data')
        rows = list(csv.DictReader(io.StringIO(text)))
        if not rows: raise ValueError('Empty upstream CSV')
        return rows


def record(target, source_date, source, **values):
    return {'status':'PASS' if source_date == target and all(v is not None for v in values.values()) else 'MISSING_OR_WRONG_SESSION',
            'source_date':source_date, 'source':source, **values}


def table_rows(payload, required):
    if not isinstance(payload, dict): return []
    tables = payload.get('tables', [payload])
    if not isinstance(tables, list): return []
    for table in tables:
        if not isinstance(table, dict): continue
        fields = table.get('fields') or []
        if all(key in fields for key in required):
            return [dict(zip(fields, row)) for row in table.get('data', []) if isinstance(row, list) and len(row) >= len(fields)]
    return []


def parse_context(raw, target):
    raw = {key:([r for r in value if isinstance(r,dict)] if isinstance(value,list) else value) for key,value in raw.items()}
    result = {}
    mi = raw.get('mi', {})
    if not isinstance(mi, dict): mi = {}
    mi_day = day(mi.get('date'))
    hist = raw.get('taiex', [])
    row = next((r for r in hist if day(r.get('Date')) == target), {}) if isinstance(hist, list) else {}
    total_rows = table_rows(mi, ('成交統計','成交金額(元)','成交股數(股)'))
    total = next((r for r in total_rows if str(r.get('成交統計','')).startswith('總計')), {})
    if row:
        result['TAIEX'] = record(target, day(row.get('Date')), 'TWSE MI_5MINS_HIST + dated MI_INDEX market totals',
            open=num(row.get('OpeningIndex')), high=num(row.get('HighestIndex')), low=num(row.get('LowestIndex')), close=num(row.get('ClosingIndex')),
            volume=num(total.get('成交股數(股)')) if mi_day == target else None,
            turnover=num(total.get('成交金額(元)')) if mi_day == target else None)
        result['TAIEX']['volume_scope'] = 'TWSE whole-market shares; index points themselves have no traded volume'
    fm = raw.get('taiex_fallback') or []
    if not result.get('TAIEX', {}).get('status') == 'PASS' and isinstance(fm, list):
        row = next((r for r in fm if r.get('date') == target), {})
        if row:
            result['TAIEX'] = record(target, row.get('date'), 'FinMind TaiwanStockPrice TAIEX',
                open=num(row.get('open')), high=num(row.get('max')), low=num(row.get('min')), close=num(row.get('close')),
                volume=num(row.get('Trading_Volume')), turnover=num(row.get('Trading_money')))
    otc = raw.get('otc', [])
    row = next((r for r in otc if day(r.get('Date')) == target), {}) if isinstance(otc, list) else {}
    vol = raw.get('otc_volume', [])
    v = next((r for r in vol if day(r.get('Date')) == target), {}) if isinstance(vol, list) else {}
    if row:
        result['TPEX'] = record(target, day(row.get('Date')), 'TPEx tpex_index + tpex_daily_trading_index',
            open=num(row.get('Open')), high=num(row.get('High')), low=num(row.get('Low')), close=num(row.get('Close')),
            volume=num(v.get('TradeVolume')), turnover=num(v.get('TradeAmount')))
    breadth = table_rows(mi, ('類型','股票'))
    def breadth_count(prefix):
        cell = next((r['股票'] for r in breadth if r['類型'].startswith(prefix)), '')
        return num(str(cell).split('(')[0])
    result['breadth'] = record(target, mi_day, 'TWSE MI_INDEX stock-only breadth', advances=breadth_count('上漲'), declines=breadth_count('下跌'))
    result['breadth']['scope'] = 'TWSE stocks; excludes warrant-heavy all-security counts'
    inst = raw.get('institutional', {})
    if isinstance(inst, dict):
        rows = table_rows(inst, ('單位名稱','買賣差額'))
        def net(prefix):
            vals = [num(r['買賣差額']) for r in rows if r['單位名稱'].startswith(prefix)]
            return sum(vals) if vals and all(v is not None for v in vals) else None
        result['institutional_totals'] = record(target, day(inst.get('date')), 'TWSE BFI82U TWD; foreign dealer not double counted',
            foreign_net_twd=net('外資及陸資'), trust_net_twd=net('投信'), dealer_net_twd=net('自營商'), total_net_twd=net('合計'))
        result['institutional_totals']['scope'] = 'TWSE; foreign-dealer amounts are already included in dealer/official total'
    otc_inst = raw.get('otc_institutional', [])
    if isinstance(otc_inst, list):
        entries = [r for r in otc_inst if day(r.get('Date')) == target]
        def otc_net(label):
            r = next((r for r in entries if r.get('Investor','').replace('\\u3000','').strip() == label), {})
            return num(r.get('Net'))
        foreign = otc_net('外資及陸資(不含自營商)')
        trust, dealer, total = otc_net('投信'), otc_net('自營商合計'), otc_net('三大法人合計*')
        otc_record = record(target, target if entries else None, 'TPEx tpex_3insti_summary TWD',
            foreign_net_twd=foreign, trust_net_twd=trust, dealer_net_twd=dealer, total_net_twd=total)
        if all(x is not None for x in (foreign,trust,dealer,total)) and abs(foreign+trust+dealer-total) > 1:
            otc_record['status'] = 'COMPONENT_SUM_CONFLICT'
        listed = result.get('institutional_totals', {})
        result['institutional_by_market'] = {'TWSE':dict(listed), 'TPEx':otc_record}
        if 'otc_institutional' in raw and not listed.get('status') == otc_record.get('status') == 'PASS':
            result['institutional_totals'] = {**listed, 'status':'PARTIAL_MARKET_COVERAGE', 'scope':'TWSE only; TPEx component missing or inconsistent'}
        if listed.get('status') == otc_record.get('status') == 'PASS':
            keys = ('foreign_net_twd','trust_net_twd','dealer_net_twd','total_net_twd')
            result['institutional_totals'] = record(target, target, 'TWSE BFI82U + TPEx official summary; TWD',
                **{key:listed[key]+otc_record[key] for key in keys})
            result['institutional_totals']['scope'] = 'TWSE + TPEx; foreign dealers not double counted'

    margin = raw.get('margin', {})
    if isinstance(margin, dict):
        rows = table_rows(margin, ('項目','前日餘額','今日餘額'))
        balances = {r['項目']:(num(r['前日餘額']),num(r['今日餘額'])) for r in rows}
        before, current = balances.get('融資(交易單位)', (None,None))
        sb, sc = balances.get('融券(交易單位)', (None,None))
        result['margin_totals'] = record(target, day(margin.get('date')), 'TWSE MI_MARGN credit statistics',
            margin_balance=current, margin_change=current-before if current is not None and before is not None else None,
            short_balance=sc, short_change=sc-sb if sc is not None and sb is not None else None)
        result['margin_totals']['units'] = 'provider trading units (lots); no second division by 1000'
        result['margin_totals']['scope'] = 'TWSE'
    quotes = raw.get('otc_quotes') or []
    ordinary = {r.get('SecuritiesCompanyCode'):r for r in quotes if day(r.get('Date')) == target
                and len(str(r.get('SecuritiesCompanyCode',''))) == 4 and str(r.get('SecuritiesCompanyCode','')).isdigit()}
    changes = [num(r.get('Change')) for r in ordinary.values()]
    otc_breadth = record(target, target if ordinary else None, 'TPEx daily close; derived four-digit stock breadth',
        advances=sum(x > 0 for x in changes if x is not None) if ordinary else None,
        declines=sum(x < 0 for x in changes if x is not None) if ordinary else None)
    otc_breadth.update({'scope':'TPEx four-digit stocks; ETFs/warrants excluded',
                       'not_comparable':sum(x is None for x in changes), 'pool_size':len(ordinary)})
    if ordinary and all(x is None for x in changes): otc_breadth['status'] = 'MISSING_COMPARABLE_CHANGES'
    result['breadth_by_market'] = {'TWSE':dict(result['breadth']), 'TPEx':otc_breadth}
    credit = raw.get('otc_margin') or []
    current_credit = {r.get('SecuritiesCompanyCode'):r for r in credit if day(r.get('Date')) == target}
    def credit_sum(key):
        values = [num(r.get(key)) for r in current_credit.values()]
        return sum(values) if values and all(x is not None for x in values) else None
    mb, mp = credit_sum('MarginPurchaseBalance'), credit_sum('MarginPurchaseBalancePreviousDay')
    sb, sp = credit_sum('ShortSaleBalance'), credit_sum('ShortSaleBalancePreviousDay')
    otc_credit = record(target, target if current_credit else None, 'TPEx margin balances, unique instrument rows summed',
        margin_balance=mb, margin_change=mb-mp if mb is not None and mp is not None else None,
        short_balance=sb, short_change=sb-sp if sb is not None and sp is not None else None)
    otc_credit['units'] = 'TPEx provider-native balance units; reported separately, not combined with differently scoped totals'
    result['margin_by_market'] = {'TWSE':dict(result.get('margin_totals',{})), 'TPEx':otc_credit}
    future = raw.get('futures', [])
    if isinstance(future, list):
        r = next((r for r in future if day(r.get('Date') or r.get('日期')) == target
                  and (r.get('ContractCode') or r.get('商品名稱')) == '臺股期貨'
                  and (r.get('Item') or r.get('身份別')) == '外資及陸資'), {})
        result['futures_positioning'] = record(target, day(r.get('Date') or r.get('日期')), 'TAIFEX TX foreign net open interest, dated official API/CSV',
            foreign_net_contracts=num(r.get('OpenInterest(Net)') if 'OpenInterest(Net)' in r else r.get('多空未平倉口數淨額')))
    if result.get('futures_positioning', {}).get('status') != 'PASS':
        candidates = raw.get('futures_fallback') or []
        r = next((r for r in candidates if r.get('date') == target and (r.get('futures_id') or r.get('name')) in ('TX','TXF')
                  and r.get('institutional_investors') == '外資'), {})
        long_oi, short_oi = num(r.get('long_open_interest_balance_volume')), num(r.get('short_open_interest_balance_volume'))
        if r:
            result['futures_positioning'] = record(target, r.get('date'), 'FinMind TaiwanFuturesInstitutionalInvestors TX fallback',
                foreign_net_contracts=long_oi-short_oi if long_oi is not None and short_oi is not None else None)

    indices = table_rows(mi, ('指數','收盤指數','漲跌百分比(%)'))
    result['sector_performance'] = {'source_date':mi_day,'source':'TWSE official price-index board; price performance is not capital flow',
        'items':[{'name':r['指數'],'close':num(r['收盤指數']),'change_pct':num(r['漲跌百分比(%)'])} for r in indices]}
    return result


def collect_context(target, checked):
    d = target.replace('-', '')
    urls = {
        'mi':f'https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={d}&type=ALL&response=json',
        'taiex':'https://openapi.twse.com.tw/v1/indicesReport/MI_5MINS_HIST',
        'otc':'https://www.tpex.org.tw/openapi/v1/tpex_index',
        'otc_volume':'https://www.tpex.org.tw/openapi/v1/tpex_daily_trading_index',
        'otc_quotes':'https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes',
        'otc_margin':'https://www.tpex.org.tw/openapi/v1/tpex_mainboard_margin_balance',
        'otc_institutional':'https://www.tpex.org.tw/openapi/v1/tpex_3insti_summary',
        'institutional':f'https://www.twse.com.tw/rwd/zh/fund/BFI82U?dayDate={d}&type=day&response=json',
        'margin':f'https://www.twse.com.tw/rwd/zh/marginTrading/MI_MARGN?date={d}&selectType=MS&response=json',
        'futures':'https://openapi.taifex.com.tw/v1/MarketDataOfMajorInstitutionalTradersDetailsOfFuturesContractsBytheDate'}
    raw, diagnostics = {}, []
    def run(item):
        name, url = item
        try: return name, fetch(url), None
        except Exception as exc: return name, None, type(exc).__name__+': '+str(exc)[:180]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for name, payload, error in pool.map(run, urls.items()):
            raw[name] = payload
            diagnostics.append({'name':name,'url':urls[name],'status':'FAIL' if error else 'FETCHED','error':error})
    context = parse_context(raw, target)
    if context.get('TAIEX', {}).get('status') != 'PASS':
        try: raw['taiex_fallback'] = finmind('TaiwanStockPrice','TAIEX',target,target)
        except Exception as exc: diagnostics.append({'name':'taiex_finmind','error':str(exc)[:180]})
    if context.get('futures_positioning', {}).get('status') != 'PASS':
        try:
            raw['futures'] = fetch('https://www.taifex.com.tw/cht/3/futContractsDateDown',
                data={'queryStartDate':target.replace('-','/'),'queryEndDate':target.replace('-','/'),'commodityId':'TXF'})
            diagnostics.append({'name':'futures_dated_csv','status':'FETCHED','target':target})
        except Exception as exc: diagnostics.append({'name':'futures_dated_csv','error':str(exc)[:180]})
    context = parse_context(raw, target)
    if context.get('futures_positioning', {}).get('status') != 'PASS':
        try:
            raw['futures_fallback'] = finmind('TaiwanFuturesInstitutionalInvestors','TX',target,target)
            diagnostics.append({'name':'futures_finmind','status':'FETCHED','target':target})
        except Exception as exc: diagnostics.append({'name':'futures_finmind','error':str(exc)[:180]})
        context = parse_context(raw, target)
    context['_diagnostics'] = diagnostics
    context['_collected_at_taipei'] = checked.isoformat()
    return context


def main():
    now = datetime.now(TW)
    slot = os.environ.get('REPORT_SLOT', 'evening')
    target = completed_session('XTAI', datetime.combine(now.date(), DELIVERY_TIMES[slot], TW))['date']
    path = Path('out') / now.date().isoformat() / (slot+'.json')
    payload = json.loads(path.read_text())
    try:
        payload['market_context'] = collect_context(target, now)
    except Exception as exc:
        payload['market_context'] = {'_error':type(exc).__name__+': '+str(exc)[:200], '_status':'PARTIAL_CONTEXT_FAILURE'}
    payload['collection_completed_at_taipei'] = datetime.now(TW).isoformat()
    write_snapshot(payload, now.date().isoformat(), slot)
    print('MARKET_CONTEXT', json.dumps({k:v.get('status') for k,v in payload['market_context'].items() if not k.startswith('_')},ensure_ascii=False))


if __name__ == '__main__': main()
