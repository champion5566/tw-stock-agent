# 2026-11-19 evening public original ledger
REPORT_ID: 2026-11-19-PM
PARENT_REPORT_ID: 2026-11-19-AM
DATA_BLOB_SHA: 8af25168108939b60d7368b5629f436ebf24c4f6
DATA_GENERATED_AT: 2026-11-19T22:51:46.367647+08:00
DATA_PUBLICATION: exact file-changing commit/time not independently certified; bundle publication_status=PENDING_PUSH_AND_READBACK
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261119-AM
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=40194.91.
ACTUAL_OPEN: 40145.73; provider FinMind TAIEX same-session market_context; -49.18 points (-0.12%) versus prior close; not official-direct 09:00.
SIGNED_ERROR: NOT_APPLICABLE; ABSOLUTE_ERROR: NOT_APPLICABLE; DIRECTION: UNVERIFIABLE; RANGE: UNVERIFIABLE.
ORIGINAL_ELIGIBILITY: NOT_SCORED; no original numerical forecast; original publication time not independently certified.
MORNING_FORMAL_PREDICTIONS: NONE in original ledger.
PARENT_EVENING_2026-11-18: no matured formal numeric threshold or ACT established in original ledger; conditional research checks unscored.
NEW_FORMAL_PREDICTIONS: NONE. Next-session scenarios are research checks only.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
ROLLING_5_20: qualified n/5 and n/20 NOT_AUDITED; original text, timestamps, and matching results not fully verified; no MAE or hit rate.
SCORE_100: N/A; weights 25/25/15/25/10 unchanged.
TAIEX: 2026-11-19 open 40145.73, close 38426.89 versus 40194.91, -1768.02 (-4.40%); TPEX close 285.33.
BREADTH: TWSE 67 up/993 down; TPEx 51 up/807 down, 19 uncomparable.
SECTOR: semiconductor -4.29% vs TAIEX -4.40%; electronic components -8.34%.
INSTITUTIONS: TWSE+TPEx foreign -23127313437 TWD, trust +3331765376, dealer -25493634565, total -45289182626. TWSE and TPEx scopes separately preserved.
MARGIN: TWSE -144646 native lots; TPEx -80400 native units, not merged. 00631L -20172 native lots, five-session +82095; 0050 +57046 native lots, five-session +82875.
SIX_EXACT_SESSION_CLOSES: 0050 90.20; 006208 202.65; 00631L 24.57; 2330 2100.00; 3707 46.95; 5483 129.50. 2026-11-19 daily_ohlcv.data.close agrees with stock_close_table_markdown; no broker snapshots.
US: Yahoo/yfinance 22:50 bars (SOX 22:51), VIX 22:35. At 23:00 main 9-10m, VIX 25m DELAYED; completion-time independent verification unavailable.
TX: Shioaji TXFR1 true tick 2026-11-19T22:51:44.693+08:00, price 39712; at 23:00 age 8m15s; completion-time age not independently certified.
ASIA: JP/KR provider quotes have same-day dated observations but are STALE relative to 23:00; not current session live.
QUALITY: report_output_quality.py NOT_EXECUTED; six closes manually compared with exact JSON and deterministic table.
PUBLICATION: report bundle fetched from data/snapshots and blob SHA checked; branch commit and file-changing timestamp NOT_INDEPENDENTLY_VERIFIED. Not retroactively qualified.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-19-PM","parent_report_id":"2026-11-19-AM","updated_at_taipei":"2026-11-19T23:00:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-19 TWSE sector and FinMind TAIEX","observed_at":"2026-11-19 close","detail":"semiconductor -4.29% versus TAIEX -4.40%, relative +0.11pp; TWSE breadth 67/993; 2330 foreign net -8634761 shares"}],"change_reason":"Broad selloff but semiconductor slightly outperformed, so persistent sector-specific relative weakness not confirmed","next_check":"2026-11-20 semiconductor relative return, breadth, and 2330 foreign net","falsifier":"Repeated sector underperformance alongside deteriorating breadth supports weakness; sustained outperformance rejects it"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"2026-11-19 FinMind 00631L and TWSE margin","observed_at":"2026-11-19 close","detail":"00631L 24.57 (-8.46%), margin -20172 native lots, five-session +82095; 0050 margin +57046; TWSE aggregate margin -144646"}],"change_reason":"Sharp leveraged ETF drawdown and still-positive five-day credit growth despite one-day deleveraging warrant continued risk monitoring; no forced-liquidation proof","next_check":"2026-11-20 00631L price, margin daily and five-session; TWSE breadth and market margin","falsifier":"Sustained margin contraction and price stabilization reduce risk; renewed borrowing amid further drawdown increases risk"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"No numeric morning forecast; qualified 5/20 sample counts unaudited"},{"id":"PUBLICATION-PIN","detail":"Exact data branch commit and file publication time not independently verified; blob SHA 8af25168108939b60d7368b5629f436ebf24c4f6"},{"id":"US-TX-FRESHNESS","detail":"23:00 ages calculated; completion-time verification pending"},{"id":"QUALITY-CHECK","detail":"Script not executed; manually checked six closes"}],"corrections_applied":[]}
[/RESEARCH_STATE]
