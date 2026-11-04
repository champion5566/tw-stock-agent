import copy
import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from quote_quality import TW
from regional_quotes import parse_naver, parse_japan, select_regional
from market_context import parse_context, day
from collect_cross_market import completed_us_close, security_identity
from report_contract import asia_status
from scripts.align_asia_window import seconds_until_window

NOW = datetime(2026,11,5,8,32,tzinfo=TW)


def page(code='998405.T', value='3,895.38', clock='09:31'):
    payload = '1:'+json.dumps({'priceBoard':{'code':code,'price':{'value':value,'updateDate':clock,'delayMinutes':0}}})
    return '<script>self.__next_f.push('+json.dumps([1,payload])+')</script>'


class RegionalSourceTests(unittest.TestCase):
    def test_naver_preserves_explicit_source_clock_and_percent(self):
        q=parse_naver({'itemCode':'KOSPI','closePrice':'5,683.80','localTradedAt':'2026-11-05T09:31:00+09:00',
                      'marketStatus':'OPEN','fluctuationsRatio':'-1.25'},NOW)
        self.assertEqual(q['price'],5683.8)
        self.assertEqual(q['status'],'PASS')
        self.assertEqual(q['latest_bar_at_taipei'],'2026-11-05T08:31:00+08:00')
        self.assertEqual(q['change_pct'],-1.25)
        self.assertFalse(q['is_live'])

    def test_naver_missing_clock_is_not_replaced_by_fetch_time(self):
        self.assertEqual(parse_naver({'closePrice':'123'},NOW)['status'],'NO_TIMESTAMP')

    def test_japan_priceboard_identity_and_server_date_are_used(self):
        q=parse_japan(page(), '998405.T', NOW, 'Thu, 05 Nov 2026 00:32:00 GMT')
        self.assertEqual(q['status'],'PASS')
        self.assertEqual(q['price'],3895.38)
        self.assertTrue(q['source_date_inferred'])
        self.assertIn('HTTP-Date',q['timestamp_basis'])
        with self.assertRaises(ValueError):parse_japan(page('8035'),'998405.T',NOW)

    def test_japan_equity_nested_board_uses_its_own_price_and_clock(self):
        payload={'priceBoard':{'board':{'codeWithMarketExtension':'6857.T','price':{'value':'34,570'},
                  'japanUpdateTime':'09:31','priceChangeRate':{'value':'-3.35'},'delayMinutes':0}}}
        html='<script>self.__next_f.push('+json.dumps([1,json.dumps(payload)])+')</script>'
        q=parse_japan(html,'6857.T',NOW,'Thu, 05 Nov 2026 00:32:00 GMT')
        self.assertEqual(q['status'],'PASS')
        self.assertEqual(q['price'],34570)
        self.assertEqual(q['change_pct'],-3.35)

    def test_japan_date_only_never_gets_invented_closing_clock(self):
        q=parse_japan(page(clock='11/4'),'998405.T',NOW,'Thu, 05 Nov 2026 00:32:00 GMT')
        self.assertEqual(q['status'],'NO_TIMESTAMP')
        self.assertEqual(q['source_date'],'2026-11-04')
        self.assertIsNone(q['trade_time'])

    def test_japan_without_server_date_cannot_qualify_minute_quote(self):
        self.assertEqual(parse_japan(page(),'998405.T',NOW)['status'],'NO_TIMESTAMP')

    def test_stale_primary_uses_independent_fresh_fallback_without_mixing(self):
        old={'price':100,'source':'regional','status':'STALE','trade_time':'2026-11-04T09:30:00+09:00','high':105}
        new={'price':101,'source':'global','status':'PASS','trade_time':'2026-11-05T09:31:00+09:00'}
        selected=select_regional(old,new,NOW)
        self.assertEqual(selected['source'],'global')
        self.assertNotIn('high',selected)
        self.assertEqual(selected['source_observations']['regional'],old)

    def test_date_only_topix_prefers_timestamped_true_index_observation(self):
        a={'price':3895.38,'source':'JP','status':'NO_TIMESTAMP'}
        b={'price':3895.38,'source':'Naver .TOPX','status':'STALE','trade_time':'2026-11-04T15:30:02+09:00'}
        self.assertEqual(select_regional(a,b,NOW)['source'],'Naver .TOPX')

    def test_japanese_holiday_is_not_a_missing_feed(self):
        delivery=datetime(2026,11,3,8,40,tzinfo=TW)
        self.assertEqual(asia_status('jp',{},delivery,delivery.replace(minute=38)),'MARKET_CLOSED')
        self.assertEqual(asia_status('kr',{},delivery,delivery.replace(minute=38)),'MISSING')

    def test_early_preparation_aligns_quotes_not_historical_collection(self):
        self.assertEqual(seconds_until_window(NOW.replace(minute=20),'REQUEST_PREPARATION'),480)
        self.assertEqual(seconds_until_window(NOW,'REQUEST_PREPARATION'),0)
        self.assertEqual(seconds_until_window(NOW.replace(minute=20),'PREVIEW'),0)


