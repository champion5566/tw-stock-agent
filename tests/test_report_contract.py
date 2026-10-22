import copy
import contextlib
import io
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

import pandas as pd
import collect_cross_market
import report_scenarios
from instruments import STOCKS, REPORT_STOCKS, WATCH_STOCKS
from quote_quality import TW
from report_contract import US_REQUIRED, ASIA_REQUIRED, DELIVERY_TIMES, CUTOFF_TIMES
from session_calendar import completed_session
from stock_metrics import metrics, flows
from test_pipeline import in_directory
from shioaji_quotes import collect_quotes


def fixture(mode='morning'):
    checked = datetime(2026, 10, 22, 8, 42, tzinfo=TW) if mode == 'morning' else datetime(2026, 10, 22, 22, 56, tzinfo=TW)
    target = '2026-10-21' if mode == 'morning' else '2026-10-22'
    rows=[]
    for index, day in enumerate(pd.bdate_range(end=target, periods=25)):
        rows.append({'date':day.date().isoformat(), 'open':100,'max':105,'min':99,'close':102,
                     'Trading_Volume':1000+index, 'Trading_money':100000+index,
                     'Foreign_Investor_buy':10,'Foreign_Investor_sell':5,
                     'Foreign_Dealer_Self_buy':0,'Foreign_Dealer_Self_sell':0,
                     'Investment_Trust_buy':3,'Investment_Trust_sell':1,
                     'Dealer_self_buy':4,'Dealer_self_sell':1,
                     'Dealer_Hedging_buy':2,'Dealer_Hedging_sell':1,
                     'Dealer_buy':0,'Dealer_sell':0,
                     'MarginPurchaseTodayBalance':20,'MarginPurchaseYesterdayBalance':19,
                     'ShortSaleTodayBalance':1,'ShortSaleYesterdayBalance':1})
    market={'fetched_at_taipei':checked.replace(hour=8,minute=25).isoformat() if mode=='morning' else checked.replace(hour=22,minute=15).isoformat(),
            'stocks':{code:{key:{'status':'PASS','history':rows} for key in ('daily_ohlcv','institutional','margin')} for code in STOCKS},
            'market_context':{}}
    context_fields={'TAIEX':('open','high','low','close','volume','turnover'),
                    'TPEX':('open','high','low','close','volume','turnover'),
                    'breadth':('advances','declines'),
                    'institutional_totals':('foreign_net_twd','trust_net_twd','dealer_net_twd','total_net_twd'),
                    'margin_totals':('margin_balance','margin_change','short_balance','short_change'),
                    'futures_positioning':('foreign_net_contracts',)}
    for name, keys in context_fields.items():
        market['market_context'][name]={'status':'PASS','source_date':target,**{key:1 for key in keys}}
    cross={'fetched_at_taipei':checked.replace(minute=38 if mode=='morning' else 52).isoformat(),
           'assets':{'us':{}}, 'taifex':{}, 'us_regular_close':{}}
    for area,names in ASIA_REQUIRED.items():
        cross['assets'][area]={name:{'price':100,'status':'PASS','latest_bar_at_taipei':checked.replace(hour=8,minute=40).isoformat()}
                               for name in names}
    for name in US_REQUIRED:
        cross['us_regular_close'][name]={'price':100,'source_date':'2026-10-21','session_completed':True,'status':'PASS'}
        cross['assets']['us'][name]={'price':100,'status':'PASS','latest_bar_at_taipei':checked.replace(hour=22,minute=50).isoformat()}
    cross['taifex']['shioaji_session_tx']={'price':40000,'data_kind':'snapshot','trade_time':checked.replace(hour=4,minute=59,second=59).isoformat()}
    cross['taifex']['shioaji_live_tx']={'price':40000,'data_kind':'tick','trade_time':checked.replace(hour=22,minute=55).isoformat()}
    return checked, market, cross


