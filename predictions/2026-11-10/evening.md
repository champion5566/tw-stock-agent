# 2026-11-10 evening original public ledger
REPORT_ID: 2026-11-10-PM
PARENT_REPORT_ID: 2026-11-10-AM
DATA_PATH: reports/2026-11-10/evening.json
DATA_BLOB_SHA: 79444182fdabb59ecb4bc71c68b828fdd5dcc625
DATA_GENERATED_AT: 2026-11-10T22:54:11.530051+08:00
DATA_READINESS: DATA_PARTIAL; VIX 22:35 DELAYED at 23:00, STALE after 23:05
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_PARENT_ID: OPEN-20261110-AM
OPEN_PARENT_ORIGINAL: CENTER N/A; DELTA_POINTS N/A; DELTA_PERCENT N/A; INTERVAL N/A; CONFIDENCE N/A_UNCALIBRATED; PRIOR_CLOSE 41661.70; DIRECTION ABSTAIN_NUMERIC; DATA_GENERATED_AT 08:28:15.
NO_NEW_SCORED_FORECAST: TRUE
DIRECTION: ABSTAIN
VERIFICATION: NOT_APPLICABLE
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
OPEN_ID: OPEN-20261110-AM
OPEN_ACTUAL_PROVIDER: 42130.33; +468.63 points / +1.12485% versus 41661.70, FinMind same-day TAIEX daily open; official 09:00 direct retrieval not independently established.
OPEN_RESULT: UNVERIFIABLE_NO_NUMERIC_FORECAST; no signed/absolute error, direction or interval score.
ROLLING_5_20: N/A_NOT_AUDITED; do not invent sample counts.
PARENT_PREDICTIONS: 1 open abstention; no HIT/MISS.
PREVIOUS_PM: 2026-11-09-PM PREDICTION_COUNT 0.
SCORE_100: N/A; original weights 25/25/15/25/10 unchanged.
MARKET: TAIEX 42711.92 +1050.22 (+2.52%); semiconductor +2.66%, electronics components +6.75%; TWSE breadth 526/491; TPEx breadth 451/360.
INSTITUTIONAL: TWSE+TPEx combined foreign -33021860621 TWD; trust +40853040874; dealer -18258815176; total -10427634923.
CREDIT: TWSE margin -57360 native lots; 0050 -3559, 00631L -29393 native lots; cannot infer forced liquidation.
DATA_READINESS: DATA_PARTIAL; VIX 22:35 bar age 25m at 23:00; US others 22:50 age 10m; TX Shioaji true tick 22:54:06.717 age 5m53s at target. Actual completion freshness must be reassessed; no later tick available.
SOURCE_LIMITATIONS: security_identity SEC 403; SPCX identity not verified; historical holdings identity mapping not assumed.
QUALITY_CHECK: NOT_EXECUTED; six displayed daily closes manually checked against daily_ohlcv.data.close and stock_close_table_markdown.
NEXT_CHECK: 2026-11-11 semiconductor relative return and breadth, foreign institutional flow, 0050/00631L credit trend; verify US/TX at completion.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-10-PM","parent_report_id":"2026-11-10-AM","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"reports/2026-11-10/evening.json","observed_at":"2026-11-10","detail":"Semiconductor +2.66% versus TAIEX +2.52%, TWSE breadth 526/491; electronics components +6.75%."}],"change_reason":"Maintain prior rejection; semiconductor again modestly outperformed but narrow spread does not prove fundamental strength.","next_check":"2026-11-11 semiconductor relative return and breadth","falsifier":"Repeated semiconductor underperformance with deteriorating breadth"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"reports/2026-11-10/evening.json","observed_at":"2026-11-10","detail":"00631L 30.25 vs 28.90; margin -29393 native lots; 0050 99.70 vs 97.45; margin -3559; TWSE margin -57360."}],"change_reason":"Credit balances contracted as prices rose, supporting temporary easing; five-day balances remain elevated for 00631L and 0050, so systemic risk not rejected.","next_check":"2026-11-11 ETF and market margin balances with price","falsifier":"Renewed price weakness with expanding margin balances"}],"pending_checks":[],"corrections_applied":[]}
[/RESEARCH_STATE]
