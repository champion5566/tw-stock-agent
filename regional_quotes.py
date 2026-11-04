"""Regional sources used by maintained Naver/finance projects; no credentials.

Public page quotes are observations, never broker ticks. Original provider time,
precision, response clock and market state stay attached to the selected source.
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

from quote_quality import TW, positive_price, quote_status

JP = ZoneInfo('Asia/Tokyo')
KR = ZoneInfo('Asia/Seoul')
HEADERS = {'User-Agent':'Mozilla/5.0 (compatible; tw-stock-agent public market research)', 'Accept':'application/json,text/html'}
JP_CODES = {'NIKKEI225':'998407.O', 'TOPIX':'998405.T', 'ADVANTEST':'6857.T', 'TOKYO_ELECTRON':'8035.T'}
KR_CODES = {'KOSPI':'KOSPI', 'KOSDAQ':'KOSDAQ', 'KPI200':'KOSPI200', '005930':'SAMSUNG', '000660':'SK_HYNIX'}


def number(value):
    try: return float(str(value).replace(',', ''))
    except (TypeError, ValueError): return None


def get(url):
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    with requests.Session() as session:
        session.mount('https://', HTTPAdapter(max_retries=Retry(total=1, backoff_factor=0.5,
            status_forcelist=(429,500,502,503,504), allowed_methods=('GET',), respect_retry_after_header=False)))
        response = session.get(url, headers=HEADERS, timeout=(4,10))
        response.raise_for_status()
        return response


def parse_naver(item, checked):
    price = positive_price(number(item.get('closePriceRaw') or item.get('closePrice')))
    raw_time = item.get('localTradedAt')
    try:
        stamp = datetime.fromisoformat(raw_time)
        if stamp.tzinfo is None: stamp = None
    except (TypeError, ValueError): stamp = None
    status = quote_status(price, stamp, checked, max_age_minutes=15)
    if stamp and item.get('marketStatus') == 'CLOSE' and status == 'PASS': status = 'MARKET_CLOSED'
    return {'price':price, 'status':status, 'source':'Naver public regional quote',
            'ticker':item.get('itemCode') or item.get('reutersCode'), 'trade_time':stamp.isoformat() if stamp else None,
            'latest_bar_at_taipei':stamp.astimezone(TW).isoformat() if stamp else None,
            'provider_time_text':raw_time, 'market_status':item.get('marketStatus'),
            'provider_delay_minutes':item.get('stockExchangeType', {}).get('delayTime'),
            'change_pct':number(item.get('fluctuationsRatioRaw') or item.get('fluctuationsRatio')),
            'open':number(item.get('openPriceRaw') or item.get('openPrice')),
            'high':number(item.get('highPriceRaw') or item.get('highPrice')),
            'low':number(item.get('lowPriceRaw') or item.get('lowPrice')),
            'data_kind':'provider_quote', 'is_live':False, 'is_formal_close':False,
            'timestamp_basis':'provider localTradedAt with explicit offset',
            'fetched_at_taipei':checked.isoformat()}


def naver_group(kind, codes, checked):
    url = f'https://polling.finance.naver.com/api/realtime/domestic/{kind}/{codes}'
    result = {}
    for item in get(url).json().get('datas', []):
        name = KR_CODES.get(item.get('itemCode'))
        if name:
            result[name] = {**parse_naver(item, checked), 'source_url':url}
    return result


def naver_world(code, checked):
    kind = 'stock' if code.endswith('.T') else 'index'
    url = f'https://api.stock.naver.com/{kind}/{code}/basic'
    return {**parse_naver(get(url).json(), checked), 'source':f'Naver world {kind} quote', 'source_url':url}


def price_board(html):
    soup = BeautifulSoup(html, 'html.parser')
    decoder = json.JSONDecoder()
    for script in soup.find_all('script'):
        text = script.get_text()
        if 'priceBoard' not in text or 'self.__next_f.push(' not in text: continue
        try: payload = json.loads(text[text.index('(')+1:text.rfind(')')])[1]
        except (ValueError, TypeError, IndexError): continue
        match = re.search(r'"priceBoard"\s*:\s*', payload)
        if match:
            board, _ = decoder.raw_decode(payload[match.end():])
            if isinstance(board.get('board'), dict):
                stock = board['board']
                return {**stock, 'code':stock.get('codeWithMarketExtension') or stock.get('code'),
                        'price':{**stock.get('price', {}), 'updateDate':stock.get('japanUpdateTime'),
                                 'changePriceRate':stock.get('priceChangeRate', {}).get('value'),
                                 'delayMinutes':stock.get('delayMinutes')}}
            return board
    raise ValueError('Yahoo Japan priceBoard schema missing; do not guess a page-wide number')


def parse_japan(html, code, checked, response_date=None):
    board = price_board(html)
    if board.get('code') not in (code, code.split('.')[0]): raise ValueError('Yahoo Japan instrument identity mismatch')
    info = board.get('price', {})
    raw_time = str(info.get('updateDate') or '')
    price = positive_price(number(info.get('value')))
    stamp, source_date, basis = None, None, 'provider date only; no source clock invented'
    # For a minute-only display, use the provider HTTP Date (not fetch time), and
    # only while that exchange session is actually open. Preserve this inference.
    server = None
    if response_date:
        try: server = parsedate_to_datetime(response_date).astimezone(JP)
        except (TypeError, ValueError): pass
    if re.fullmatch(r'\d{1,2}:\d{2}', raw_time) and server:
        import exchange_calendars as calendars
        hour, minute = map(int, raw_time.split(':'))
        candidate = server.replace(hour=hour, minute=minute, second=0, microsecond=0)
        calendar = calendars.get_calendar('XTKS')
        if calendar.is_open_on_minute(candidate) and calendar.is_open_on_minute(server.replace(second=0, microsecond=0)):
            stamp = candidate
            source_date = candidate.date().isoformat()
            basis = 'provider HH:MM + provider HTTP-Date within open XTKS session; date inferred'
    elif re.fullmatch(r'\d{1,2}/\d{1,2}', raw_time) and server:
        month, day = map(int, raw_time.split('/'))
        year = server.year - (month > server.month)
        source_date = datetime(year, month, day).date().isoformat()
    return {'price':price, 'status':quote_status(price, stamp, checked, max_age_minutes=15),
            'source':'Yahoo Japan regional page', 'ticker':code,
            'source_url':f'https://finance.yahoo.co.jp/quote/{code}',
            'trade_time':stamp.isoformat() if stamp else None,
            'latest_bar_at_taipei':stamp.astimezone(TW).isoformat() if stamp else None,
            'source_date':source_date, 'provider_time_text':raw_time,
            'provider_response_date':response_date, 'timestamp_basis':basis,
            'source_date_inferred':stamp is not None, 'timestamp_precision':'minute' if stamp else 'date',
            'provider_delay_minutes':info.get('delayMinutes'), 'change_pct':number(info.get('changePriceRate')),
            'data_kind':'provider_quote', 'is_live':False, 'is_formal_close':False,
            'fetched_at_taipei':checked.isoformat()}


def japan_quote(code, checked):
    response = get(f'https://finance.yahoo.co.jp/quote/{code}')
    return parse_japan(response.text, code, checked, response.headers.get('Date'))


def collect_asia(checked):
    jobs = [('kr', None, lambda:naver_group('index', 'KOSPI,KOSDAQ,KPI200', checked)),
            ('kr', None, lambda:naver_group('stock', '005930,000660', checked))]
    jobs += [('jp', name, lambda c=code:japan_quote(c, checked)) for name, code in JP_CODES.items()]
    jobs += [('jp_naver', 'TOPIX', lambda:naver_world('.TOPX', checked)), ('jp_naver', 'NIKKEI225', lambda:naver_world('.N225', checked)),
             ('jp_naver', 'ADVANTEST', lambda:naver_world('6857.T', checked)),
             ('jp_naver', 'TOKYO_ELECTRON', lambda:naver_world('8035.T', checked))]
    result = {'jp':{}, 'jp_naver':{}, 'kr':{}, 'errors':[]}
    def run(job):
        area, name, fn = job
        try: return area, name, fn(), None
        except Exception as exc: return area, name, None, type(exc).__name__+': '+str(exc)[:160]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for area, name, data, error in pool.map(run, jobs):
            if error: result['errors'].append({'area':area, 'name':name, 'error':error})
            elif name: result[area][name] = data
            else: result[area].update(data)
    for name, fallback in result['jp_naver'].items():
        result['jp'][name] = select_regional(result['jp'].get(name, {}), fallback, checked)
    return result


def select_regional(primary, fallback, checked):
    def valid(item):
        if not item or item.get('status') != 'PASS': return False
        try: stamp = datetime.fromisoformat(item.get('trade_time') or item['latest_bar_at_taipei'])
        except (KeyError, TypeError, ValueError): return False
        return quote_status(item.get('price'), stamp, checked, 15) == 'PASS'
    chosen = primary if valid(primary) else fallback if valid(fallback) else fallback if fallback.get('price') is not None and fallback.get('trade_time') and not primary.get('trade_time') else primary if primary.get('price') is not None else fallback
    return {**chosen, 'regional_selection':{'primary_source':primary.get('source'), 'primary_status':primary.get('status'),
            'fallback_source':fallback.get('source'), 'fallback_status':fallback.get('status'),
            'selected_source':chosen.get('source')}, 'source_observations':{'regional':primary,'global_yahoo':fallback}}
