# 2026-11-22 evening public original ledger
REPORT_ID: 2026-11-22-PM
PARENT_REPORT_ID: 2026-11-22-AM
MARKET_SESSION: SUNDAY_CLOSED
PUBLIC_ONLY: TRUE
DATA_REF_PIN: data/snapshots@94d3a193c9339e1f195809159ce3c62db77dcdb7 (GitHub ref read in this run)
PARENT_LEDGER: predictions/2026-11-22/morning.md blob 818681433cb313ec861ffe54b8c2682b60716e0f
PREVIOUS_EVENING: predictions/2026-11-21/evening.md blob 8ddc0142cc093205767ef30d383ac489a932e404
CURRENT_MARKET_JSON: reports/2026-11-22/morning.json and evening.json NOT_FOUND at pinned ref.
[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261122-AM
ORIGINAL: SUNDAY_CLOSED; CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; PREVIOUS_CLOSE=36033.29 (2026-11-20 historical provider value, not Sunday market data).
ACTUAL_OPEN: NOT_APPLICABLE_NO_SESSION.
SIGNED_ERROR: NOT_APPLICABLE; ABSOLUTE_ERROR: NOT_APPLICABLE; DIRECTION: UNVERIFIABLE; RANGE: UNVERIFIABLE; ELIGIBILITY: NO_MARKET_SESSION; SCORE: NOT_SCORED.
MORNING_FORMAL_PREDICTIONS: NONE (parent morning original).
PARENT_MATURED_ACT: NONE identified in 2026-11-21-PM original.
HIT/MISS: NONE; no unsupported numerical thresholds or conditional scenario partially settled.
NEXT_EXPECTED_SESSION: 2026-11-23, subject to official calendar.
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
QUALIFIED_5_20: n/5 UNKNOWN_NOT_AUDITED; n/20 UNKNOWN_NOT_AUDITED; missing certified original/actual/timing pairs. No MAE/direction/interval publication.
SCORE_WEIGHTS: 25/25/15/25/10; TOTAL: N/A.
LAST_COMPLETED_TWSE_SESSION: 2026-11-20; TAIEX 36033.29 (-2393.60, -6.23%); 16 advances /1058 declines; semiconductor -5.82%; inherited from parent, not reverified official-direct in this run.
SIX_HISTORICAL_CLOSES_2026-11-20: 0050=84.45; 006208=189.80; 00631L=21.24; 2330=2000.00; 3707=42.30; 5483=117.00; parent-sourced historical values, no Sunday daily_ohlcv comparison possible.
CREDIT_2026-11-20: 00631L margin +14262 native lots, five-session +95537; no evidence of forced liquidation.
US: Sunday no US regular session; Friday close and individual monitoring list not independently reverified. No current price claim.
JP/KR: Sunday closed; no current-session price.
TX: no verified true Tick within ten minutes of Sunday 23:00; status UNKNOWN.
DATA_READINESS: MARKET_CLOSED_SUNDAY; historical cross-market coverage NOT_VERIFIED.
CODE_CI: UNKNOWN; SOURCE_RUN: NOT_APPLICABLE_SUNDAY; QUALITY_CHECK: NOT_EXECUTED; PUBLICATION_READBACK: pending create/readback; DELIVERY_ACK: UNKNOWN.
[/ROLLING_ERROR_LOG]
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-22-PM","parent_report_id":"2026-11-22-AM","updated_at_taipei":"2026-11-22 23:02 Asia/Taipei","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-22-AM original ledger citing 2026-11-20 completed session","observed_at":"2026-11-20 close","detail":"Semiconductor -5.82% versus TAIEX -6.23%, relative +0.41pp; breadth 16 advances/1058 declines"}],"change_reason":"Sunday closed; no new Taiwan trading evidence","next_check":"2026-11-23 sector-relative return, breadth, 2330 foreign net shares","falsifier":"Repeated sector outperformance with broader advances weakens weakness hypothesis"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure amid drawdown","status":"WATCH","evidence":[{"source":"2026-11-22-AM original ledger citing 2026-11-20 completed session","observed_at":"2026-11-20 close","detail":"00631L 21.24, margin +14262 native lots; five-day +95537"}],"change_reason":"No Sunday ETF price or margin observation; no inference of liquidation","next_check":"2026-11-23 00631L daily close and daily/five-day margin change","falsifier":"Sustained margin contraction alongside price stabilization weakens risk hypothesis"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"5/20 qualified original/outcome pairs not audited"},{"id":"SOURCE-PUBLICATION","detail":"Historical publication time and latest evaluation review not independently certified"},{"id":"QUALITY-CHECK","detail":"No Sunday market JSON; report_output_quality.py not executed"}],"corrections_applied":[]}
[/RESEARCH_STATE]
