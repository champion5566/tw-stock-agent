# 2026-11-23 evening public original ledger
REPORT_ID: 2026-11-23-PM
PARENT_REPORT_ID: 2026-11-23-AM
DATA_REF_PIN: data/snapshots@cc4d78417df8bf1964ef8fd6903fc4840ad7d415
DATA_JSON_BLOB: 2c1bea39f3e783ce688dcbd3cbbc0280898c92ed
DATA_COMMIT_AT: 2026-11-23 22:51:57 Asia/Taipei
SOURCE_GENERATED_AT: 2026-11-23T22:51:53.115969+08:00
PUBLIC_ONLY: TRUE
[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261123-AM
ORIGINAL: ABSTAIN_NUMERIC; CENTER=N/A; DELTA=N/A; RANGE=N/A; PREVIOUS_CLOSE=36033.29; MORNING_LEDGER_LATE_AFTER_08:40.
ACTUAL_OPEN: 35899.48 (2026-11-23 FinMind same-day daily market context; not TWSE official direct 09:00).
ACTUAL_DELTA: -133.81 points; ACTUAL_PERCENT: -0.37%.
SIGNED_ERROR/ABS_ERROR: NOT_APPLICABLE_NO_NUMERIC_FORECAST; DIRECTION/RANGE: UNVERIFIABLE; FORMAL_SCORE: NOT_SCORED.
TODAY_MORNING_FORECASTS: NONE; ACTIONS: NONE.
PREVIOUS_EVENING_2026-11-22: no matured formal ACT identified; no HIT/MISS.
NEXT_SESSION: 2026-11-24; conditional research scenarios are not formal numeric predictions.
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
QUALIFIED_5_20: n/5 UNKNOWN_NOT_AUDITED; n/20 UNKNOWN_NOT_AUDITED; original, publication and outcome eligibility missing; MAE/direction/coverage NOT_PUBLISHED.
SCORE_WEIGHTS: 25/25/15/25/10; TOTAL: N/A.
LATEST_REVIEW: evaluations/ledger-review-45096159177-1.json (2026-11-23 09:44:42 Taipei); PROVIDER_MATCHED is outcome-only, not official or formally eligible.
TAIEX_2026-11-23: close 36811.89; open 35899.48; breadth TWSE 652 up/362 down; TPEX 560 up/254 down.
SIX_CLOSES_2026-11-23_DAILY: 0050=87; 006208=195.55; 00631L=22.5; 2330=2030; 3707=43.3; 5483=128.5; sourced exclusively same-session daily_ohlcv.data.close, agrees with stock_close_table_markdown.
CREDIT: 00631L margin +89847 native lots, five-session +163990; TWSE total +132289; do not infer liquidation.
US: yfinance 22:50 five-minute bars; VIX 22:35 (DELAYED at 23:00); no post-collection refresh certified.
TX: Shioaji TXFR1 40035 at 22:51:51.795; 23:00 age 8m08s, completion age must be recalculated.
DATA_READINESS: DATA_PARTIAL (VIX delayed). CODE_CI: UNKNOWN. SOURCE_RUN: 45198480418. PUBLICATION_READBACK: data exact-ref read; new ledger readback pending. DELIVERY_ACK: UNKNOWN.
QUALITY_CHECK: NOT_EXECUTED; six daily closes manually compared to JSON/table; no automatic PASS.
[/ROLLING_ERROR_LOG]
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-23-PM","parent_report_id":"2026-11-23-AM","updated_at_taipei":"2026-11-23 22:56 Asia/Taipei (ledger construction; actual delivery separate)","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"reports/2026-11-23/morning.json@64796fa; 2026-11-20 close","observed_at":"2026-11-20 close","detail":"Semiconductor -5.82%, TAIEX -6.23%; +0.41pp relative; US SOX -10.73% on 11/20; KR KOSPI -3.26% at 08:28 11/23"},{"source":"reports/2026-11-23/evening.json@cc4d78417df8bf1964ef8fd6903fc4840ad7d415","observed_at":"2026-11-23 close","detail":"TAIEX +2.16%, semiconductor +2.58%, relative +0.42pp; TWSE breadth 652/362; institutional combined -477.44 億 TWD"}],"change_reason":"Taiwan sector outperformed again, so persistent sector-specific weakness lacks support; keep WATCH pending multi-session check","next_check":"2026-11-24 sector-relative return, breadth, foreign 2330 flow","falsifier":"Repeated semiconductor underperformance with worsening breadth"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure amid drawdown","status":"WATCH","evidence":[{"source":"reports/2026-11-23/morning.json@64796fa","observed_at":"2026-11-20 close","detail":"00631L close 21.24; margin +14262 native lots daily, +95537 over five sessions; 0050 margin -61672 daily"},{"source":"reports/2026-11-23/evening.json@cc4d78417df8bf1964ef8fd6903fc4840ad7d415","observed_at":"2026-11-23 close","detail":"00631L 22.50 (+5.93%), margin +89847 provider-native lots, five-session +163990; TWSE margin +132289"}],"change_reason":"Price rebound with sharply increased 00631L margin increases credit exposure; no evidence of liquidation","next_check":"2026-11-24 00631L close/margin and five-session credit","falsifier":"Margin reduction sustained with price stabilization"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"5/20 eligible originals and outcomes not audited; no numeric morning forecast"},{"id":"PUBLICATION-TIMING","detail":"Bundle commit timestamp 22:51:57 verified; ledger/report delivery independently unverified"},{"id":"QUOTE-AGE","detail":"US 22:50 bars and VIX 22:35; TX 22:51:51.795 require age recomputation at actual delivery"}],"corrections_applied":[{"id":"AM-1105-CHANGE","evidence":"2026-11-20 completed US close-to-close values recorded in current report"},{"id":"AM-1105-TIME","evidence":"2026-11-21 04:59 TX historical snapshot explicitly separated from 2026-11-23 08:28 Korea"}]}
[/RESEARCH_STATE]
