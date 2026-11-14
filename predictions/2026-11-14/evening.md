# 2026-11-14 evening public non-trading-day ledger
REPORT_ID: 2026-11-14-PM
PARENT_REPORT_ID: 2026-11-14-AM
SESSION: SATURDAY_TWSE_CLOSED
LAST_COMPLETED_TWSE_SESSION: 2026-11-13
NEXT_EXPECTED_TWSE_SESSION: 2026-11-16 (subject to exchange calendar)
DATA_REVISION_PIN: 7f17f706bad2deb3c1320ecd2d323d003172e726
DATA_SNAPSHOT_STATUS: 2026-11-14 evening.json MISSING; non-trading day
PARENT_LEDGER_STATUS: VALID_THREE_BLOCKS
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_PARENT_ID: OPEN-20261114-AM
OPEN_PARENT_ORIGINAL: CENTER N/A; DELTA_POINTS N/A; DELTA_PERCENT N/A; RANGE N/A; CONFIDENCE N/A; REFERENCE_LAST_CLOSE 43675.12 (2026-11-13 provider); INPUT_CUTOFF 2026-11-14T08:38:00+08:00; REASON SATURDAY_MARKET_CLOSED.
OPEN_PARENT_ACTUAL: NO_OFFICIAL_09_00_OPEN_ON_SATURDAY
OPEN_PARENT_RESULT: UNVERIFIABLE_NOT_APPLICABLE_CLOSED; no signed/absolute error, direction or interval score.
PARENT_MORNING_PREDICTION_COUNT: 0
PREVIOUS_PM: 2026-11-13-PM PREDICTION_COUNT 0; no matured numerical close thresholds.
NEW_FORMAL_PREDICTIONS: NONE. Next trading-day scenarios are research checks, not scored calls.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-14-PM
OPEN_RECAP: OPEN-20261114-AM NO_FORECAST; Saturday TWSE closed; not a formal sample.
ROLLING_5_20: NOT_AUDITED; n/5 and n/20 unknown; no MAE/direction/interval figures.
SCORE_100: N/A; existing 25/25/15/25/10 weights retained.
LATEST_COMPLETED_TWSE: 2026-11-13 TAIEX close 43675.12, +583.25 (+1.35%), provider data as recorded in original parent ledger.
SIX_CLOSES_2026_11_13: 0050=102.50;006208=235.05;00631L=31.92;2330=2350.00;3707=59.50;5483=162.50. Historical exact-session daily close table in 2026-11-13 parent, not Saturday prices.
DATA_EXCEPTION: 2026-11-14 evening.json absent as expected for Saturday; no current Taiwan OHLCV/institutional/credit; do not substitute Friday prices as Saturday.
SOURCE_CUTOFF_EXCEPTION: 2026-11-13 original bundle generated 22:58:06 after cutoff; original ledger retained. Later 23:32 bundle is not ex-ante eligible.
US_QUOTES: Saturday 23:00 Taipei is Saturday 10:00 ET; US regular market closed. No live regular-session quote claims.
TX_TICK: No verified <=10m actual trade; UNKNOWN.
QUALITY_CHECK: NOT_EXECUTED; no current-session six-stock closes to reconcile.
NEXT_CHECK: 2026-11-16 completed Friday US session, Taiwan market breadth, semiconductor relative return, 00631L margin, exact data timing and output quality.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-14-PM","parent_report_id":"2026-11-14-AM","updated_at_taipei":"2026-11-14 23:00 scheduled target; execution before target","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"predictions/2026-11-13/evening.md","observed_at":"2026-11-13","detail":"Semiconductor +1.23% vs TAIEX +1.35%; stock breadth 811 up / 199 down; no Saturday TWSE session"}],"change_reason":"No new Taiwan regular-session evidence on Saturday; retain parent status","next_check":"2026-11-16 semiconductor minus TAIEX return, breadth and TSMC institutional shares","falsifier":"Repeated material semiconductor underperformance accompanied by deteriorating breadth reopens WATCH"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"predictions/2026-11-13/evening.md","observed_at":"2026-11-13","detail":"00631L 31.92, margin +820 native lots, five-day -63024; no Saturday credit observations"}],"change_reason":"No new Taiwan credit data; no evidence of forced liquidation","next_check":"2026-11-16 00631L exact-session price, credit balance and 5-day change","falsifier":"Sustained recovery with falling margin balances weakens near-term credit risk"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"Historical 5/20 eligible numeric opens not audited; do not infer n=0 from unreviewed files"},{"id":"CUTOFF-DEFECT","detail":"2026-11-13 original evening bundle generated 22:58:06 after cutoff; later republished bundle generated 23:32 is also not eligible for original cutoff"}],"corrections_applied":[]}
[/RESEARCH_STATE]
