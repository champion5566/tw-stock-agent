# 2026-11-20 evening public original ledger
REPORT_ID: 2026-11-20-PM
PARENT_REPORT_ID: 2026-11-20-AM
DATA_BLOB_SHA: c16f0920df43ca12dfc5a571486adda4841fd11a
DATA_GENERATED_AT: 2026-11-20T22:54:12.501024+08:00
DATA_PUBLICATION: data/snapshots branch file fetched and blob checked; exact file-changing commit/time not independently certified. Bundle publication_status=PENDING_PUSH_AND_READBACK. No retroactive eligibility.
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261120-AM
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=38426.89.
ACTUAL_OPEN: 37646.13; FinMind TAIEX same-session market_context, 2026-11-20; -780.76 points (-2.03%) vs previous close. Not official-direct 09:00.
SIGNED_ERROR: NOT_APPLICABLE; ABSOLUTE_ERROR: NOT_APPLICABLE; DIRECTION: UNVERIFIABLE; RANGE: UNVERIFIABLE.
ELIGIBILITY: NOT_SCORED; no numerical original forecast; original file-changing publication time not independently certified.
MORNING_FORMAL_PREDICTIONS: NONE in original 2026-11-20-AM ledger.
PARENT_EVENING_2026-11-19: NEW_FORMAL_PREDICTIONS NONE; research scenarios unscored. No matured numeric threshold or ACT established.
NEW_FORMAL_PREDICTIONS: NONE; next-session scenarios research-only, not retrospectively scored.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
ROLLING_5_20: qualified n/5 and n/20 NOT_AUDITED; original text, publication time and matching official outcomes not fully certified. No MAE/hit-rate.
SCORE_100: N/A; weights 25/25/15/25/10 unchanged.
TAIEX: 2026-11-20 open 37646.13, close 36033.29 versus 38426.89, -2393.60 (-6.23%); TPEX close 263.31.
BREADTH: TWSE stock-only 16 advances/1058 declines; TPEx four-digit 49 advances/815 declines, 12 noncomparable.
SECTOR: semiconductor -5.82% vs TAIEX -6.23%, relative +0.41pp; electronic components -9.51%.
INSTITUTIONS: TWSE+TPEx foreign -1832333955 TWD, trust -6833846102, dealer -35242349433, total -43908529490. TWSE-only total -50940775695; TPEx +7032246205. Do not mix scopes.
MARGIN: TWSE -548868 provider-native lots; TPEx -102429 provider-native units separately. 00631L margin +14262 lots, five-session +95537, price -13.55%; 0050 margin -61672 native lots.
SIX_EXACT_SESSION_CLOSES: 0050 84.45; 006208 189.80; 00631L 21.24; 2330 2000.00; 3707 42.30; 5483 117.00. Same-session daily_ohlcv.data.close agrees with stock_close_table_markdown; no broker snapshot.
US: Yahoo/yfinance 22:50 bars, VIX 22:35. At 23:00 main 10m, VIX 25m DELAYED; at 23:04:56 main 14m56s, VIX 29m56s DELAYED. Later than 23:05 VIX STALE, main after 23:05 DELAYED. No fresh completion-time pull.
TX: Shioaji true TXFR1 tick 2026-11-20T22:54:11.791+08:00 price 36047; at 23:00 age 5m48s PASS; at 23:04:56 age 10m44s FAIL >10m.
ASIA: same-day dated JP/KR observations, historical at 23:00, not live; Nikkei -5.06%, TOPIX -3.88%, KOSPI -5.21%, SK Hynix -7.02%.
QUALITY: report_output_quality.py NOT_EXECUTED; six closes manually checked against JSON and deterministic table. Not automatic PASS.
PUBLICATION: exact data-branch file-changing commit/time NOT_VERIFIED; bundle generated before 22:58 but generation alone does not certify publication.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-20-PM","parent_report_id":"2026-11-20-AM","updated_at_taipei":"2026-11-20T23:04:56+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-20 TWSE sector board / FinMind TAIEX","observed_at":"2026-11-20 close","detail":"Semiconductor -5.82% vs TAIEX -6.23% (+0.41pp relative), TWSE breadth 16 up/1058 down; no sector-specific underperformance"},{"source":"2026-11-20 regional dated observations","observed_at":"2026-11-20 trading day","detail":"Nikkei -5.06%, TOPIX -3.88%, KOSPI -5.21%; overseas semiconductor hardware weak, not proof of Taiwan earnings impairment"}],"change_reason":"Broad collapse increases market risk but Taiwan semiconductors outperform; relative-weakness claim not accepted","next_check":"2026-11-23 semiconductor return minus TAIEX return, TWSE breadth, 2330 foreign net shares","falsifier":"Sustained domestic semiconductor outperformance with breadth recovery rejects persistent weakness; repeated underperformance with worsening breadth supports it"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure amid drawdown","status":"WATCH","evidence":[{"source":"2026-11-20 FinMind 00631L and TWSE margin","observed_at":"2026-11-20 close","detail":"00631L 21.24 (-13.55%), margin +14262 native lots, 5d +95537; TWSE aggregate margin -548868 lots"}],"change_reason":"Renewed 00631L margin expansion amid sharp drawdown increases exposure concern, but does not prove forced liquidation","next_check":"2026-11-23 00631L price, margin daily/5d, TWSE breadth and aggregate margin","falsifier":"Sustained credit contraction with price stabilization reduces risk; further falling price plus rising margin strengthens concern"}],"pending_checks":[{"id":"PUBLICATION-PIN","detail":"Exact file-changing data branch commit/time not independently certified"},{"id":"OPEN-CALIBRATION","detail":"No qualified numeric open forecast; 5/20 n unaudited"},{"id":"US-TX-FRESHNESS","detail":"TX older than 10 minutes at 23:04:56; new tick required"},{"id":"QUALITY-CHECK","detail":"Automated report checker not executed"}],"corrections_applied":[]}
[/RESEARCH_STATE]
