# 2026-11-11 evening original public ledger
REPORT_ID: 2026-11-11-PM
PARENT_REPORT_ID: 2026-11-11-AM
DATA_PATH: reports/2026-11-11/evening.json
DATA_PINNED_COMMIT: e5a5696f0f4339b2cfc26d38a53e3f46d7c3d38b
DATA_BLOB_SHA: dfec03fe99a2aedb88afbad0642ae3373a674c4d
DATA_GENERATED_AT: 2026-11-11T22:52:13.871783+08:00
DATA_FILE_CHANGED_COMMIT_AT: 2026-11-11T22:52:17+08:00
DATA_READINESS: DATA_PARTIAL; VIX 22:35 bar DELAYED at 23:00, becomes STALE after 23:05; no completion-time refresh certified
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_PARENT_ID: OPEN-20261111-AM
OPEN_PARENT_ORIGINAL: CENTER N/A; DELTA_POINTS N/A; DELTA_PERCENT N/A; INTERVAL N/A; CONFIDENCE N/A_UNCALIBRATED; PRIOR_CLOSE 42711.92; DIRECTION ABSTAIN_NUMERIC; DATA_GENERATED_AT 2026-11-11T08:28:17.169048+08:00; INPUT_CUTOFF 08:38.
NO_NEW_SCORED_FORECAST: TRUE
DIRECTION: ABSTAIN
VERIFICATION: NOT_APPLICABLE
RATIONALE: No calibrated reproducible predictive advantage; preserve hypotheses as research state rather than fabricate forecast.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
OPEN_ID: OPEN-20261111-AM
OPEN_ACTUAL_PROVIDER: 43135.76; +423.84 points / +0.99232% versus prior close 42711.92; FinMind same-session TAIEX daily open, corroborated by 2026-11-11 09:03 CNA news; not independently retrieved TWSE official 09:00 raw record.
OPEN_RESULT: UNVERIFIABLE_NO_NUMERIC_FORECAST; signed error/absolute error/direction/interval not scoreable.
ROLLING_5_20: NOT_AUDITED; no verified eligible n, MAE, direction accuracy or interval coverage published; missing full original/outcome audit.
PARENT_PREDICTIONS: 1 OPEN abstention; no HIT/MISS.
PREVIOUS_PM: 2026-11-10-PM PREDICTION_COUNT 0; no matured scored PM prediction.
LATEST_EVALUATION: evaluations/ledger-review-42939212722-1.json as_of 2026-11-11T09:29:56+08:00; historical provider-matched is not formal prediction eligibility; no current-day supported outcome.
SCORE_100: N/A; weights 25/25/15/25/10 unchanged.
MARKET: 2026-11-11 TAIEX close 44257.15 vs prior 42711.92, +1545.23 (+3.62%); semiconductor +4.50%; TWSE stock breadth 634/368; TPEx stock breadth 520/288; scopes not interchangeable with news all-security breadth.
INSTITUTIONAL: TWSE+TPEx combined foreign -2688039684 TWD, trust +20662080753, dealer +7708128219, total +25682169288 TWD; sector price performance is not institutional flow.
CREDIT: TWSE margin -10232 provider-native lots; TPEx margin +19476 separately; 0050 -3061, 00631L -14651 provider-native lots; cannot infer forced liquidation.
CLOSE_SOURCE: exact-session daily_ohlcv.data.close and stock_close_table_markdown only, not broker snapshot; 0050 103.20, 006208 236.60, 00631L 32.53, 2330 2395.00, 3707 60.90, 5483 161.00.
SOURCE_LIMITATIONS: VIX 22:35 bar 25 minutes old at 23:00 (DELAYED); other US 22:50 bars 10 minutes old at target; TXFR1 Shioaji true tick 22:52:12.939, 7m47s at 23:00, >10m after 23:02:12.939; cannot claim completion-time latest. SEC ticker identity lookup 403, SPCX historical mapping not certified. Report generated after 23:00 target; no backfill into morning inputs.
SOURCE_CONFLICT: News turnover approximately 8491.65 億元 vs package FinMind turnover 8762.95 億元; do not merge or cite as identical scope without reconciliation. News breadth counts differ from stock-only TWSE dataset.
QUALITY_CHECK: NOT_EXECUTED; displayed closes manually checked against exact-session JSON; no automatic PASS claimed.
NEXT_CHECK: 2026-11-12 semiconductor relative return and market breadth, ETF/market credit, institutional totals by scope, US/TX freshness at completion, turnover scope reconciliation.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-11-PM","parent_report_id":"2026-11-11-AM","updated_at_taipei":"2026-11-11T23:04:32+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"REJECT","evidence":[{"source":"reports/2026-11-11/evening.json @ e5a5696f0f4339b2cfc26d38a53e3f46d7c3d38b","observed_at":"2026-11-11","detail":"Semiconductor +4.50% vs TAIEX +3.62%, TWSE stock breadth 634 advances/368 declines, TSMC close 2395 (+4.81%)."}],"change_reason":"Retain rejection: domestic semiconductors outperformed despite previous US semiconductor softness; one day does not establish earnings growth or a new persistent regime.","next_check":"2026-11-12 same-session semiconductor minus TAIEX return, TWSE breadth and TSMC institutional net shares","falsifier":"Repeated semiconductor underperformance with worsening breadth would justify reopening the hypothesis."},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF and credit volatility risk","status":"WATCH","evidence":[{"source":"reports/2026-11-11/evening.json @ e5a5696f0f4339b2cfc26d38a53e3f46d7c3d38b","observed_at":"2026-11-11","detail":"00631L close 32.53 (+7.54%) margin -14651 provider-native lots, 0050 close 103.20 (+3.51%) margin -3061; TWSE margin -10232 and TPEx margin +19476 reported separately."}],"change_reason":"ETF credit contracted with price recovery, easing near-term pressure; TPEx margin rose, so no claim of system-wide deleveraging or forced liquidation.","next_check":"2026-11-12 00631L/0050 price, margin balances and separate TWSE/TPEx totals","falsifier":"Sustained price strength with declining ETF and market credit exposure weakens near-term risk; renewed falling price and increasing margin strengthens it."}],"pending_checks":[],"corrections_applied":[{"id":"AM-1105-TIME","evidence":"Preserved 04:59 completed TX observation as historical, not contemporaneous with 08:27-08:28 Asia inputs."},{"id":"AM-1105-CHANGE","evidence":"Morning original 2026-11-11 included dated completed US regular returns."},{"id":"AM-1105-COVERAGE","evidence":"Morning ledger retained valid TOPIX/Advantest/Tokyo Electron/KOSPI despite stale Nikkei; no false all-Asia outage."}]}
[/RESEARCH_STATE]
