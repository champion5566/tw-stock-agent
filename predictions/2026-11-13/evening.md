# 2026-11-13 evening original public ledger
REPORT_ID: 2026-11-13-PM
PARENT_REPORT_ID: 2026-11-13-AM
DATA_PATH: reports/2026-11-13/evening.json
DATA_BLOB_SHA: 7361c0fb83f3236b4d50e42988674bc8c686730f
DATA_GENERATED_AT: 2026-11-13T22:58:06.339035+08:00
DATA_CUTOFF: 2026-11-13T22:58:00+08:00
DATA_READINESS: DATA_PARTIAL; generated six seconds after cutoff; TX Tick after cutoff; VIX delayed.
FORMAL_SAMPLE_ELIGIBLE: FALSE
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_PARENT_ID: OPEN-20261113-AM
OPEN_PARENT_ORIGINAL: CENTER N/A; DELTA_POINTS N/A; DELTA_PERCENT N/A; INTERVAL N/A; CONFIDENCE N/A_UNCALIBRATED; PRIOR_CLOSE 43091.87; DIRECTION ABSTAIN_NUMERIC; INPUT_GENERATED_AT 2026-11-13T08:28:18.685132+08:00.
OPEN_PARENT_ACTUAL_PROVIDER: 2026-11-13 TAIEX daily open 43719.75; +627.88 (+1.4571%) versus prior 43091.87; FinMind provider, not independent official TWSE 09:00 direct read.
OPEN_PARENT_RESULT: UNVERIFIABLE_NO_NUMERIC_FORECAST; no signed error, absolute error, direction or interval score.
PREVIOUS_PM: 2026-11-12-PM PREDICTION_COUNT 0; no matured numerical directional forecast.
NEW_FORMAL_PREDICTIONS: NONE. Next-session scenarios are unscored research checks, not trading calls.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-13-PM
PARENT_LEDGER_STATUS: VALID_THREE_BLOCKS
OPEN_RECAP: OPEN-20261113-AM ABSTAIN_NUMERIC; observed open 43719.75, +627.88 points (+1.46%) on FinMind daily data; forecast error and direction/interval unscoreable.
ROLLING_5_20: NOT_AUDITED; no invented n/5, n/20, MAE, hit or coverage statistics.
SCORE_100: N/A; original 25/25/15/25/10 weights unchanged.
MARKET: 2026-11-13 TAIEX open 43719.75 close 43675.12 versus previous 43091.87 (+583.25,+1.35%); TWSE breadth 811/199; TPEx 584/230. Semiconductor +1.23% versus TAIEX +1.35% (-0.12pp).
INSTITUTIONAL: TWSE+TPEx foreign +32626807640 TWD, trust +8643072606, dealer +7757670448, total +49027550694 TWD; TWSE and TPEx separately sourced.
CREDIT: TWSE margin +4891 native lots; TPEx +20074 native units; 00631L margin +820 native lots, five-day -63024; no automatic shares-to-lots conversion.
CLOSE_RECONCILIATION: 2026-11-13 daily_ohlcv.data.close 0050 102.50,006208 235.05,00631L 31.92,2330 2350.00,3707 59.50,5483 162.50; matched deterministic stock_close_table_markdown; not broker snapshot.
SOURCE_LIMITATIONS: Bundle generated 22:58:06 after cutoff, so not qualified as timely source. VIX bar 22:40 delayed 20m at target, 22:55 other US bars 5m at target; TX Shioaji Tick 22:58:05 after cutoff, 1m55s old at target, cannot qualify cutoff. At later completion, ages require recalculation. Japan/Korea completed-day observations are not live at 23:00. SPCX private mapping unverified.
QUALITY_CHECK: NOT_EXECUTED; six closes manually reconciled to exact-session daily fields. No automatic PASS.
NEXT_CHECK: 2026-11-16 semiconductor-minus-TAIEX return, TWSE breadth, 00631L margin and five-day balance, foreign flow, fresh US and TX observations.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-13-PM","parent_report_id":"2026-11-13-AM","updated_at_taipei":"2026-11-13 after 23:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"reports/2026-11-13/evening.json","observed_at":"2026-11-13","detail":"Semiconductor +1.23% versus TAIEX +1.35%, -0.12pp; TWSE breadth 811 up/199 down."}],"change_reason":"Single-day 0.12pp underperformance does not establish persistent weakness; prior rejection retained.","next_check":"2026-11-16 semiconductor daily return minus TAIEX, breadth and TSMC institutional net shares","falsifier":"Repeated material underperformance with weakening breadth reopens WATCH"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"reports/2026-11-13/evening.json","observed_at":"2026-11-13","detail":"00631L close 31.92 versus 30.99, margin +820 native lots, five-day margin -63024; TWSE margin +4891, TPEx +20074 native units."}],"change_reason":"One-day margin reaccumulation after substantial five-day decline; mixed evidence warrants monitoring, not forced-liquidation narrative.","next_check":"2026-11-16 00631L close, margin balance and five-day changes; TWSE and TPEx credit separately","falsifier":"Sustained price recovery with lower credit balances weakens near-term leverage risk"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"No ex-ante numeric open forecast; require official outcomes and audited originals before scoring"},{"id":"CUTOFF-DEFECT","detail":"Data bundle generated after 22:58 cutoff; investigate pipeline timing without retroactively qualifying source"}],"corrections_applied":[]}
[/RESEARCH_STATE]
