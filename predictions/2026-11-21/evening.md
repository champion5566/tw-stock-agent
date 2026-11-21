# 2026-11-21 evening public original ledger
REPORT_ID: 2026-11-21-PM
PARENT_REPORT_ID: 2026-11-21-AM
MARKET_SESSION: SATURDAY_CLOSED
PUBLIC_ONLY: TRUE
DATA_REF_PIN: data/snapshots@32cc8833703d3192ef8c48ab946d0ceb14092026 (2026-11-21 08:37:34 Asia/Taipei)
SOURCE: predictions/2026-11-21/morning.md blob 0fb8f0c736d7a555d35551fbf2704577ae44cd4; predictions/2026-11-20/evening.md blob 6473b614a418b0a401f046975517561f6bb40080
DATA: 2026-11-21 morning.json and evening.json absent at pinned revision. No new Saturday TWSE session.
[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261121-AM
ORIGINAL: SATURDAY_CLOSED; CENTER=N/A; DELTA=N/A; RANGE=N/A; CONFIDENCE=N/A; PREVIOUS_CLOSE=36033.29 (2026-11-20 historical provider close).
ACTUAL_OPEN: NOT_APPLICABLE_NO_SESSION.
SIGNED_ERROR: NOT_APPLICABLE; ABSOLUTE_ERROR: NOT_APPLICABLE; DIRECTION: UNVERIFIABLE; RANGE: UNVERIFIABLE; ELIGIBILITY: NO_MARKET_SESSION; SCORE: NOT_SCORED.
MORNING_FORMAL_PREDICTIONS: NONE; previous 2026-11-20-PM formal new predictions NONE; matured ACT NONE identified in parent. No HIT/MISS; research scenarios are not executable forecast thresholds.
NEXT_SESSION: 2026-11-23 expected next TWSE trading session, subject to official calendar.
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
QUALIFIED_5_20: n/5 and n/20 UNKNOWN_NOT_AUDITED; full original/publication timestamps and matching outcomes not certified; MAE, direction and interval scores NOT_PUBLISHED.
SCORE_WEIGHTS: 25/25/15/25/10; total N/A.
LAST_COMPLETED_TWSE_SESSION: 2026-11-20; TAIEX 36033.29 (-2393.60, -6.23%); TWSE stock breadth 16 up / 1058 down; semiconductor -5.82% versus TAIEX -6.23%.
SIX_LAST_SESSION_CLOSES: 0050=84.45; 006208=189.80; 00631L=21.24; 2330=2000.00; 3707=42.30; 5483=117.00; parent JSON-derived historical values, not current Saturday closes.
CREDIT: 2026-11-20 00631L margin +14262 native lots, five-session +95537; no new Saturday observation.
US: Saturday 23:00 Asia/Taipei is outside US regular session; 2026-11-20 US completed session not independently fetched/verified in this report, no current quote claim. JP/KR Saturday closed; no fabricated prices.
TX: no independently verified true Tick within 10 minutes of Saturday 23:00; UNKNOWN, not historical tick as current.
DATA_READINESS: NOT_APPLICABLE_WEEKEND for TWSE; cross-market data NOT_VERIFIED. CODE_CI UNKNOWN; SOURCE_RUN UNKNOWN.
QUALITY: report_output_quality.py NOT_EXECUTED; no current daily six-stock JSON for manual comparison; historical figures inherited with attribution.
PUBLICATION: pinned branch SHA and parent ledger blob verified; today's new ledger publication/readback separately required.
[/ROLLING_ERROR_LOG]
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-21-PM","parent_report_id":"2026-11-21-AM","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-20 parent original ledger","observed_at":"2026-11-20 close","detail":"Semiconductor -5.82%, TAIEX -6.23%, relative +0.41pp; TWSE 16 advances/1058 declines"}],"change_reason":"No new Taiwan session on Saturday; no new corroboration or falsification","next_check":"2026-11-23 semiconductor minus TAIEX return, breadth, 2330 foreign net shares","falsifier":"Sustained sector outperformance with improving breadth weakens relative-weakness hypothesis"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure amid drawdown","status":"WATCH","evidence":[{"source":"2026-11-20 parent original ledger","observed_at":"2026-11-20 close","detail":"00631L 21.24 (-13.55%), margin +14262 native lots, five-session +95537"}],"change_reason":"Saturday closed; no fresh credit data; prior elevated risk retained without claiming forced liquidation","next_check":"2026-11-23 00631L same-day price and margin daily/five-day changes","falsifier":"Sustained margin contraction and price stabilization weakens risk hypothesis"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"5/20 eligible samples unaudited"},{"id":"SOURCE-PUBLICATION","detail":"No Saturday market JSON; last trading-day data publication time not independently certified"},{"id":"QUALITY-CHECK","detail":"Automated output checker not run"}],"corrections_applied":[]}
[/RESEARCH_STATE]