class MarketSourceTests(unittest.TestCase):
    def raw(self):return json.loads((Path(__file__).parent/'fixtures/market-context-2026-11-04.json').read_text())

    def test_real_official_payloads_fill_all_six_required_market_items(self):
        context=parse_context(self.raw(),'2026-11-04')
        for name in ('TAIEX','TPEX','breadth','institutional_totals','margin_totals','futures_positioning'):
            self.assertEqual(context[name]['status'],'PASS',name)
        self.assertEqual(context['breadth']['advances'],438)
        self.assertEqual(context['margin_totals']['margin_change'],32079)
        self.assertEqual(context['futures_positioning']['foreign_net_contracts'],-93647)

    def test_malformed_optional_source_rows_do_not_hide_independent_market_data(self):
        raw=self.raw();raw['otc_margin']=['schema changed',None];raw['margin']['tables']=[None,{}]
        result=parse_context(raw,'2026-11-04')
        self.assertEqual(result['TAIEX']['status'],'PASS')
        self.assertEqual(result['TPEX']['status'],'PASS')
        self.assertNotEqual(result['margin_totals']['status'],'PASS')

    def test_old_latest_only_future_rows_do_not_fill_current_target(self):
        raw=self.raw()
        for r in raw['futures']:r['日期']='2026/11/03'
        self.assertNotEqual(parse_context(raw,'2026-11-04')['futures_positioning']['status'],'PASS')

    def test_futures_finmind_is_an_independent_exact_date_fallback(self):
        raw=self.raw();raw['futures']=[]
        raw['futures_fallback']=[{'date':'2026-11-04','futures_id':'TX','institutional_investors':'外資',
                                  'long_open_interest_balance_volume':11103,'short_open_interest_balance_volume':104750}]
        result=parse_context(raw,'2026-11-04')['futures_positioning']
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['foreign_net_contracts'],-93647)
        raw['futures_fallback'][0]['date']='2026-11-03'
        self.assertNotEqual(parse_context(raw,'2026-11-04')['futures_positioning']['status'],'PASS')

    def test_missing_table_and_reordered_columns_fail_safely(self):
        raw=self.raw();raw['margin']['tables']=[]
        self.assertNotEqual(parse_context(raw,'2026-11-04')['margin_totals']['status'],'PASS')
        raw=self.raw()
        raw['institutional']['fields'].reverse()
        for row in raw['institutional']['data']:row.reverse()
        self.assertEqual(parse_context(raw,'2026-11-04')['institutional_totals']['total_net_twd'],-160160345734)

    def test_otc_institutional_is_combined_once_and_conflicts_withhold_full_coverage(self):
        raw=self.raw()
        raw['otc_institutional']=[{'Date':'1151104','Investor':label,'Net':str(net)} for label,net in
            [('\\u3000外資及陸資(不含自營商)',-2240584579),('投信',-1836916910),('自營商合計',-565877109),('三大法人合計*',-4643378598),('\\u3000外資自營商',99)]]
        result=parse_context(raw,'2026-11-04')
        self.assertEqual(result['institutional_totals']['status'],'PASS')
        self.assertEqual(result['institutional_totals']['total_net_twd'],-164803724332)
        raw['otc_institutional'][3]['Net']='0'
        self.assertEqual(parse_context(raw,'2026-11-04')['institutional_totals']['status'],'PARTIAL_MARKET_COVERAGE')

    def test_otc_derived_breadth_excludes_etfs_and_credit_keeps_native_units(self):
        raw=self.raw()
        raw['otc_quotes']=[{'Date':'1151104','SecuritiesCompanyCode':c,'Change':v} for c,v in [('5483','+1'),('3707','-2'),('00679B','+3')]]
        raw['otc_margin']=[{'Date':'1151104','SecuritiesCompanyCode':'5483','MarginPurchaseBalance':'1234',
                           'MarginPurchaseBalancePreviousDay':'1200','ShortSaleBalance':'45','ShortSaleBalancePreviousDay':'40'}]
        result=parse_context(raw,'2026-11-04')
        self.assertEqual(result['breadth_by_market']['TPEx']['advances'],1)
        self.assertEqual(result['breadth_by_market']['TPEx']['declines'],1)
        self.assertEqual(result['margin_by_market']['TPEx']['margin_balance'],1234)
        self.assertEqual(result['margin_by_market']['TPEx']['margin_change'],34)

    def test_roc_dates_and_native_units(self):
        self.assertEqual(day('1151104'),'2026-11-04')
        self.assertIsNone(day('bad'))
        self.assertEqual(parse_context(self.raw(),'2026-11-04')['margin_totals']['margin_balance'],9514915)

    def test_us_close_fallback_selects_exact_symbol_date_and_close_case(self):
        checked=datetime(2026,11,4,8,32,tzinfo=TW)
        with patch('collect_cross_market.regular_close',return_value={'status':'MISSING'}),patch('collect_cross_market.finmind',return_value=[{'date':'2026-11-03','stock_id':'NVDA','Close':206.69}]):
            q=completed_us_close('NVDA',checked)
            self.assertEqual(q['status'],'PASS')
            self.assertEqual(q['price'],206.69)
            self.assertFalse(q['is_live'])
        with patch('collect_cross_market.regular_close',return_value={'status':'MISSING'}),patch('collect_cross_market.finmind',return_value=[{'date':'2026-11-02','stock_id':'NVDA','Close':100}]):
            self.assertEqual(completed_us_close('NVDA',checked)['status'],'MISSING')

    def test_current_security_master_never_reassigns_historical_position(self):
        class Response:
            def json(self):return {'0':{'ticker':'SPCX','title':'CURRENT ISSUER','cik_str':123}}
        with patch('regional_quotes.get',return_value=Response()):
            item=security_identity(NOW)['SPCX']
            self.assertEqual(item['status'],'VERIFIED_CURRENT_SECURITY')
            self.assertEqual(item['historical_position_mapping'],'NOT_VERIFIED_DO_NOT_REASSIGN')
