# 2026-11-17 morning public original ledger
REPORT_ID: 2026-11-17-AM
OPEN_ID: OPEN-20261117-AM
SNAPSHOT_SHA: fa3b26305a928b0cd654b904062e26c69718a9b8
DATA_GENERATED_AT_TAIPEI: 2026-11-17T08:28:21+08:00
DATA_COMMIT_AT_TAIPEI: 2026-11-17T08:28:27+08:00
REPORT_DELIVERY: AFTER_08:40; original numerical forecast not qualified
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261117-AM
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=41040.08 (TWSE 2026-11-16).
METHOD: No calibrated, reproducible mapping from completed US regular session, completed TX night, and fresh Asia observations to TWSE 09:00 spot open. No futures last-tick substitution.
INPUTS: pinned morning.json generated 08:28:21; market fetched 08:23:47; cross fetched 08:28:00; TXFR1 40935 at 04:59:53 completed-night last observation; US completed 2026-11-16 regular-session bars; Asia regional 08:27-08:28, Nikkei 08:12 STALE.
CUTOFF: 2026-11-17 08:38 Asia/Taipei; verification target TWSE official 2026-11-17 09:00 open.
ELIGIBILITY: NOT_SCORED; output after 08:40, no numeric pre-open original. No backfill from later actual.
PRIOR_EVENING: 2026-11-16-PM no new formal numeric prediction; evening.json missing at pinned snapshot, parent original ledger exists.
NEW_FORMAL_PREDICTIONS: NONE.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
OPEN_5_20: qualified sample count unverified; numerical MAE/direction/range N/A.
SCORE_100: N/A (25/25/15/25/10 weights retained; no qualifying original numeric forecast).
SOURCE: reports/2026-11-17/morning.json at fa3b26305a928b0cd654b904062e26c69718a9b8; stock OHLCV 2026-11-16, all six PASS; US completed 2026-11-16 normal-session closes PASS; Asia Nikkei STALE, TOPIX and Japan semiconductor plus Korea PASS.
PREVIOUS_EVENING_GAP: reports/2026-11-16/evening.json NOT_FOUND at pinned SHA; 2026-11-16 evening ledger is late and documents same issue.
OUTPUT_CHECK: report_output_quality.py NOT_EXECUTED; printed six daily closes manually checked against stock_close_table_markdown and daily_ohlcv.data.close.
SOURCE_LIMITATIONS: SEC company ticker lookup 403; Nikkei STALE 08:12, do not discard other Japan quotes; US cross_market intraday bars not used as formal normal-session close; TX night 04:59:53 is historical not 08:40 live.
NEXT_CHECK: confirm source freshness and restore missing evening JSON through documented pipeline; do not retroactively qualify late material.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-17-AM","parent_report_id":"2026-11-16-PM","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-16 TWSE official sector index","detail":"semiconductor -6.33% vs TAIEX -6.03%; electronics components -9.42%"},{"source":"Yahoo/yfinance 2026-11-16 completed US regular daily","detail":"SOX -5.28%, Nasdaq -2.49%, TSM ADR -6.34%"},{"source":"2026-11-17 08:27-08:28 Asia regional","detail":"TOPIX -1.24%, Advantest -3.77%, Tokyo Electron +0.57%, KOSPI -1.12%, Samsung -1.47%, Hynix 0.00%"}],"change_reason":"Retain WATCH; relative weakness supported but persistence and fundamental earnings transmission unverified","next_check":"2026-11-17 TWSE semiconductor minus TAIEX close return, stock breadth, TSM institutions","falsifier":"Semiconductor relative outperformance with improved breadth"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"FinMind exact 2026-11-16 00631L daily and margin","detail":"close 27.95 vs prior 31.92; margin balance +21394 native lots on day, -41325 five-day"}],"change_reason":"Sharp price loss with rising same-day margin exposure warrants WATCH; no forced liquidation conclusion","next_check":"2026-11-17 00631L daily close and margin changes plus TWSE breadth","falsifier":"Price stabilization with sustained credit contraction"}],"pending_checks":[{"id":"EVENING-DATA-MISSING","detail":"2026-11-16 evening.json absent at pinned SHA"},{"id":"NIKKEI-STALE","detail":"08:12 selected regional quote stale; valid TOPIX and equipment quotes retained"},{"id":"OPEN-CALIBRATION","detail":"No qualified numeric opening forecast model"}],"corrections_applied":[]}
[/RESEARCH_STATE]
