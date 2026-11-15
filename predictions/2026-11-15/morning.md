# 2026-11-15 morning public non-trading-day ledger
REPORT_ID: 2026-11-15-AM
PARENT_REPORT_ID: 2026-11-14-PM
SESSION: SUNDAY_TWSE_CLOSED
LAST_COMPLETED_TWSE_SESSION: 2026-11-13
NEXT_EXPECTED_TWSE_SESSION: 2026-11-16 (subject to exchange calendar)
DATA_REVISION_PIN: 2048caad1301e9f71fd4a94df6601ec27b93e2e6
DATA_SNAPSHOT_STATUS: 2026-11-15 morning.json not confirmed; no Taiwan regular session
PARENT_LEDGER_STATUS: VALID_THREE_BLOCKS
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_ID: OPEN-20261115-AM
OPEN_CENTER: N/A
OPEN_DELTA_POINTS: N/A
OPEN_DELTA_PERCENT: N/A
OPEN_RANGE: N/A
OPEN_CONFIDENCE: N/A
REFERENCE_LAST_CLOSE: 43675.12 (2026-11-13, provider from pinned parent ledger, not official-direct)
INPUT_CUTOFF: 2026-11-15T08:38:00+08:00
METHOD: No model calculation; Sunday TWSE closed
INPUTS: Pinned 2026-11-14 evening ledger; 2026-11-13 completed session provider close
OFFICIAL_VERIFICATION: No Sunday 09:00 TWSE open; not applicable
ELIGIBILITY: NON_TRADING_DAY_NOT_SCORED
NEW_FORMAL_PREDICTIONS: NONE
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-15-AM
OPEN_RECAP: OPEN-20261115-AM N/A; Sunday closed, no numerical error
ROLLING_5_20: NOT_AUDITED; n unknown, no fabricated accuracy
SCORE_100: N/A; retain weights 25/25/15/25/10
PARENT_REPORT: 2026-11-14-PM no new formal forecasts; original three blocks present
LAST_COMPLETED_TWSE: 2026-11-13 TAIEX 43675.12, +583.25 (+1.35%), provider as recorded in parent
SIX_CLOSES_2026_11_13: 0050=102.50;006208=235.05;00631L=31.92;2330=2350.00;3707=59.50;5483=162.50; historical same-session values from pinned parent, not Sunday quotes
CUTOFF_EXCEPTION: 2026-11-13 evening original generated 22:58:06 after 22:58 cutoff; later 23:32 artifact ineligible for original deadline
SOURCE_STATUS: No Sunday Taiwan/Japan/Korea regular-session observations expected; US Friday completed regular-session returns not independently checked this run
QUALITY_CHECK: NOT_EXECUTED; no current trading-day report draft
NEXT_CHECK: Monday 2026-11-16 pre-08:38 data publication, US Friday regular close, actual Japan/Korea 08:20+ valid observations, Taiwan 09:00 official open
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-15-AM","parent_report_id":"2026-11-14-PM","updated_at_taipei":"2026-11-15 08:44 scheduled execution (late)","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"predictions/2026-11-14/evening.md","observed_at":"2026-11-13","detail":"Semiconductor +1.23% vs TAIEX +1.35%; 811 up / 199 down; no Sunday trading"}],"change_reason":"No new Taiwan session, retain previous REJECT; not proof of fundamental improvement","next_check":"2026-11-16 semiconductor minus TAIEX return, breadth, TSMC institutional shares","falsifier":"Repeated material underperformance and deteriorating breadth would reopen WATCH"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"predictions/2026-11-14/evening.md","observed_at":"2026-11-13","detail":"00631L 31.92, margin +820 native lots, five-day -63024; no Sunday credit data"}],"change_reason":"No new credit evidence; cannot infer liquidation","next_check":"2026-11-16 exact-session 00631L price, credit balance and five-day change","falsifier":"Sustained price recovery with declining margin would weaken immediate credit-risk thesis"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"No audited 5/20 formal opening forecasts"},{"id":"CUTOFF-DEFECT","detail":"2026-11-13 evening original generated six seconds after cutoff; no retrospective qualification"}],"corrections_applied":[]}
[/RESEARCH_STATE]