class CalendarAndRequirementTests(unittest.TestCase):
    def test_real_report_list_is_six_and_observations_are_separate(self):
        self.assertEqual(set(REPORT_STOCKS),{'0050','006208','00631L','2330','3707','5483'})
        self.assertTrue(set(REPORT_STOCKS).issubset(STOCKS))
        self.assertFalse(set(REPORT_STOCKS).intersection(WATCH_STOCKS))
        self.assertEqual(DELIVERY_TIMES['morning'].isoformat(),'08:50:00')

    def test_weekend_and_us_holiday_calendar(self):
        monday=datetime(2026,10,26,8,50,tzinfo=TW)
        self.assertEqual(completed_session('XTAI',monday)['date'],'2026-10-23')
        independence_day=datetime(2026,7,6,8,50,tzinfo=TW)
        self.assertEqual(completed_session('XNYS',independence_day)['date'],'2026-07-02')

    def test_us_daylight_saving_not_fixed_utc_hour(self):
        summer=completed_session('XNYS',datetime(2026,10,22,8,45,tzinfo=TW))
        winter=completed_session('XNYS',datetime(2026,11,5,8,45,tzinfo=TW))
        self.assertEqual(datetime.fromisoformat(summer['closed_at']).hour,20)
        self.assertEqual(datetime.fromisoformat(winter['closed_at']).hour,21)

    def test_yahoo_regular_close_excludes_current_open_session(self):
        checked=datetime(2026,10,22,23,0,tzinfo=TW)
        history=pd.DataFrame({'Close':[100,110]},index=pd.to_datetime(['2026-10-21','2026-10-22']).tz_localize('America/New_York'))
        with patch.object(collect_cross_market.yf,'Ticker') as ticker:
            ticker.return_value.history.return_value=history
            result=collect_cross_market.regular_close('NVDA',checked)
            self.assertEqual(result['price'],100)
            self.assertEqual(result['source_date'],'2026-10-21')
            self.assertFalse(ticker.return_value.history.call_args.kwargs['prepost'])
            self.assertFalse(result['is_formal_close'])


