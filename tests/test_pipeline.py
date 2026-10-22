"""Contracts at collector/provider/storage boundaries; no remote data or credentials."""
import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

import collect_market
import collect_intraday
import collect_shioaji_night
import research_ledger
from quote_quality import (TW, daily_status, quote_status, select_observation,
                           select_stock_quote, shioaji_snapshot_time)
from shioaji_quotes import collect_quotes
from snapshot_io import write_snapshot

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 22, 11, 5, tzinfo=TW)


@contextlib.contextmanager
def in_directory(directory):
    previous = Path.cwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(previous)


class QualityContractTests(unittest.TestCase):
    def test_midnight_tick_is_live_but_future_day_is_not_prior_session(self):
        checked = NOW.replace(hour=0, minute=1)
        self.assertEqual(quote_status(100, checked-timedelta(minutes=2), checked), 'PASS')
        self.assertEqual(quote_status(100, checked+timedelta(days=1), checked), 'FUTURE_TIMESTAMP')

    def test_invalid_timestamp_and_daily_dates(self):
        self.assertIsNone(shioaji_snapshot_time(1e99))
        self.assertEqual(daily_status('2026-10-23', NOW.date()), 'FUTURE_TIMESTAMP')
        self.assertEqual(daily_status('2026-10-21', NOW.date()), 'PRIOR_SESSION')
        self.assertEqual(daily_status('bad', NOW.date()), 'FAIL')

    def test_fallback_does_not_inherit_mis_ohlc(self):
        mis = {'source':'TWSE_MIS', 'status':'NO_LAST_TRADE', 'open':100}
        fallback = {'source':'Shioaji_snapshot', 'status':'PASS', 'price':101}
        selected = select_stock_quote(mis, fallback)
        self.assertNotIn('open', selected)
        self.assertEqual(selected['mis_diagnostic'], mis)
        self.assertEqual(mis['status'], 'NO_LAST_TRADE')

    def test_iex_selection_does_not_inherit_yahoo_bar_clock(self):
        yahoo = {'open':100, 'latest_bar_at_taipei':'old', 'source':'Yahoo'}
        iex = {'status':'PASS', 'price':102, 'source':'IEX',
               'trade_time_utc':'2026-10-22T03:05:00Z', 'age_seconds':0}
        selected = select_observation(yahoo, iex)
        self.assertNotIn('open', selected)
        self.assertEqual(selected['latest_bar_at_taipei'], NOW.isoformat())
        self.assertEqual(selected['fallback_yahoo'], yahoo)


