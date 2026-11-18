# 2026-11-18 evening public original ledger
REPORT_ID: 2026-11-18-PM
PARENT_REPORT_ID: 2026-11-18-AM
DATA_BLOB_SHA: e4aabf7975aa6e9f4ae7622e67eebc48ec68a3dd
DATA_GENERATED_AT: 2026-11-18T22:53:57.428107+08:00
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261118-AM
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=40092.11.
ORIGINAL_ELIGIBILITY: NOT_SCORED; no numerical original; publication/delivery timing not independently certified.
ACTUAL_OPEN: 40720.09 from 2026-11-18 FinMind TAIEX daily; change +627.98 points, +1.57%; not official-direct 09:00.
SIGNED_ERROR: NOT_APPLICABLE; ABSOLUTE_ERROR: NOT_APPLICABLE; DIRECTION: UNVERIFIABLE; RANGE: UNVERIFIABLE.
MORNING_FORMAL_PREDICTIONS: NONE.
PARENT_EVENING_2026-11-17: No formal numeric forecast or matured ACT threshold identified in original ledger; unscored conditional research checks.
NEW_FORMAL_PREDICTIONS: NONE; next-session scenarios are unscored research checks.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
ROLLING_5_20: Qualified n/5 and n/20 NOT_AUDITED; complete original forecasts, timing and matched outcomes missing; MAE/direction/range N/A.
SCORE_100: N/A; weights 25/25/15/25/10 retained.
TAIEX: 2026-11-18 open 40720.09 close 40194.91 vs prior 40092.11, +102.80 (+0.26%); TPEX close 307.55.
BREADTH: TWSE 492 up/520 down; TPEx 352 up/433 down.
SECTOR: semiconductor +0.64%, electronic components +1.03%, TWSE TAIEX +0.26%.
INSTITUTIONS: TWSE+TPEx foreign -75204608285 TWD; trust +11953755582; dealer -4465094409; total -67715947112. Market scopes remain separate where required.
MARGIN: TWSE +105588 provider-native lots; TPEx -7838 provider-native units, not aggregated; 00631L +48725, five-session +82772.
SIX_EXACT_SESSION_CLOSES: 0050 94.10; 006208 212.00; 00631L 26.84; 2330 2175.00; 3707 51.50; 5483 142.00. Source 2026-11-18 daily_ohlcv.data.close, matched stock_close_table_markdown, not broker snapshot.
US: Yahoo/yfinance 22:50 five-minute bars and VIX 22:35; at 23:00 age 10m and 25m DELAYED respectively. No completion-time PASS assumed. BRK.B mapped to Yahoo BRK-B; SPCX identity unverified.
TX: Shioaji TXFR1 true tick 2026-11-18T22:53:56.411+08:00 price 39812; 23:00 age 6m04s; completion-time age not independently certified.
QUALITY: report_output_quality.py NOT_EXECUTED; six displayed closes manually compared to pinned blob; no automatic PASS.
PUBLICATION: snapshot blob SHA verified; exact branch commit and file publication timestamp NOT_VERIFIED; generated 22:53:57, bundle status PENDING_PUSH_AND_READBACK. No retroactive formal qualification.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-18-PM","parent_report_id":"2026-11-18-AM","updated_at_taipei":"2026-11-18T22:58:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-18 TWSE sector board and FinMind TAIEX","observed_at":"2026-11-18 close","detail":"semiconductor +0.64% versus TAIEX +0.26%, relative +0.38pp; TWSE breadth 492 up/520 down; 2330 foreign net -15452905 shares"}],"change_reason":"Semiconductor outperformed, opposing persistent relative weakness; breadth mixed, so keep WATCH rather than claim structural recovery","next_check":"2026-11-19 sector relative return, breadth and 2330 foreign net","falsifier":"Repeated relative underperformance alongside deteriorating breadth would support weakness; repeated outperformance would reject it"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"2026-11-18 FinMind 00631L daily/credit and TWSE margin","observed_at":"2026-11-18 close","detail":"00631L 26.84 versus 26.86 (-0.07%); margin +48725 native lots, five-session +82772; TWSE margin +105588"}],"change_reason":"Leverage financing expansion accelerated while ETF failed to recover; risk elevated, no proof of forced liquidation","next_check":"2026-11-19 00631L price and margin daily/five-session, TWSE credit and breadth","falsifier":"Sustained margin contraction with price stabilization"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"No numeric morning opening forecast; 5/20 qualified samples not audited"},{"id":"PUBLICATION-PIN","detail":"Exact data/snapshots branch commit and file publication timestamp not independently certified; blob SHA e4aabf7975aa6e9f4ae7622e67eebc48ec68a3dd"},{"id":"US-TX-FRESHNESS","detail":"23:00 ages must be recomputed; completion-time freshness requires independent time evidence"},{"id":"SECURITY-IDENTITY","detail":"SPCX current identity unverified due SEC 403; do not equate with historical holdings"}],"corrections_applied":[]}
[/RESEARCH_STATE]