class ReadinessTests(unittest.TestCase):
    def report(self, mode='morning'):
        checked, market, cross=fixture(mode)
        return report_scenarios.build_report(mode,market,cross=cross,checked_at=checked),market,cross,checked

    def test_full_sections_ready_does_not_ack_delivery_or_ledger(self):
        report,_,_,_=self.report()
        self.assertEqual(report['status'],'DATA_READY')
        self.assertEqual(report['delivery_status'],'NOT_ACKNOWLEDGED')
        self.assertEqual(report['readiness']['parent_ledger_status'],'NOT_CHECKED')
        self.assertEqual(report['stocks']['006208']['role'],'report_required')
        self.assertEqual(report['stocks']['2313']['role'],'watch_only')
        self.assertFalse(report['futures']['TXFR1']['is_live'])

    def test_all_stocks_complete_is_not_full_report_ready(self):
        checked,market,cross=fixture()
        report=report_scenarios.build_report('morning',market,checked_at=checked)
        self.assertEqual(report['stock_data_status'],'COMPLETE')
        self.assertEqual(report['status'],'DATA_PARTIAL')
        self.assertEqual(report['readiness']['sections']['us_regular_close']['status'],'PARTIAL')

    def test_old_data_cannot_redefine_expected_session(self):
        checked,market,cross=fixture()
        for stock in market['stocks'].values():
            stock['daily_ohlcv']['history']=stock['daily_ohlcv']['history'][:-1]
        report=report_scenarios.build_report('morning',market,cross=cross,checked_at=checked)
        self.assertEqual(report['target_session_date'],'2026-10-21')
        self.assertEqual(report['stocks']['2330']['daily_ohlcv']['status'],'MISSING_TARGET_SESSION')
        self.assertEqual(report['status'],'DATA_PARTIAL')

    def test_proxy_not_accepted_as_actual_topix(self):
        checked,market,cross=fixture()
        cross['assets']['jp']['TOPIX_ETF_PROXY']=cross['assets']['jp'].pop('TOPIX')
        report=report_scenarios.build_report('morning',market,cross=cross,checked_at=checked)
        self.assertEqual(report['readiness']['sections']['asia_open']['items']['jp/TOPIX'],'MISSING')
        self.assertEqual(report['status'],'DATA_PARTIAL')

    def test_night_quotes_evaluated_at_2300_not_at_2252_capture(self):
        checked,market,cross=fixture('evening')
        cross['taifex']['shioaji_live_tx']['trade_time']=checked.replace(minute=45).isoformat()
        report=report_scenarios.build_report('evening',market,cross=cross,checked_at=checked)
        self.assertNotEqual(report['readiness']['sections']['tx_live']['status'],'PASS')

    def test_cutoff_violation_is_visible(self):
        checked,market,cross=fixture()
        report=report_scenarios.build_report('morning',market,cross=cross,checked_at=checked.replace(minute=46))
        self.assertEqual(report['readiness']['sections']['cutoff']['items']['generation'],'AFTER_CUTOFF')
        self.assertEqual(report['status'],'DATA_PARTIAL')

    def test_missing_turnover_and_credit_are_not_zero_filled(self):
        checked,market,cross=fixture()
        for code in REPORT_STOCKS:
            stock=copy.deepcopy(market['stocks'][code])
            del stock['daily_ohlcv']['history'][-1]['Trading_money']
            market['stocks'][code]=stock
        report=report_scenarios.build_report('morning',market,cross=cross,checked_at=checked)
        self.assertIsNone(report['stocks']['2330']['metrics']['turnover_twd'])
        self.assertEqual(report['status'],'DATA_PARTIAL')

    def test_broker_snapshot_must_be_near_actual_completed_night_end(self):
        checked,market,cross=fixture()
        cross['taifex']['shioaji_session_tx']['trade_time']=checked.replace(hour=8,minute=30).isoformat()
        report=report_scenarios.build_report('morning',market,cross=cross,checked_at=checked)
        self.assertEqual(report['readiness']['sections']['tx_completed_night']['status'],'PARTIAL')

    def test_dealer_aggregate_is_not_double_counted(self):
        row={'Foreign_Investor_buy':10,'Foreign_Investor_sell':2,
             'Foreign_Dealer_Self_buy':0,'Foreign_Dealer_Self_sell':0,'Investment_Trust_buy':4,'Investment_Trust_sell':1,
             'Dealer_self_buy':5,'Dealer_self_sell':1,'Dealer_Hedging_buy':3,'Dealer_Hedging_sell':2,
             'Dealer_buy':5,'Dealer_sell':0}
        result=flows(row)
        self.assertEqual(result['dealer_net_shares'],5)
        self.assertEqual(result['total_net_shares'],16)
        row['Dealer_buy']=99
        self.assertTrue(flows(row)['dealer_components_conflict'])
        self.assertIsNone(flows(row)['total_net_shares'])

    def test_aftermarket_single_snapshot_requires_no_subscription_or_wait(self):
        snap=NS(ts=datetime(2026,10,22,4,59,59,tzinfo=timezone.utc).timestamp()*1e9, close=40000)
        api=NS(login=lambda **kwargs:None, logout=lambda:None, snapshots=lambda contracts:[snap],
               Contracts=NS(Futures=NS(TXF=NS(TXFR1=NS(code='TXFR1')))))
        sdk=NS(Shioaji=lambda **kwargs:api,constant=NS(QuoteType=NS(Tick='Tick'),QuoteVersion=NS(v1='v1')))
        with patch.dict(os.environ,{'SHIOAJI_API_KEY':'test','SHIOAJI_SECRET_KEY':'test'}):
            result=collect_quotes(future_snapshot=True,stream=False,sdk=sdk,
                clock=lambda:datetime(2026,10,22,8,38,tzinfo=TW), wait=lambda seconds:self.fail('Must not wait'))
        self.assertEqual(result['data_kind'],'snapshot')
        self.assertEqual(result['price'],40000)
        self.assertFalse(result['is_live'])
        self.assertEqual(result['trade_time'],'2026-10-22T04:59:59+08:00')


if __name__=='__main__': unittest.main()
