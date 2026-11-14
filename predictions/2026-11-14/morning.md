# 2026-11-14 morning non-trading-day public ledger
REPORT_ID: 2026-11-14-AM
PARENT_REPORT_ID: 2026-11-13-PM
SESSION: SATURDAY_TWSE_CLOSED
LAST_COMPLETED_TWSE_SESSION: 2026-11-13
NEXT_EXPECTED_TWSE_SESSION: 2026-11-16 (subject to exchange calendar)
DATA_PATH: reports/2026-11-13/evening.json
DATA_BLOB_SHA: 5d0305697d4ae1f0261ea8ccef0feed6c90bdef8
DATA_READINESS: DATA_PARTIAL (evening source; generation after 22:58 cutoff)
TODAY_MORNING_PACKAGE: MISSING (non-trading day)
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_ID: OPEN-20261114-AM
TARGET: 2026-11-14 TWSE official 09:00 TAIEX opening
CENTER: N/A; DELTA_POINTS: N/A; DELTA_PERCENT: N/A; RANGE: N/A; CONFIDENCE: N/A
REFERENCE_LAST_CLOSE: 43675.12 (2026-11-13; FinMind provider as recorded in parent ledger, not direct TWSE read)
REASON: SATURDAY_MARKET_CLOSED; no official opening exists.
INPUT_CUTOFF: 2026-11-14T08:38:00+08:00
INPUTS: 2026-11-13-PM parent ledger and 2026-11-13 evening bundle; no Saturday Asian equity open; no new Taiwan regular session.
METHOD: MARKET_CALENDAR_CLOSURE_CHECK; no numerical model run.
VERIFICATION_TIME: 2026-11-14T09:00:00+08:00 NOT_APPLICABLE_CLOSED
FORMAL_SAMPLE_ELIGIBLE: FALSE
NEW_FORMAL_PREDICTIONS: NONE
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-14-AM
PARENT_LEDGER_STATUS: VALID_THREE_BLOCKS
PARENT_PREDICTION_COUNT: 0
PREVIOUS_OPEN: OPEN-20261113-AM ABSTAIN_NUMERIC; no forecast error score.
ROLLING_5_20: NOT_AUDITED; no invented sample count, MAE or hit rate.
SCORE_100: N/A (25/25/15/25/10 retained).
LATEST_COMPLETED_MARKET: 2026-11-13 TAIEX close 43675.12, +1.35%; semiconductor +1.23%, relative -0.12pp; TWSE breadth 811 up/199 down.
SIX_CLOSES_2026_11_13: 0050=102.50;006208=235.05;00631L=31.92;2330=2350.00;3707=59.50;5483=162.50 (exact daily_ohlcv.data.close via deterministic close table).
PARENT_SOURCE_EXCEPTION: 2026-11-13 evening bundle generated 22:58:06 after 22:58 cutoff; TX Tick after cutoff; VIX delayed.
QUALITY_CHECK: NOT_EXECUTED; parent bundle close table used, not an automated draft check.
NEXT_CHECK: 2026-11-16 official trading calendar, completed Friday US regular close, valid Monday 08:20-08:38 Japan/Korea observations, Taiwan semiconductor relative return, breadth, 00631L credit.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-14-AM","parent_report_id":"2026-11-13-PM","updated_at_taipei":"2026-11-14 08:40","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"predictions/2026-11-13/evening.md","observed_at":"2026-11-13","detail":"Semiconductor +1.23% versus TAIEX +1.35%, -0.12pp; breadth 811 up/199 down"}],"change_reason":"Saturday no new TWSE session; no new evidence to revise Friday status","next_check":"2026-11-16 semiconductor return minus TAIEX and breadth","falsifier":"Repeated material underperformance with weakening breadth reopens WATCH"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"predictions/2026-11-13/evening.md","observed_at":"2026-11-13","detail":"00631L close 31.92, margin +820 native lots, five-day -63024"}],"change_reason":"No Saturday credit data; no claim of forced liquidation","next_check":"2026-11-16 00631L price and native-unit credit changes","falsifier":"Sustained recovery with reduced margin balances weakens near-term risk"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"Need original ex-ante numeric forecasts and independently checked official opens before scoring"},{"id":"CUTOFF-DEFECT","detail":"2026-11-13 evening bundle generated six seconds after cutoff; not retroactively qualified"}],"corrections_applied":[]}
[/RESEARCH_STATE]
