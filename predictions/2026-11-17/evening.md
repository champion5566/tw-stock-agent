# 2026-11-17 evening public original ledger
REPORT_ID: 2026-11-17-PM
PARENT_REPORT_ID: 2026-11-17-AM
DATA_BLOB_SHA: 16c157e45e40073c74ec78b5597b1b265d35c361
DATA_GENERATED_AT: 2026-11-17T22:52:01.989162+08:00
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261117-AM
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=41040.08.
ORIGINAL_ELIGIBILITY: NOT_SCORED; morning delivered after 08:40; no numerical forecast.
ACTUAL_OPEN: 40546.64 from 2026-11-17 FinMind TAIEX daily; change -493.44 points, -1.20%; not official-direct 09:00.
SIGNED_ERROR: NOT_APPLICABLE; ABSOLUTE_ERROR: NOT_APPLICABLE; DIRECTION: UNVERIFIABLE; RANGE: UNVERIFIABLE.
MORNING_FORMAL_PREDICTIONS: NONE.
PARENT_EVENING_2026-11-16: No new formal prediction; no matured numeric threshold.
NEW_FORMAL_PREDICTIONS: NONE; scenarios are unscored research checks.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
ROLLING_5_20: Qualified n/5 and n/20 NOT_AUDITED; MAE/direction/range N/A; missing complete originals/results.
SCORE_100: N/A; weights 25/25/15/25/10 retained.
SIX_EXACT_SESSION_CLOSES: 0050 94 (-2.54%); 006208 211.9 (-4.05%); 00631L 26.86 (-3.90%); 2330 2170 (-2.03%); 3707 52 (-4.94%); 5483 144 (-4.00%). Source daily_ohlcv.data.close and stock_close_table_markdown same 2026-11-17.
TAIEX: close 40092.11, open 40546.64, previous 41040.08; TPEX 306.61.
BREADTH: TWSE 234 up 789 down; TPEx 162 up 651 down.
INSTITUTIONS: TWSE+TPEx net -54456368726 TWD; scope separate from TWSE.
MARGIN: TWSE -15035 native lots; TPEx margin missing due HTTP 520.
US: Yahoo/yfinance bars 22:50, VIX 22:35; at 23:00 10min and 25min(DELAYED); completion quote age must be recomputed, not automatically certified.
TX: Shioaji true Tick 2026-11-17T22:51:57.724000+08:00 40089; at 23:00 approx 8m02s, completion age must be recomputed.
JP_KR: dated 2026-11-17 regional quotes are historical after market close; no live 23:00 claim.
QUALITY: report_output_quality.py NOT_EXECUTED; six close fields manually compared against JSON.
PUBLICATION: data blob 16c157e45e40073c74ec78b5597b1b265d35c361; exact branch commit pin not verified; data bundle's publication status PENDING_PUSH_AND_READBACK.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-17-PM","parent_report_id":"2026-11-17-AM","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-17 TWSE sector and TAIEX","detail":"semiconductor -2.16% versus TAIEX -2.31%; relative outperformance 0.15pp despite 234 up/789 down"}],"change_reason":"Relative weakness not confirmed today; broad weakness persists, no fundamental causality proven","next_check":"2026-11-18 semiconductor relative return and TWSE stock breadth, 2330 institutions","falsifier":"Repeated semiconductor outperformance with broad participation"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"2026-11-17 FinMind daily and credit","detail":"00631L close 26.86 vs 27.95 (-3.90%); margin +31328 native lots, 5d +19396; TWSE overall margin -15035"}],"change_reason":"Price decline plus individual ETF margin growth supports elevated risk; no proof of forced liquidation","next_check":"2026-11-18 00631L price, margin change and five-day balance","falsifier":"Price stabilizes and financing contracts"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"No qualified numeric original forecast; rolling 5/20 unverified"},{"id":"OTC-MARGIN-520","detail":"TPEx margin endpoint HTTP 520; no OTC margin aggregation"},{"id":"QUOTE-FRESHNESS","detail":"VIX 22:35 delayed at target; completion freshness not independently re-fetched"},{"id":"PUBLICATION-PIN","detail":"Blob SHA verified; exact commit ref not established; output checker not run"}],"corrections_applied":[]}
[/RESEARCH_STATE]
