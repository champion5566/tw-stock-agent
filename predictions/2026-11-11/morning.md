# 2026-11-11 morning original public ledger
REPORT_ID: 2026-11-11-AM
PARENT_REPORT_ID: 2026-11-10-PM
DATA_PATH: reports/2026-11-11/morning.json
DATA_BLOB_SHA: baa003acf3877c23f57028a62aedf2519aafabe3
DATA_GENERATED_AT: 2026-11-11T08:28:17.169048+08:00
DATA_CUTOFF: 2026-11-11T08:38:00+08:00
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 1
PREDICTION_ID: OPEN-20261111-AM
TARGET: TWSE TAIEX official 2026-11-11 09:00 opening index
PRIOR_CLOSE: 42711.92 (2026-11-10 TWSE)
CENTER: N/A
DELTA_POINTS: N/A
DELTA_PERCENT: N/A
INTERVAL: N/A
CONFIDENCE: N/A_UNCALIBRATED
DIRECTION: ABSTAIN_NUMERIC
METHOD: No reproducible calibrated cash-open model; no conversion of completed TX night snapshot into cash opening.
INPUTS: 2026-11-10 TAIEX close 42711.92; US completed regular session 2026-11-10 SP500 -0.3842%, NASDAQ -0.7416%, SOX -0.3548%, TSM +2.0225%, NVDA -5.4738%; TXFR1 42522 at 2026-11-11T04:59:58.955+08:00; JP TOPIX +0.56%, ADVANTEST -0.42%, TOKYO_ELECTRON +0.19% at 08:27; KR KOSPI -0.25%, SAMSUNG -0.40%, SK_HYNIX -0.74% at 08:28; NIKKEI 08:12 STALE.
INPUT_PACKAGE_GENERATED_AT: 2026-11-11T08:28:17.169048+08:00
INPUT_CUTOFF: 2026-11-11T08:38:00+08:00
VERIFY_AT: 2026-11-11T09:00:00+08:00 via official TWSE 09:00 opening index
FORMAL_SAMPLE: NO_NUMERIC_FORECAST
INVALIDATION: N/A; abstention
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-11-AM
PARENT_REPORT_ID: 2026-11-10-PM
PARENT_PREDICTION_COUNT: 0
PARENT_OPEN_RESULT: OPEN-20261110-AM provider daily open 42130.33; official 09:00 direct match unverified; original forecast N/A; UNSCOREABLE.
ROLLING_5_20: N/A_NOT_AUDITED
SCORE_100_WEIGHTS: 25/25/15/25/10
SCORE_100: N/A_NO_SETTLED_COMPARABLE_FORECAST
DATA_READINESS: DATA_PARTIAL
DATA_EXCEPTION: NIKKEI225 08:12 DELAYED; TOPIX, Advantest, Tokyo Electron, KOSPI, Samsung, SK Hynix valid at 08:27-08:28.
SOURCE_NOTE: US regular daily closes only; TXFR1 completed night 04:59:58 snapshot not current or certified settlement; no inferred spot-futures basis.
QUALITY_CHECK: NOT_EXECUTED; six displayed closes manually checked against same-session daily_ohlcv.data.close and stock_close_table_markdown.
NEXT_CHECK: 2026-11-11 09:00 official open, then close semiconductor relative performance, breadth, ETF margin.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-11-AM","parent_report_id":"2026-11-10-PM","updated_at_taipei":"2026-11-11T08:38:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"reports/2026-11-10/evening.json","observed_at":"2026-11-10","detail":"Taiwan semiconductor +2.66% versus TAIEX +2.52%; electronics components +6.75%."},{"source":"reports/2026-11-11/morning.json","observed_at":"2026-11-11 08:28","detail":"US SOX -0.35%, NVDA -5.47%, TSM +2.02%; Asia semiconductors mixed to soft."}],"change_reason":"Maintain prior rejection of persistent Taiwan relative weakness; overnight external softness raises a fresh test, not proof of domestic relative weakness.","next_check":"2026-11-11 Taiwan semiconductor sector return minus TAIEX return and TWSE breadth at close","falsifier":"Repeated Taiwan semiconductor underperformance versus TAIEX with deteriorating breadth"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"reports/2026-11-10/evening.json","observed_at":"2026-11-10","detail":"00631L margin -29393 provider-native lots as price rose; 0050 margin -3559; TWSE margin -57360."}],"change_reason":"Balance reduction with price recovery eases near-term pressure, but does not establish systemic deleveraging or forced liquidations.","next_check":"2026-11-11 close 00631L/0050 prices and provider-native margin changes","falsifier":"Sustained price strength with falling credit exposure"}],"pending_checks":[],"corrections_applied":[{"id":"AM-1105-TIME","evidence":"TX 04:59 observation explicitly predates JP/KR 08:27-08:28"},{"id":"AM-1105-CHANGE","evidence":"US regular daily close-to-close returns shown from same provider"},{"id":"AM-1105-COVERAGE","evidence":"Nikkei delayed but TOPIX and Japanese semiconductor quotes retained"}]}
[/RESEARCH_STATE]
