import unittest
from report_output_quality import check_close_table, render_close_table, render_us_regular_close_table


def bundle():
    return {'target_session_date':'2026-11-04','stocks':{
        code:{'daily_ohlcv':{'status':'PASS','source_date':'2026-11-04',
               'data':{'date':'2026-11-04','stock_id':code,'close':value}},
              'mcp_quote':{'price':999}}
        for code,value in [('006208',228.55),('00631L',30.85)]}}


class OutputQualityTests(unittest.TestCase):
    def test_actual_morning_price_mismatches_are_identified(self):
        text='| 代號 | 收盤 | 今日重點 |\n|---|---:|---|\n| 006208 | 229.20 | 觀察 |\n| 00631L | 31.23 | 風險 |'
        result=check_close_table(bundle(),text)
        self.assertEqual(result['status'],'FAIL')
        self.assertEqual([x['code'] for x in result['errors'] if x['reason'] == 'CLOSE_MISMATCH'], ['006208', '00631L'])
        self.assertEqual(len([x for x in result['errors'] if x['reason'] == 'REQUIRED_CLOSE_ROW_MISSING']), 4)

    def test_render_uses_daily_close_not_snapshot_or_model(self):
        text=render_close_table(bundle())
        self.assertIn('| 006208 | 228.55 |',text)
        self.assertNotIn('999',text)
        result=check_close_table(bundle(),text)
        self.assertEqual(result['errors'],[])
        self.assertEqual(result['status'],'PARTIAL')
        self.assertEqual(result['checked'],2)

    def test_missing_printed_value_when_source_exists_is_an_output_failure(self):
        text='| 代號 | 收盤 |\n|---|---:|\n| 006208 | N/A |'
        self.assertEqual(check_close_table(bundle(),text)['status'],'FAIL')

    def test_missing_five_rows_cannot_pass_when_one_close_matches(self):
        b = bundle()
        text = '| 代號 | 收盤 |\n|---|---:|\n| 006208 | 228.55 |'
        result = check_close_table(b, text)
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('00631L', [x['code'] for x in result['errors'] if x['reason'] == 'REQUIRED_CLOSE_ROW_MISSING'])

    def test_duplicate_close_row_fails(self):
        b = bundle()
        text = render_close_table(b) + '\n| 006208 | 228.55 |'
        result = check_close_table(b, text)
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('DUPLICATE_CLOSE_ROW', [x['reason'] for x in result['errors']])

    def test_us_regular_table_includes_dated_previous_close_and_return(self):
        b = {'scenario': 'morning', 'us_regular_close': {'SP500': {
            'status': 'PASS', 'change_status': 'PASS', 'session_completed': True,
            'previous_close': 7549.94, 'price': 7520.93, 'change_pct': -0.3842,
            'previous_source_date': '2026-11-09', 'source_date': '2026-11-10'}}}
        text = render_us_regular_close_table(b)
        self.assertIn('| SP500 | 2026-11-09 | 7549.94 | 2026-11-10 | 7520.93 | -0.38% |', text)
        self.assertIn('| SOX | N/A | N/A | N/A | N/A | N/A |', text)
        self.assertEqual(render_us_regular_close_table({'scenario': 'evening'}), '')

    def test_us_regular_table_rejects_missing_prior_session(self):
        b = {'scenario': 'morning', 'us_regular_close': {'SP500': {
            'status': 'PASS', 'change_status': 'PASS', 'session_completed': True,
            'previous_close': 7549.94, 'price': 7520.93, 'change_pct': -0.3842,
            'previous_source_date': None, 'source_date': '2026-11-10'}}}
        self.assertIn('| SP500 | N/A | N/A | N/A | N/A | N/A |', render_us_regular_close_table(b))

    def test_no_table_is_not_a_claim_of_successful_validation(self):
        self.assertEqual(check_close_table(bundle(),'no table')['status'],'NOT_CHECKED_NO_CLOSE_TABLE')

    def test_opening_forecast_table_not_treated_as_daily_close(self):
        text='| 代號 | 預測收盤 |\n|---|---:|\n| 006208 | 300 |'
        self.assertEqual(check_close_table(bundle(),text)['status'],'NOT_CHECKED_NO_CLOSE_TABLE')

    def test_wrong_session_cannot_supply_a_canonical_close(self):
        b=bundle();b['stocks']['006208']['daily_ohlcv']['source_date']='2026-11-03'
        result=check_close_table(b,'| 代號 | 收盤 |\n|---|---:|\n| 006208 | 228.55 |')
        self.assertEqual(result['errors'][0]['reason'],'NO_CURRENT_CANONICAL_CLOSE')


if __name__=='__main__':
    unittest.main()
