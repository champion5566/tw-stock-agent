# 2026-11-20 morning public original ledger
REPORT_ID: 2026-11-20-AM
OPEN_ID: OPEN-20261120-AM
DATA_BLOB_SHA: 4bce02b5d41a36197b4c71627aee207208cb93c3
DATA_GENERATED_AT: 2026-11-20T08:28:18.412329+08:00
DATA_INPUT_TIMES: market 2026-11-20T08:20:38.177803+08:00; cross 2026-11-20T08:28:00.676165+08:00; US regular 2026-11-19 completed session; JP 08:27; KR 08:28; TX last 04:59:59.
DATA_PUBLICATION: file fetched on data/snapshots; exact changing commit/time not independently certified. point_in_time_verified=false; publication_status=PENDING_PUSH_AND_READBACK.
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261120-AM
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=38426.89.
METHOD: no calibrated reproducible spot-opening model; no numerical prediction. Completed TX night 38107 at 04:59:59 is not 09:00 TWSE cash open.
INPUT_CUTOFF: 2026-11-20 08:38 Asia/Taipei. VERIFICATION_TARGET: 2026-11-20 09:00 TWSE official cash opening.
ELIGIBILITY: NOT_SCORED; no numeric forecast; original publication timing not independently certified.
PARENT_2026-11-19-PM: OPEN-20261119-AM center N/A; FinMind ACT open 40145.73, not official-direct; no score.
NEW_FORMAL_PREDICTIONS: NONE; research scenarios unscored.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
ROLLING_5_20: qualified sample n not audited; no accuracy claim.
SCORE_100: N/A; weights 25/25/15/25/10 unchanged.
TAIEX: 2026-11-19 close 38426.89 (-4.40%), TWSE breadth 67 up/993 down, TPEx 51 up/807 down; semiconductor -4.29% vs market -4.40%.
INSTITUTIONS: TWSE+TPEx total -45289182626 TWD; foreign -23127313437; trust +3331765376; dealer -25493634565.
SIX_CLOSES: 0050 90.2; 006208 202.65; 00631L 24.57; 2330 2100; 3707 46.95; 5483 129.5. Exact same-session daily_ohlcv.data.close; stock_close_table_markdown agrees.
CREDIT: 0050 margin +57046 native lots; 00631L margin -20172 native lots, five-day 82095; TWSE aggregate -144646 native lots.
US_REGULAR_2026-11-19: SP500 -2.02%, NASDAQ -2.25%, SOX -2.41%, TSM ADR -2.90%, NVDA -3.30%, AMD -7.72%, MU -2.10%, VIX +15.80%; completed Yahoo daily bars, not official-direct.
ASIA: TOPIX -2.08%, Advantest -9.37%, Tokyo Electron -6.69%; KOSPI -3.69%, Samsung -4.47%, SK Hynix -6.00% (08:27-08:28); Nikkei 08:12 STALE only.
TX: 38107 at 2026-11-20 04:59:59, completed night last observation, not live.
QUALITY: report_output_quality.py NOT_EXECUTED; six closes manually cross-checked against exact JSON and table.
PUBLICATION: branch changing commit and publication time not independently verified; no retrospective eligibility.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-20-AM","parent_report_id":"2026-11-19-PM","updated_at_taipei":"2026-11-20T08:38:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"TWSE 2026-11-19","detail":"Semiconductor -4.29% versus TAIEX -4.40%, +0.11pp relative; not confirmed domestic sector underperformance"},{"source":"2026-11-19 US regular and 2026-11-20 Asia 08:27-08:28","detail":"SOX -2.41%, TSM ADR -2.90%; Japan equipment and Korea memory sharply down"}],"change_reason":"Overseas weakness raises downside risk but domestic relative weakness not yet confirmed; retain WATCH","next_check":"2026-11-20 TWSE semiconductor relative return, breadth and 2330 foreign flow","falsifier":"Sustained domestic semiconductor outperformance with improving breadth undermines weakness thesis"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure amid sharp drawdowns","status":"WATCH","evidence":[{"source":"2026-11-19 FinMind","detail":"00631L 24.57; margin -20172 native lots, 5d 82095; 0050 margin +57046"}],"change_reason":"One-day deleveraging does not erase five-day credit expansion; no proof of forced liquidation","next_check":"2026-11-20 00631L price and credit daily/5d, TWSE aggregate margin","falsifier":"Sustained credit contraction with price stabilization reduces risk"}],"pending_checks":[{"id":"PUBLICATION-PIN","detail":"Exact file-changing data branch commit/time not independently certified"},{"id":"OPEN-CALIBRATION","detail":"No calibrated numerical open model"},{"id":"QUALITY-CHECK","detail":"Automated output checker not executed"}],"corrections_applied":[{"id":"AM-1105","detail":"Same-basis US daily returns; 04:59 TX not used to infer reaction to 08:28 Korea; stale Nikkei does not discard fresh Japan semiconductor"}]}
[/RESEARCH_STATE]
