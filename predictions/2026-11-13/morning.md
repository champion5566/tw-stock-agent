# 2026-11-13 morning original public ledger
REPORT_ID: 2026-11-13-AM
PARENT_REPORT_ID: 2026-11-12-PM
DATA_PATH: reports/2026-11-13/morning.json
DATA_BLOB_SHA: 2aaaad9f323a2b948562012219a8ace8e3c2e0c3
DATA_GENERATED_AT: 2026-11-13T08:28:18.685132+08:00
DATA_CUTOFF: 2026-11-13T08:38:00+08:00
PUBLICATION_COMMIT_AND_TIME: UNVERIFIED
DATA_READINESS: DATA_PARTIAL; jp/NIKKEI225 DELAYED; other seven Asia observations PASS
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 1
PREDICTION_ID: OPEN-20261113-AM
TARGET: TWSE TAIEX official 2026-11-13 09:00 opening index
CENTER: N/A
DELTA_POINTS: N/A
DELTA_PERCENT: N/A
INTERVAL: N/A
CONFIDENCE: N/A_UNCALIBRATED
PRIOR_CLOSE: 43091.87 (TWSE 2026-11-12 completed session)
DIRECTION: ABSTAIN_NUMERIC
METHOD: No historically calibrated reproducible spot-open model; no synthetic point forecast from TX.
INPUTS: 2026-11-12 US regular close SP500 7592.40 (-0.35%), NASDAQ 25366.09 (-0.39%), SOX 10506.67 (-0.54%), TSM ADR 405.49 (-1.90%), NVDA 166.19 (-4.34%), AMD 585.30 (+5.86%), AVGO 364.36 (+5.54%), MU 798.44 (-1.59%); completed TXFR1 night last observation 43676 at 2026-11-13 04:59:59.450+08:00; JP TOPIX +0.43%, Advantest +6.15%, Tokyo Electron +2.61% at 08:27; Nikkei 08:12 DELAYED; KR KOSPI +2.09%, Samsung +2.28%, SK Hynix +2.87% at 08:28.
INPUT_GENERATED_AT: 2026-11-13T08:28:18.685132+08:00
INPUT_CUTOFF: 2026-11-13T08:38:00+08:00
VERIFICATION_AT: 2026-11-13T09:00:00+08:00 TWSE official
FORMAL_SCORE: UNSCOREABLE_NO_NUMERIC_FORECAST
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-13-AM
PARENT_REPORT_ID: 2026-11-12-PM
PARENT_LEDGER_STATUS: VALID_THREE_BLOCKS
PARENT_PREDICTION_COUNT: 0
PARENT_OPEN: OPEN-20261112-AM abstained; provider open 44180.46 is not an official-direct 09:00 certified outcome.
LATEST_REVIEW_FROM_PARENT: evaluations/ledger-review-43135985334-1.json as of 2026-11-12 09:40:34; 40 historical records, 11 PROVIDER_MATCHED (9 HIT, 2 MISS), 16 UNVERIFIABLE, 13 NOT_TESTED; formal_score_eligible=false.
CURRENT_OPEN_ERROR: N/A
ROLLING_5D_20D: NOT_AUDITED
SCORE_100: N/A; weights 25/25/15/25/10 preserved.
QUALITY_CHECK: NOT_EXECUTED; manually checked six closes against daily_ohlcv.data.close, not broker snapshot.
MARKET: 2026-11-12 TAIEX 43091.87 (-2.63%), semiconductor -2.66%, TWSE breadth 277 up/730 down.
CREDIT: 00631L margin -19495 provider-native lots; TWSE margin -69621 native lots, TPEx -15248 native units separately; no forced liquidation inference.
NEXT_CHECK: 2026-11-13 official TAIEX opening, semiconductor relative return and breadth at close; validate publication commit timestamp separately.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-13-AM","parent_report_id":"2026-11-12-PM","updated_at_taipei":"2026-11-13T08:36:38+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"reports/2026-11-12/evening.json","observed_at":"2026-11-12","detail":"Semiconductor -2.66% versus TAIEX -2.63%, -0.03pp; breadth 277/730"},{"source":"reports/2026-11-13/morning.json","observed_at":"2026-11-13 08:27-08:28","detail":"US SOX -0.54%, TSM ADR -1.90%; Japan Advantest +6.15%, Tokyo Electron +2.61%, Korea Samsung +2.28%, SK Hynix +2.87%"}],"change_reason":"Mixed overseas company-specific moves do not establish renewed persistent Taiwan semiconductor underperformance; retain prior REJECT, recheck Taiwan close.","next_check":"2026-11-13 TWSE semiconductor daily return minus TAIEX daily return, TWSE breadth, TSMC foreign/trust net shares","falsifier":"Repeated meaningful semiconductor underperformance with deteriorating breadth reopens WATCH"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"reports/2026-11-12/evening.json","observed_at":"2026-11-12","detail":"00631L 30.99, margin -19495 native lots; TWSE margin -69621; TPEx margin -15248 native units"}],"change_reason":"No new Taiwan credit data this morning; keep WATCH without claiming margin calls.","next_check":"2026-11-13 00631L/0050 daily close and margin changes; TWSE/TPEx credit separately","falsifier":"Recovery with sustained lower balances weakens immediate leverage-risk claim"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"Collect genuine ex-ante numeric forecasts and official open outcomes; no retrospective scoring"}],"corrections_applied":[{"id":"AM-1105-CHANGE","evidence":"2026-11-13 morning US same-session previous/current closes and returns from deterministic table"},{"id":"AM-1105-TIME","evidence":"04:59 TX observation separately from 08:27-08:28 Asia"},{"id":"AM-1105-COVERAGE","evidence":"Nikkei delayed while TOPIX, Advantest, Tokyo Electron valid"}]}
[/RESEARCH_STATE]
