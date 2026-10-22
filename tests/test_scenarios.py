import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

import collect_intraday
from quote_quality import TW, select_stock_quote
from report_scenarios import build_report, render_markdown
from shioaji_quotes import tick_observation, collect_quotes
import test_pipeline
from test_pipeline import NOW, in_directory


def market_fixture():
    previous = {'date':'2026-10-21','open':100,'max':110,'min':95,'close':105,'Trading_Volume':1000}
    today = {**previous,'date':'2026-10-22','close':108}
    return {'stocks':{code:{key:{'status':'PASS','history':[previous,today]}
                      for key in ('daily_ohlcv','institutional','margin')}
                      for code in collect_intraday.STOCKS}}


class SourcePriorityTests(unittest.TestCase):
    def test_shioaji_wins_when_both_are_fresh(self):
        broker={'source':'Shioaji_tick','status':'PASS','price':101,'open':99}
        mis={'source':'TWSE_MIS','status':'PASS','price':100,'open':98}
        selected=select_stock_quote(broker,mis)
        self.assertEqual(selected['source'],'Shioaji_tick')
        self.assertEqual(selected['open'],99)
        self.assertFalse(selected['quote_selection']['fallback_used'])
        self.assertEqual(selected['source_observations']['fallback']['price'],100)

    def test_invalid_broker_falls_back_without_mixing_ohlc(self):
        selected=select_stock_quote({'source':'Shioaji_snapshot','status':'STALE','price':98,'high':200},
                                    {'source':'TWSE_MIS','status':'PASS','price':100})
        self.assertEqual(selected['source'],'TWSE_MIS')
        self.assertTrue(selected['quote_selection']['fallback_used'])
        self.assertNotIn('high',selected)

    def test_both_failed_keeps_explicit_failure(self):
        selected=select_stock_quote({'source':'Shioaji','status':'ERROR'},
                                    {'source':'TWSE_MIS','status':'NO_LAST_TRADE'})
        self.assertNotEqual(selected['status'],'PASS')
        self.assertIsNone(selected.get('price'))

    def test_actual_collector_selects_broker_even_when_mis_passes(self):
        broker={'source':'Shioaji_tick','status':'PASS','price':101,'data_kind':'tick', 'trade_time':NOW.isoformat()}
        mis={'source':'TWSE_MIS','status':'PASS','price':100}
        with tempfile.TemporaryDirectory() as directory, in_directory(directory), \
             patch.object(collect_intraday,'now',return_value=NOW), \
             patch.object(collect_intraday,'shioaji',return_value={'stock_quotes':{'2330':broker}}), \
             patch.object(collect_intraday,'mis',return_value={'2330':mis}), \
             contextlib.redirect_stdout(io.StringIO()):
            collect_intraday.main()
            result=json.loads(Path('out/2026-10-22/intraday.json').read_text())
        self.assertEqual(result['quotes']['2330']['source'],'Shioaji_tick')
        self.assertEqual(result['source_priority'][0],'Shioaji_tick')

    def test_indicative_auction_tick_is_rejected(self):
        self.assertIsNone(tick_observation(NS(close=100,datetime=NOW,simtrade=True),NOW,
                                          source='Shioaji_tick',units='TWD/share'))

    def test_stock_ticks_have_matching_ohlc(self):
        tick=NS(close=100,datetime=NOW,open=95,high=101,low=94,total_volume=123,volume=1)
        obs=tick_observation(tick,NOW,source='Shioaji_tick',units='TWD/share')
        self.assertEqual((obs['open'],obs['high'],obs['low'],obs['total_volume']),(95,101,94,123))
        self.assertEqual(obs['status'],'PASS')


class StreamSDKTests(unittest.TestCase):
    fake_sdk = test_pipeline.SDKContractTests.fake_sdk
    # Exercise the adapter itself with one stock stream and one futures stream.
    def test_stock_tick_preferred_to_single_snapshot(self):
        sdk, old_wait=self.fake_sdk()
        def wait(seconds):
            self.stock_callback(None,NS(code='2330',close=101,datetime=NOW,open=99,high=102,low=98))
            old_wait(seconds)
        with patch.dict('os.environ',{'SHIOAJI_API_KEY':'test','SHIOAJI_SECRET_KEY':'test'}):
            result=collect_quotes(('2330',),sdk=sdk,clock=lambda:NOW,wait=wait)
        self.assertEqual(result['stock_quotes']['2330']['source'],'Shioaji_tick')
        self.assertEqual(result['stock_quotes']['2330']['price'],101)
        self.assertEqual(result['stock_snapshots']['2330']['price'],100)
        self.assertFalse(result['stock_snapshots']['2330']['is_live'])
        self.assertEqual(self.calls.count('subscribe'),2)
        self.assertEqual(self.calls.count('unsubscribe'),2)


class ReportScenarioTests(unittest.TestCase):
    def test_0820_morning_excludes_same_day_close(self):
        report=build_report('morning',market_fixture(),checked_at=NOW.replace(hour=8,minute=20))
        self.assertEqual(report['target_session_date'],'2026-10-21')
        self.assertEqual(report['stocks']['2330']['daily_ohlcv']['data']['close'],105)
        self.assertEqual(report['status'],'COMPLETE')

    def test_2300_night_uses_today_but_never_old_institutional(self):
        market=market_fixture()
        for stock in market['stocks'].values():
            stock['institutional']['history'].pop()
        report=build_report('evening',market,checked_at=NOW.replace(hour=23,minute=0))
        self.assertEqual(report['stocks']['2330']['daily_ohlcv']['data']['close'],108)
        inst=report['stocks']['2330']['institutional']
        self.assertEqual(inst['status'],'MISSING_TARGET_SESSION')
        self.assertIsNone(inst['data'])
        self.assertEqual(inst['prior_reference']['date'],'2026-10-21')
        self.assertEqual(report['status'],'PARTIAL')

    def test_daytime_evening_preview_does_not_call_bar_a_close(self):
        report=build_report('evening',market_fixture(),checked_at=NOW,experiment=True)
        self.assertEqual(report['stocks']['2330']['daily_ohlcv']['status'],'SESSION_NOT_CLOSED')
        self.assertIsNone(report['stocks']['2330']['daily_ohlcv']['data'])
        self.assertFalse(report['point_in_time_verified'])
        self.assertIn('現時資料流程試跑',render_markdown(report))

    def test_intraday_stale_price_is_not_displayed_as_current(self):
        stale={'price':100,'source':'Shioaji_tick','data_kind':'tick','trade_time':(NOW-timedelta(hours=1)).isoformat()}
        report=build_report('intraday',intraday={'quotes':{'2330':stale}},checked_at=NOW)
        self.assertEqual(report['stocks']['2330']['status'],'STALE')
        self.assertIsNone(report['stocks']['2330']['price'])
        self.assertFalse(report['stocks']['2330']['is_live'])

    def test_snapshot_is_observation_not_live_tick(self):
        snap={'price':100,'source':'Shioaji_snapshot','data_kind':'snapshot','trade_time':NOW.isoformat()}
        report=build_report('intraday',intraday={'quotes':{'2330':snap}},checked_at=NOW)
        self.assertEqual(report['stocks']['2330']['status'],'PASS')
        self.assertFalse(report['stocks']['2330']['is_live'])


if __name__=='__main__': unittest.main()
