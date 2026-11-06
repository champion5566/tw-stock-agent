# Public morning prediction ledger — 2026-11-06
REPORT_ID: 2026-11-06-AM
PARENT_REPORT_ID: 2026-11-05-PM
PARENT_SOURCE: predictions/2026-11-05/evening.md
DATA_REVISION_PIN: e0b9198973003c4024d472b57dc885d171bb3f8a
DATA_PACKAGE: reports/2026-11-06/morning.json
DATA_PACKAGE_GENERATED_AT: 2026-11-06T08:28:15.235405+08:00
PUBLIC_ONLY: TRUE
[PREDICTION_LEDGER]
PREDICTION_COUNT: 1
ID: OPEN-20261106-AM
Target: TWSE TAIEX official 2026-11-06 09:00 opening index.
Prior official provider TAIEX 2026-11-05 close: 41574.72 points.
Predicted center: N/A; signed delta: N/A; signed percent: N/A; interval: N/A; confidence: UNCALIBRATED.
Original direction: ABSTAIN_NUMERIC_FORECAST.
Reason: No previously validated reproducible spot-opening mapping from completed TX futures and cross-market returns to TAIEX opening; Nikkei selected source 08:12 stale, and point-in-time report explicitly unverified. A qualitative risk-off assessment is not a numeric forecast.
Inputs and observation times: TXFR1 Shioaji completed night snapshot 38936 at 2026-11-06 04:59:58.105 +08; US completed 2026-11-05 regular daily close SP500 7353.73 (-4.36%), NASDAQ 24315.00 (-5.52%), SOX 9011.14 (-12.25%), TSM ADR 353.10 (-10.78%), NVDA 181.60 (-9.26%); Japan TOPIX 3728.23 (-5.38%) at 08:27 Taipei, ADVANTEST -12.12% and TOKYO_ELECTRON -9.79% at 08:27; Korea KOSPI 4923.47 (-8.55%), SAMSUNG -9.98%, SK_HYNIX -11.71% at 08:28; Nikkei provider 08:12 STALE, excluded from fresh-index inference.
Method: exact-session provider daily close-to-close percentage returns for US; regional quote percentage changes with original timestamps; qualitative risk ranking only; no numerical index-opening regression or calibrated error distribution available. Futures minus spot is NOT a calibrated basis.
Data cutoff: 2026-11-06 08:38 +08; verification time: 2026-11-06 09:00 official TWSE opening observation.
Formal score: UNSCOREABLE_NO_NUMERIC_EX_ANTE_PREDICTION.
Invalidation/next check: official 09:00 opening, 2330 opening and listed breadth; test whether global semiconductor risk transmits into Taiwan or a contemporaneous rebound emerges.
No other new scored market or stock predictions: uncalibrated confidence and lack of robust actionable edge.
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
PARENT_REPORT_ID: 2026-11-05-PM
PARENT_PREDICTION_COUNT: 0
PARENT_STATUS: VALID_ORIGINAL_THREE_BLOCKS
PARENT_ABSTENTION: preserved, not retroactively scored.
HISTORICAL_REVIEW: evaluations/ledger-review-historical-20261105.json inspected; PROVIDER_MATCHED outcome is not official direct, ex-ante eligibility or profit.
TODAY_OPEN_MAE: N/A_NO_NUMERIC_PREDICTION
FORMAL_SCORE_100: N/A_NO_COMPLETE_VERIFIABLE_CATEGORY_COVERAGE; weights retained 25/25/15/25/10.
DATA_EXCEPTION: 2026-11-06 morning bundle readiness DATA_PARTIAL because jp/NIKKEI225 delayed/stale; TOPIX, ADVANTEST, TOKYO_ELECTRON and Korean observations independently PASS.
DATA_EXCEPTION: broker 04:59 completed TX cannot establish resistance to 08:27-08:28 Asia selling; no contemporaneous basis.
DATA_EXCEPTION: 2026-11-05 evening bundle generated 23:43:43 after 22:58 cutoff; cannot be backdated to parent forecast eligibility.
DATA_EXCEPTION: report_output_quality.py not executed in this connector-only run; six closes checked directly against exact-date daily_ohlcv.data.close and stock_close_table_markdown.
CORRECTIONS_APPLIED: AM-1105-TIME, AM-1105-CHANGE, AM-1105-COVERAGE; evidence is 2026-11-06 data revision and explicit dated comparison; this does not prove improved predictive performance.
[/ROLLING_ERROR_LOG]
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-06-AM","parent_report_id":"2026-11-05-PM","updated_at_taipei":"2026-11-06T08:40:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Global semiconductor repricing may drive Taiwan's electronics weakness; no order-collapse evidence","status":"WATCH","evidence":[{"source":"reports/2026-11-06/morning.json us_regular_close and asia_open","observed_at":"2026-11-06T08:28:00+08:00","detail":"SOX -12.25%, TSM ADR -10.78%, TOPIX -5.38%, Advantest -12.12%, KOSPI -8.55%, SK Hynix -11.71%"}],"change_reason":"Stronger cross-region contemporaneous selloff evidence; TX 04:59 predates Asia moves","next_check":"2026-11-06 Taiwan regular close: semiconductor index daily return versus TAIEX daily return and TWSE stock-only breadth","falsifier":"Semiconductor index outperforms TAIEX and TWSE breadth turns positive"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leverage can amplify volatility, but balance changes alone do not prove margin liquidation","status":"WATCH","evidence":[{"source":"reports/2026-11-06/morning.json stocks/00631L and stocks/0050","observed_at":"2026-11-06T08:23:50+08:00","detail":"00631L 2026-11-05 close 29.21, 0050 close 97.15, 0050 native margin +4009 lots; distinct instruments and units"}],"change_reason":"Exact-date daily prices confirm further weakness, no causal liquidation proof","next_check":"2026-11-06 completed-session 00631L return and native margin balance changes versus 0050","falsifier":"No further relative dislocation despite credit contraction"}],"pending_checks":[],"corrections_applied":[{"id":"AM-1105-TIME","evidence":"TX 04:59 explicitly earlier than JP/KR 08:27-08:28"},{"id":"AM-1105-CHANGE","evidence":"US 2026-11-05 exact regular-session close-to-close returns included"},{"id":"AM-1105-COVERAGE","evidence":"Nikkei stale isolated; valid TOPIX, Advantest and Tokyo Electron preserved"}]}
[/RESEARCH_STATE]