import unittest
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT=Path(__file__).resolve().parents[1]


class WorkflowContracts(unittest.TestCase):
    def test_all_workflows_parse_and_keep_existing_schedules(self):
        workflows={p.stem:yaml.safe_load(p.read_text()) for p in (ROOT/'.github/workflows').glob('*.yml')}
        # PyYAML YAML 1.1 parses unquoted `on` as True.
        def triggers(name): return workflows[name].get('on',workflows[name].get(True))
        self.assertEqual([x['cron'] for x in triggers('market-data')['schedule']],
                         ['25 0 * * 1-5','40 12 * * 1-5'])
        self.assertEqual([x['cron'] for x in triggers('cross-market')['schedule']],
                         ['35 21 * * 1-5','30 0 * * 1-5','45 14 * * 1-5'])
        self.assertIn('workflow_dispatch',triggers('intraday-on-demand'))

    def test_research_is_separate_from_published_ingestion(self):
        workflow=yaml.safe_load((ROOT/'.github/workflows/market-data.yml').read_text())
        jobs=workflow['jobs']
        self.assertEqual(jobs['research']['needs'],'snapshot')
        ingestion='\n'.join(step.get('run','') for step in jobs['snapshot']['steps'])
        self.assertIn('publish_snapshots.sh',ingestion)
        self.assertNotIn('backtest_baseline.py',ingestion)
        research='\n'.join(step.get('run','') for step in jobs['research']['steps'])
        self.assertIn('SOURCE_SNAPSHOT',research)
        self.assertIn('backtest_baseline.py',research)
