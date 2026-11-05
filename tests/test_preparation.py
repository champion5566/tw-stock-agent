import copy
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from quote_quality import TW
from test_pipeline import in_directory
from test_report_contract import fixture
from report_scenarios import build_report
from scripts.resolve_preparation import resolve
from scripts.publish_overlay import overlay
from scripts.reuse_night_observation import select


class PreparationTests(unittest.TestCase):
    def test_native_schedule_does_not_resubmit_request_at_head(self):
        now = datetime(2026, 11, 5, 9, 45, tzinfo=TW)
        path = 'preparation/requests/2026-11-05/morning.json'
        # The request can be old or absent locally; cron is not a new push.
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp):
            self.assertEqual(resolve({'schedule':'30 0 * * 1-5'},'schedule',now,[path]),
                             ('morning','SCHEDULED_PREPARATION'))
            self.assertEqual(resolve({'inputs':{'slot':'evening'}},'workflow_dispatch',now,[path]),
                             ('evening','PREVIEW'))

    def test_actual_push_still_rejects_stale_request(self):
        now = datetime(2026, 11, 5, 9, 45, tzinfo=TW)
        path = 'preparation/requests/2026-11-05/morning.json'
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp):
            Path(path).parent.mkdir(parents=True)
            Path(path).write_text(json.dumps({'schema_version':'preparation-request-v1',
                'slot':'morning','requested_at_taipei':'2026-11-05T08:21:54+08:00'}))
            with self.assertRaisesRegex(ValueError,'recent'):
                resolve({},'push',now,[path])

    def test_cutoff_rejects_postcutoff_asia_bar_despite_fresh_price(self):
        now, market, cross = fixture()
        cross['assets']['jp']['NIKKEI225']['latest_bar_at_taipei'] = now.replace(minute=39).isoformat()
        report = build_report('morning', market, cross=cross, checked_at=now)
        self.assertEqual(report['readiness']['sections']['asia_open']['items']['jp/NIKKEI225'], 'OBSERVATION_AFTER_CUTOFF')

    def test_late_evening_observations_are_cutoff_failures_not_clock_errors(self):
        now, market, cross = fixture('evening')
        cross['assets']['us']['NVDA']['latest_bar_at_taipei'] = now.replace(hour=23, minute=2).isoformat()
        cross['taifex']['shioaji_live_tx']['trade_time'] = now.replace(hour=23, minute=2).isoformat()
        report = build_report('evening', market, cross=cross, checked_at=now.replace(hour=23, minute=3))
        self.assertEqual(report['readiness']['sections']['us_intraday']['items']['NVDA'], 'OBSERVATION_AFTER_CUTOFF')
        self.assertEqual(report['readiness']['sections']['tx_live']['items']['TXFR1'], 'OBSERVATION_AFTER_CUTOFF')

    def test_collection_completion_not_start_decides_cutoff(self):
        now, market, cross = fixture()
        cross['collection_completed_at_taipei'] = now.replace(minute=39).isoformat()
        report = build_report('morning', market, cross=cross, checked_at=now.replace(minute=40))
        self.assertEqual(report['readiness']['sections']['cutoff']['items']['cross'], 'MISSING_OR_AFTER_CUTOFF')

    def test_no_collection_before_0820(self):
        now, market, cross = fixture()
        cross['fetched_at_taipei'] = now.replace(minute=19).isoformat()
        report = build_report('morning', market, cross=cross, checked_at=now)
        self.assertEqual(report['readiness']['sections']['cutoff']['items']['collection_window'], 'BEFORE_0820_OR_MISSING')
        with self.assertRaises(ValueError):
            resolve({'schedule':'30 0 * * 1-5'}, 'schedule', now.replace(minute=19))

    def test_request_validates_date_and_slot_without_evaluating_text(self):
        now = datetime(2026, 11, 5, 8, 20, tzinfo=TW)
        path = 'preparation/requests/2026-11-05/morning.json'
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp):
            Path(path).parent.mkdir(parents=True)
            request = {'schema_version':'preparation-request-v1', 'slot':'morning', 'requested_at_taipei':now.isoformat()}
            Path(path).write_text(json.dumps(request))
            self.assertEqual(resolve({}, 'push', now, [path]), ('morning', 'REQUEST_PREPARATION'))
            request['slot'] = 'evening; echo bad'
            Path(path).write_text(json.dumps(request))
            with self.assertRaises(ValueError): resolve({}, 'push', now, [path])
            request['slot'] = 'morning'
            request['requested_at_taipei'] = (now+timedelta(minutes=1)).isoformat()
            Path(path).write_text(json.dumps(request))
            with self.assertRaises(ValueError): resolve({}, 'push', now, [path])

    def test_late_retry_never_replaces_timely_package_and_is_archived(self):
        now, market, cross = fixture()
        report = build_report('morning', market, cross=cross, checked_at=now)
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp)/'source', Path(tmp)/'target'
            relative = Path('reports/2026-10-22/morning.json')
            path = source/relative
            path.parent.mkdir(parents=True)
            report['data_report_id'] = 'timely'
            path.write_text(json.dumps(report))
            overlay(source, target, now)
            late = copy.deepcopy(report)
            late['data_report_id'] = 'late'
            late['generated_at_taipei'] = now.replace(hour=9).isoformat()
            path.write_text(json.dumps(late))
            overlay(source, target, now.replace(hour=9))
            saved = json.loads((target/relative).read_text())
            self.assertEqual(saved['data_report_id'], 'timely')
            self.assertFalse(saved['formal_sample_eligible'])
            self.assertEqual(saved['publication_status'], 'PENDING_PUSH_AND_READBACK')
            self.assertEqual(len(list((target/relative.parent/'publication-observations/morning').glob('*.json'))), 2)

    def test_pre_push_delay_disqualifies_even_timely_generated_package(self):
        now, market, cross = fixture()
        report = build_report('morning', market, cross=cross, checked_at=now)
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp)/'source', Path(tmp)/'target'
            path = source/'reports/2026-10-22/morning.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(report))
            overlay(source, target, now.replace(minute=39))
            self.assertFalse(json.loads((target/path.relative_to(source)).read_text())['timing_eligible_at_publish_check'])

    def test_preserves_source_clock_and_rejects_day_session_for_night_reuse(self):
        now, _, cross = fixture()
        stored = {'fetched_at_taipei':now.replace(hour=6).isoformat(), 'taifex':cross['taifex']}
        result = select({}, stored, now)
        self.assertEqual(result['taifex']['shioaji_session_tx']['trade_time'], cross['taifex']['shioaji_session_tx']['trade_time'])
        stored['taifex']['shioaji_session_tx']['trade_time'] = now.replace(hour=9).isoformat()
        self.assertNotIn('completed_night_input', select({}, stored, now))

    def test_report_profile_skips_annual_finmind_history(self):
        import collect_cross_market as collector
        fake = {'status':'FAIL', 'error':'offline fixture'}
        with tempfile.TemporaryDirectory() as tmp, in_directory(tmp), patch.dict('os.environ', {'COLLECTION_PROFILE':'report','REPORT_SLOT':'evening'}), patch.object(collector, 'attempt', return_value=fake), patch.object(collector, 'finmind') as finmind:
            collector.main()
            finmind.assert_not_called()
            output = next(Path('out').glob('*/cross-evening.json'))
            self.assertEqual(json.loads(output.read_text())['history_profile'], 'report')
