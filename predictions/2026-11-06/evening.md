# Public evening prediction ledger — 2026-11-06
REPORT_ID: 2026-11-06-PM
PARENT_REPORT_ID: 2026-11-06-AM
DATA_REVISION_PIN: 4af1bc2886a37aa7e4f35979717702ae0c0899d8
DATA_PACKAGE: reports/2026-11-06/evening.json
PUBLIC_ONLY: TRUE
[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
NO_NEW_SCORED_FORECAST: TRUE
Original: 2026-11-06 no formal next-session point, direction, price, or stock prediction issued. Uncalibrated model and severe breadth/credit uncertainty; abstention is not a forecast hit.
Direction: ABSTAIN
Confidence: UNCALIBRATED
Threshold: N/A
Verification: next Taiwan trading session; not scoreable.
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
OPEN_ID: OPEN-20261106-AM
OPEN_ORIGINAL: center N/A, delta N/A, interval N/A, confidence UNCALIBRATED; previous close 41574.72; no ex-ante numeric model.
OPEN_ACTUAL_PROVIDER: 38915.76; delta -2658.96; -6.3956%; source FinMind TAIEX 2026-11-06, not official-direct.
OPEN_SIGNED_ERROR: N/A; ABS_ERROR: N/A; DIRECTION: UNVERIFIABLE; INTERVAL: UNVERIFIABLE.
ROLLING_5_20: NOT_AUDITED; do not invent n or scores.
MORNING_PREDICTION_COUNT: 1; only OPEN abstention, unscoreable.
PARENT_2026-11-05-PM: no scored forecast; preserved abstention.
MARKET: TAIEX 39701.64 versus prior 41574.72; -4.5054%; TWSE stock-only 105 up / 952 down; TWSE+TPEx institution net -108821460011 TWD.
SIX_CLOSES: 0050=92.50;006208=210.10;00631L=26.30;2330=2135.00;3707=50.90;5483=144.50; source exact-session daily_ohlcv.data.close.
DATA_READINESS: DATA_PARTIAL because VIX bar at 22:35 is 25min old at 23:00 (DELAYED); TX tick at 22:54:01 is <10min at 23:00, reassess actual completion.
OUTPUT_CHECK: manual comparison to bundle stock_close_table_markdown, automated report_output_quality.py not run.
100_POINT_SCORE: N/A; preserve weights 25/25/15/25/10.
NEXT_CHECK: exact source/publication timing, fresh US VIX and TX tick, next-session breadth and credit, historical open prediction eligibility.
[/ROLLING_ERROR_LOG]
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-06-PM","parent_report_id":"2026-11-06-AM","updated_at_taipei":"2026-11-06T23:00:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"半導體相對弱勢與全球重新定價","status":"WATCH","evidence":[{"source":"reports/2026-11-06/evening.json","observed_at":"2026-11-06T22:54:07+08:00","detail":"半導體類股-4.71%，加權-4.51%，電子零組件-7.12%；2330收2135，外資淨賣22844481股"}],"change_reason":"半導體略弱於大盤，支持弱勢但不能推論訂單下降","next_check":"下一交易日半導體相對大盤、法人及廣度","falsifier":"半導體持續跑贏大盤且廣度轉強"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"槓桿ETF與融資波動放大","status":"WATCH","evidence":[{"source":"reports/2026-11-06/evening.json","observed_at":"2026-11-06T22:54:07+08:00","detail":"00631L 29.21跌至26.30，融資原生單位增加28400；0050融資增加10673"}],"change_reason":"價格急跌且融資增加，風險升高但未證實斷頭","next_check":"下一交易日00631L與0050信用餘額和價格","falsifier":"信用餘額回落且價格穩定"}],"pending_checks":[],"corrections_applied":[{"id":"AM-1105-TIME","evidence":"沿用晨報TX完成夜盤04:59與亞洲08:27-08:28分離的觀察口徑"},{"id":"CLOSE-DAILY-1106","evidence":"六檔收盤逐項對照2026-11-06 evening.json daily_ohlcv.data.close及stock_close_table_markdown"}]}
[/RESEARCH_STATE]
