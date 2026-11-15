# 2026-11-15 evening public non-trading-day ledger
REPORT_ID: 2026-11-15-PM
PARENT_REPORT_ID: 2026-11-15-AM
SESSION: SUNDAY_TWSE_CLOSED
LAST_COMPLETED_TWSE_SESSION: 2026-11-13
NEXT_EXPECTED_TWSE_SESSION: 2026-11-16 (subject to exchange calendar)
PARENT_LEDGER_STATUS: VALID_THREE_BLOCKS
DATA_SNAPSHOT_STATUS: 2026-11-15 evening.json NOT_FOUND (404); no Taiwan regular session
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_ID: OPEN-20261115-AM
ORIGINAL: CENTER N/A; DELTA_POINTS N/A; DELTA_PERCENT N/A; RANGE N/A; CONFIDENCE N/A; REFERENCE_LAST_CLOSE 43675.12 (2026-11-13 provider historical, not Sunday quote).
ORIGINAL_INPUT_CUTOFF: 2026-11-15T08:38:00+08:00
ORIGINAL_REASON: Sunday TWSE closed; no numeric forecast.
ACTUAL: No official Sunday 09:00 TWSE opening.
RESULT: UNVERIFIABLE_NOT_APPLICABLE_CLOSED; no signed error, absolute error, direction or range score.
PARENT_MORNING_PREDICTION_COUNT: 0
PRIOR_EVENING_2026_11_14: PREDICTION_COUNT 0; no matured scored thresholds.
NEW_FORMAL_PREDICTIONS: NONE. Monday scenarios are research checks only, not ex-ante scored calls.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-15-PM
ROLLING_5_20: NOT_AUDITED; n/5 and n/20 unknown, no invented MAE, direction or range coverage.
SCORE_100: N/A; weights retained 25/25/15/25/10.
LAST_COMPLETED_TWSE: 2026-11-13 TAIEX 43675.12, +583.25 (+1.35%), provider historical per parent.
SIX_CLOSES_2026_11_13: 0050=102.50;006208=235.05;00631L=31.92;2330=2350.00;3707=59.50;5483=162.50. Historical parent values, not newly verified against exact-session daily_ohlcv this run.
COVERAGE: Sunday no new Taiwan OHLCV, market breadth, institutions, credit, JP/KR regular session; Friday US completed close not independently rechecked.
US_QUOTES: Sunday 23:00 Taipei US regular market closed; no live regular quotes claimed.
TX_TICK: No <=10-minute verified true trade; UNKNOWN.
SOURCE_CUTOFF_EXCEPTION: 2026-11-13 original evening bundle generated 22:58:06, after 22:58 cutoff; no retrospective qualification.
QUALITY_CHECK: report_output_quality.py NOT_EXECUTED; no Sunday current-session close table.
DATA_PACKAGE: reports/2026-11-15/evening.json NOT_FOUND at branch data/snapshots; no claim of successful publication.
NEXT_CHECK: 2026-11-16 morning source timeliness, completed Friday US session, valid Japan/Korea observations, Taiwan official opening, semiconductor relative performance and credit.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-15-PM","parent_report_id":"2026-11-15-AM","updated_at_taipei":"2026-11-15 22:55 scheduled execution; before 23:00 target","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"predictions/2026-11-15/morning.md","observed_at":"2026-11-13","detail":"Semiconductor +1.23% vs TAIEX +1.35%; 811 up / 199 down; Sunday no Taiwan session"}],"change_reason":"No new Taiwan trading evidence; maintain parent REJECT","next_check":"2026-11-16 semiconductor minus TAIEX return, breadth and 2330 institutional shares","falsifier":"Repeated material semiconductor underperformance with weakening breadth reopens WATCH"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"predictions/2026-11-15/morning.md","observed_at":"2026-11-13","detail":"00631L 31.92, margin +820 native lots, five-day -63024; Sunday no credit observation"}],"change_reason":"No new same-session credit evidence; do not infer forced liquidation","next_check":"2026-11-16 exact-session 00631L price and margin balances with five-day change","falsifier":"Sustained recovery and declining credit balances weaken near-term risk"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"5/20 formally eligible opening forecasts not audited; n unknown"},{"id":"CUTOFF-DEFECT","detail":"2026-11-13 original evening package generated 22:58:06, six seconds after cutoff; not retroactively eligible"}],"corrections_applied":[]}
[/RESEARCH_STATE]