class SDKContractTests(unittest.TestCase):
    def fake_sdk(self, *, fail_wait=False, tick=True, fail_snap=False, fail_login=False):
        self.calls = []
        self.callback = None
        self.stock_callback = None
        def login(**kw):
            self.calls.append('login')
            if fail_login: raise RuntimeError('not logged')
        def set_callback(callback): self.callback = callback
        def set_stock_callback(callback): self.stock_callback = callback
        def snapshots(contracts):
            if fail_snap: raise ValueError('bad snapshot')
            # Epoch-like Taiwan wall clock from the observed SDK convention.
            return [NS(code='2330', ts=1792667100_000000000, close=100)]
        api = NS(login=login, logout=lambda:self.calls.append('logout'),
                 snapshots=snapshots,
                 Contracts=NS(Stocks={'2330':NS(code='2330')},
                              Futures=NS(TXF=NS(TXFR1=NS(code='TXF')))),
                 quote=NS(set_on_tick_fop_v1_callback=set_callback,
                          set_on_tick_stk_v1_callback=set_stock_callback,
                          subscribe=lambda *a,**k:self.calls.append('subscribe'),
                          unsubscribe=lambda *a,**k:self.calls.append('unsubscribe')))
        sdk = NS(Shioaji=lambda **kw:api,
                 constant=NS(QuoteType=NS(Tick='tick'),QuoteVersion=NS(v1='v1')))
        def wait(seconds):
            if fail_wait: raise RuntimeError('wait failed')
            if tick:
                self.callback(None, NS(close=46000, datetime=NOW.replace(tzinfo=None), volume=3))
        return sdk, wait

    def run_sdk(self, **options):
        sdk, wait = self.fake_sdk(**options)
        with patch.dict(os.environ, {'SHIOAJI_API_KEY':'test', 'SHIOAJI_SECRET_KEY':'test'}):
            return collect_quotes(('2330',), sdk=sdk, clock=lambda:NOW, wait=wait)

    def test_tick_quality_and_cleanup(self):
        result = self.run_sdk()
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['trade_time'], NOW.isoformat())
        self.assertEqual(result['stock_snapshots']['2330']['trade_time'], NOW.isoformat())
        self.assertEqual(result['stock_snapshots']['2330']['status'], 'PASS')
        self.assertEqual(self.calls, ['login','subscribe','subscribe','unsubscribe','unsubscribe','logout'])

    def test_stock_failure_does_not_discard_futures(self):
        result = self.run_sdk(fail_snap=True)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['stock_snapshots']['error_type'], 'ValueError')

    def test_no_ticks_and_exception_cleanup(self):
        self.assertEqual(self.run_sdk(tick=False)['status'], 'NO_TICKS_IN_WINDOW')
        self.assertEqual(self.run_sdk(fail_wait=True)['status'], 'ERROR')
        self.assertEqual(self.calls[-2:], ['unsubscribe', 'logout'])
        self.assertEqual(self.run_sdk(fail_login=True)['status'], 'ERROR')
        self.assertEqual(self.calls[-1], 'logout')

    def test_no_credentials_does_not_load_sdk(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(collect_quotes(sdk=object())['status'], 'NOT_CONFIGURED')


class CollectorIntegrationTests(unittest.TestCase):
    def test_market_missing_last_with_current_date_is_not_pass(self):
        def mcp(method, params, call_id):
            return {} if method=='initialize' else {'quotes':[{
                'date':'2026-10-22','time':'11:05:00','last':'-'}]}
        rows = [{'date':'2026-10-21','close':100,'Trading_Volume':1000}]
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp), \
             patch.object(collect_market, 'mcp', side_effect=mcp), \
             patch.object(collect_market, 'finmind', return_value=rows), \
             patch.object(collect_market, 'datetime') as dt, \
             patch.object(collect_market.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
            dt.now.return_value = NOW
            collect_market.main()
            result = json.loads(Path('out/2026-10-22/evening.json').read_text())
            self.assertEqual(result['coverage']['daily_available'], len(collect_market.STOCKS))
            self.assertEqual(result['coverage']['live_quotes'], 0)
            self.assertEqual(result['stocks']['2330']['mcp_quote']['status'], 'NO_LAST_TRADE')
            self.assertEqual(result['stocks']['2330']['daily_ohlcv']['history'], rows)

    def test_intraday_publishes_partial_and_explicit_missing(self):
        fallback = {'source':'Shioaji_snapshot','status':'PASS','price':100}
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp), \
             patch.object(collect_intraday, 'mis', side_effect=OSError), \
             patch.object(collect_intraday, 'shioaji', return_value={'stock_snapshots':{'2330':fallback}}), \
             patch.object(collect_intraday, 'now', return_value=NOW), contextlib.redirect_stdout(io.StringIO()):
            collect_intraday.main()
            result = json.loads(Path('out/2026-10-22/intraday.json').read_text())
            self.assertEqual(result['quotes']['0050']['status'], 'MISSING')
            self.assertEqual(result['quotes']['2330']['source'], 'Shioaji_snapshot')
            self.assertEqual(len(list(Path('out/2026-10-22/observations/intraday').glob('*.json'))), 1)

    def test_research_uses_collected_date_across_midnight(self):
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp), \
             patch.dict(os.environ, {'SOURCE_SNAPSHOT':'out/2026-10-21/evening.json'}), \
             contextlib.redirect_stdout(io.StringIO()):
            write_snapshot({'stocks':{}}, '2026-10-21', 'evening')
            research_ledger.main()
            self.assertTrue(Path('out/2026-10-21/research-evening.json').exists())

    def test_latest_and_immutable_storage(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = write_snapshot({'price':1}, '2026-10-22','intraday',tmp)
            write_snapshot({'price':2}, '2026-10-22','intraday',tmp)
            self.assertEqual(json.loads(first.read_text())['price'], 2)
            self.assertEqual(len(list(first.parent.glob('observations/intraday/*.json'))), 2)
            with self.assertRaises(ValueError):
                write_snapshot({'price':float('nan')}, '2026-10-22','intraday',tmp)


class PublisherIntegrationTests(unittest.TestCase):
    def git(self, *args, cwd):
        return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()

    def test_concurrent_publish_preserves_both_runs_and_cleans_worktrees(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); origin=root/'origin.git'; origin.mkdir()
            self.git('init','--bare',cwd=origin)
            seed=root/'seed'; self.git('clone',str(origin),str(seed),cwd=root)
            (seed/'seed.json').write_text('{}')
            self.git('add','.',cwd=seed)
            self.git('-c','user.name=test','-c','user.email=test@example.com','commit','-m','seed',cwd=seed)
            self.git('push','origin','HEAD:refs/heads/data/snapshots',cwd=seed)
            processes=[]; workspaces=[]
            for label in ['one','two','three']:
                workspace=root/label
                self.git('clone','--branch','data/snapshots',str(origin),str(workspace),cwd=root)
                (workspace/'out').mkdir()
                (workspace/'out'/f'{label}.json').write_text(json.dumps({'run':label}))
                workspaces.append(workspace)
                processes.append(subprocess.Popen(['bash',str(ROOT/'scripts/publish_snapshots.sh')],
                    env={**os.environ,'GITHUB_WORKSPACE':str(workspace)},
                    stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True))
            for proc in processes:
                output=proc.communicate(timeout=30)[0]
                self.assertEqual(proc.returncode,0,output)
            files=self.git('ls-tree','--name-only','data/snapshots',cwd=origin)
            for label in ['one','two','three']: self.assertIn(f'{label}.json',files)
            for workspace in workspaces:
                self.assertEqual(self.git('worktree','list','--porcelain',cwd=workspace).count('worktree '),1)


if __name__ == '__main__': unittest.main()


class ResearchIntegrationTests(unittest.TestCase):
    def test_backtest_executes_real_engine_from_old_dated_snapshot(self):
        import backtest_baseline
        from datetime import date
        rows=[]
        for i in range(180):
            price=100 + i/10 + (i % 60 - 30)/3
            rows.append({'date':(date(2025,1,1)+timedelta(days=i)).isoformat(),
                         'open':price,'max':price+1,'min':price-1,
                         'close':price,'Trading_Volume':1000})
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp), \
             patch.dict(os.environ, {'SOURCE_SNAPSHOT':'out/2026-10-21/evening.json'}), \
             contextlib.redirect_stdout(io.StringIO()):
            write_snapshot({'stocks':{'2330':{'daily_ohlcv':{'history':rows}}}},'2026-10-21','evening')
            backtest_baseline.main()
            result=json.loads(Path('out/2026-10-21/backtest-evening.json').read_text())
            stock=result['stocks']['2330']
            self.assertEqual(stock['status'],'EXPLORATORY_ONLY')
            self.assertIn('excess_return_pct_points',stock['holdout'])
            self.assertGreater(stock['holdout']['trades'],0)


class AlpacaContractTests(unittest.TestCase):
    def test_invalid_price_cannot_be_live(self):
        import alpaca_quotes
        payload={'NVDA':{'latestTrade':{'t':NOW.isoformat(),'p':float('inf')}}}
        with patch.dict(os.environ, {'ALPACA_API_KEY_ID':'test','ALPACA_API_SECRET_KEY':'test'}), \
             patch.object(alpaca_quotes,'urlopen') as urlopen, \
             patch.object(alpaca_quotes.json,'load',return_value=payload), \
             patch.object(alpaca_quotes,'datetime') as clock:
            clock.now.return_value=NOW
            clock.fromisoformat.side_effect=datetime.fromisoformat
            result=alpaca_quotes.fetch_iex_snapshots(['NVDA'])['quotes']['NVDA']
            self.assertEqual(result['status'],'NO_LAST_TRADE')
            self.assertIsNone(result['price'])
            self.assertFalse(result['is_live'])
