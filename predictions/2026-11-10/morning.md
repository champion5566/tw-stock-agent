# 2026-11-10 morning original public ledger
REPORT_ID: 2026-11-10-AM
PARENT_REPORT_ID: 2026-11-09-PM
DATA_REF: d704f01c90a46f1e54ce14269441259123b9ec06
DATA_PATH: reports/2026-11-10/morning.json
DATA_GENERATED_AT: 2026-11-10T08:28:15.381553+08:00
DATA_PUBLICATION_COMMIT_AT: 2026-11-10T08:28:20+08:00
REPORT_RUN: AFTER_08:40_TARGET; actual completion independently unknown
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 1
PREDICTION_ID: OPEN-20261110-AM
TARGET: TWSE official TAIEX 2026-11-10 09:00 opening index
PRIOR_CLOSE: 41661.70 (2026-11-09 TWSE MI_5MINS_HIST)
CENTER: N/A
DELTA_POINTS: N/A
DELTA_PERCENT: N/A
INTERVAL: N/A
CONFIDENCE: N/A_UNCALIBRATED
DIRECTION: ABSTAIN_NUMERIC
METHOD: No validated historical point-in-time fitted conversion from TX futures, US/Asia returns and spot previous close to official opening index. Arithmetic futures-minus-spot is not a calibrated forecast.
INPUT_TIMES: Taiwan market 2026-11-10 08:22:39+08:00; cross 08:28:00+08:00; US 2026-11-09 completed regular daily bars; TXFR1 completed-night last observation 2026-11-10 04:59:56.944+08:00; JP TOPIX/ADVANTEST/TOKYO_ELECTRON 08:27+08:00; KR 08:28+08:00; NIKKEI 08:12 STALE.
DATA_CUTOFF: 2026-11-10T08:38:00+08:00
VERIFY_AT: 2026-11-10T09:00:00+08:00
FORMAL_SCORE_ELIGIBILITY: FALSE_NO_NUMERIC_FORECAST
INVALIDATION: not applicable; abstention
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-10-AM
PARENT_REPORT_ID: 2026-11-09-PM
PARENT_PREDICTION_COUNT: 0
PARENT_OPEN_20261109_AM: UNSCOREABLE; original CENTER N/A; parent evening reported actual 40347.28; do not score.
SCORE_100_WEIGHTS: 25/25/15/25/10
SCORE_100: N/A_NO_ELIGIBLE_ORIGINAL_NUMERIC_SAMPLE
ROLLING_5D_MAE: N/A_NOT_AUDITED
ROLLING_20D_MAE: N/A_NOT_AUDITED
TODAY_OPEN: PENDING_09:00
DATA_READINESS: DATA_PARTIAL; jp/NIKKEI225 DELAYED (08:12 quote); other JP/KR PASS
SOURCE_CORRECTIONS: AM-1105 time sequencing, same-basis US close returns, preserve valid JP semiconductor despite Nikkei staleness; evidenced in morning.json and visible report.
QUALITY_CHECK: NOT_EXECUTED; six closes manually compared against daily_ohlcv.data.close and stock_close_table_markdown.
PUBLICATION_STATUS: 08:28:20 file-changing commit confirmed; exact data ref readback.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-10-AM","parent_report_id":"2026-11-09-PM","updated_at_taipei":"2026-11-10T08:43:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"reports/2026-11-09/evening.json","observed_at":"2026-11-09","detail":"Taiwan semiconductor +5.40% vs TAIEX +4.94%"},{"source":"reports/2026-11-10/morning.json","observed_at":"2026-11-10T08:28:00+08:00","detail":"SOX +6.85%, TSM +3.51%; KR SK Hynix +8.63%, JP Advantest +4.56%; counterpoint NVDA -4.27%"}],"change_reason":"Maintain prior rejection of short-term relative weakness; external rebound supports but does not prove Taiwan today's result.","next_check":"2026-11-10 Taiwan semiconductor versus TAIEX and breadth at close","falsifier":"Taiwan semiconductor underperforms with weakening breadth"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"reports/2026-11-09/evening.json","observed_at":"2026-11-09","detail":"00631L margin -305 native lots, 0050 margin -400; TWSE aggregate +115481 native lots"}],"change_reason":"No new same-day Taiwan credit balances; previous mixed credit evidence unchanged.","next_check":"2026-11-10 close credit balance and price changes","falsifier":"Sustained price recovery and reduced credit risk"}],"pending_checks":[],"corrections_applied":[{"id":"AM-1105-TIME","evidence":"04:59 TX night observation separated from 08:27-08:28 Asian quotes"},{"id":"AM-1105-CHANGE","evidence":"US completed regular-session close-to-close percentage returns taken from us_regular_close"},{"id":"AM-1105-COVERAGE","evidence":"Nikkei STALE while TOPIX and Japanese semiconductor observations retained"}]}
[/RESEARCH_STATE]
