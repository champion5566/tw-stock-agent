# 2026-11-23 morning public original ledger
REPORT_ID: 2026-11-23-AM
PARENT_REPORT_ID: 2026-11-22-PM
DATA_REF_PIN: data/snapshots@64796fa804c0cd4c1e5ce6ed17f5fb07c1480eed
DATA_COMMIT_AT: 2026-11-23 08:28:25 Asia/Taipei
SOURCE_GENERATED_AT: 2026-11-23 08:28:17 Asia/Taipei
REPORT_DELIVERY: LATE_AFTER_08:40; exact completion time not independently certified
PUBLIC_ONLY: TRUE
[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261123-AM
TARGET: 2026-11-23 09:00 TWSE official TAIEX open
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=36033.29 (2026-11-20, provider market-context dated historical close).
METHOD: No calibrated reproducible spot opening model. No numeric forecast; completed night TXFR1 33919 observed 2026-11-21 04:59:59 is historical and not a spot opening estimate.
INPUT: market fetched 2026-11-23 08:21:06; cross fetched 08:28:00; bundle generated 08:28:17; pinned file-changing commit 08:28:25; data cutoff 08:38.
ELIGIBILITY: NOT_SCORED_NO_NUMERIC_MODEL_AND_LATE_REPORT; no ex-post conversion into qualified prediction.
NEXT_VERIFY: 2026-11-23 09:00 TWSE official opening index, observation only; no error scoring for N/A.
FORECASTS: NONE. ACTIONS: NONE. Top3/New Money: NONE, insufficient evidence.
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
LATEST_REVIEW: evaluations/ledger-review-44760255087-1.json; as_of 2026-11-20 23:09:36 Taipei. PROVIDER_MATCHED outcome is not formal forecast eligibility.
QUALIFIED_5_20: n/5 UNKNOWN_NOT_AUDITED; n/20 UNKNOWN_NOT_AUDITED; MAE/direction/interval N/A.
COMPOSITE_WEIGHTS: 25/25/15/25/10; TOTAL N/A for missing eligible originals/outcomes.
TW_2026-11-20: TAIEX 36033.29 (-6.23%); semiconductor -5.82%; breadth 16 up /1058 down.
SIX_CLOSES_2026-11-20_DAILY: 0050 84.45; 006208 189.80; 00631L 21.24; 2330 2000.00; 3707 42.30; 5483 117.00. All checked against same-session daily_ohlcv.data.close and stock_close_table_markdown.
US_2026-11-20_REGULAR: SP500 7175.83 -> 6910.39 (-3.70%); NASDAQ 23879.20 -> 22617.73 (-5.28%); SOX 9419.72 -> 8408.59 (-10.73%); TSM ADR 352.09 -> 318.71 (-9.48%); NVDA 145.98 -> 125.53 (-14.01%); AMD 489.19 -> 424.39 (-13.25%); AVGO 346.65 -> 304.41 (-12.19%); MU 690.44 -> 594.51 (-13.89%); VIX 28.44 -> 35.89 (+26.20%).
ASIA_2026-11-23_0828: Japan MARKET_CLOSED per calendar (prior 11/20 quotes not live); Korea KOSPI -3.26%, KOSDAQ -1.52%, Samsung -3.99%, SK Hynix -3.14%; Naver provider timestamps.
TX: 33919 at 2026-11-21 04:59:59, completed night historical last snapshot, not 11/23 live.
SOURCE_GAPS: SEC ticker identity HTTP403; formal sample calibration unavailable. Japan market closed is not source outage.
DATA_READINESS: DATA_READY (bundle contract); original ledger late and not formally eligible.
QUALITY_CHECK: NOT_EXECUTED; six displayed daily closes manually compared to pinned JSON.
PUBLICATION_READBACK: pinned source data read; original ledger create/readback pending.
DELIVERY_ACK: UNKNOWN.
[/ROLLING_ERROR_LOG]
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-23-AM","parent_report_id":"2026-11-22-PM","updated_at_taipei":"2026-11-23 08:4x Asia/Taipei (late run; exact completion clock unverified)","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"reports/2026-11-23/morning.json@64796fa; 2026-11-20 close","observed_at":"2026-11-20 close","detail":"Semiconductor -5.82%, TAIEX -6.23%; +0.41pp relative; US SOX -10.73% on 11/20; KR KOSPI -3.26% at 08:28 11/23"}],"change_reason":"Overseas downside reinforces risk but Taiwan sector relative weakness remains unproven; Japan closed","next_check":"2026-11-23 Taiwan semiconductor vs TAIEX completed-session return and breadth","falsifier":"Sector outperformance and broadening advances weaken persistent relative-weakness thesis"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure amid drawdown","status":"WATCH","evidence":[{"source":"reports/2026-11-23/morning.json@64796fa","observed_at":"2026-11-20 close","detail":"00631L close 21.24; margin +14262 native lots daily, +95537 over five sessions; 0050 margin -61672 daily"}],"change_reason":"00631L credit build persists; 0050 margin has contracted, so no generalized claim of expanding margin or forced liquidation","next_check":"2026-11-23 00631L close and margin daily/five-day changes","falsifier":"Margin contraction and price stabilization over subsequent sessions weaken credit-risk thesis"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"5/20 qualified original/actual samples not audited; opening model unavailable"},{"id":"SOURCE-PUBLICATION","detail":"Data commit at 08:28:25 verified; late original ledger not formal forecast"},{"id":"QUALITY-CHECK","detail":"report_output_quality.py not executed; manual daily close JSON comparison only"}],"corrections_applied":[{"id":"AM-1105-CHANGE","evidence":"2026-11-20 completed US close-to-close values recorded in current report"},{"id":"AM-1105-TIME","evidence":"2026-11-21 04:59 TX historical snapshot explicitly separated from 2026-11-23 08:28 Korea"}]}
[/RESEARCH_STATE]
