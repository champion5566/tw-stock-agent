# Non-trading-day morning status — 2026-11-07
REPORT_ID: 2026-11-07-AM
PARENT_REPORT_ID: 2026-11-06-PM
DATA_REVISION_PIN: 94996f4f605aaefe815ed87e7fc11fa22bab6a07
STATUS: MARKET_CLOSED_WEEKEND
PUBLIC_ONLY: TRUE
[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
OPEN_ID: OPEN-20261107-AM
TARGET: TWSE 2026-11-07 09:00 official opening
CENTER: N/A
DELTA_POINTS: N/A
DELTA_PCT: N/A
RANGE: N/A
CONFIDENCE: N/A
LAST_COMPLETED_TAIEX_CLOSE: 39701.64 (2026-11-06, FinMind provider)
METHOD: NO_FORECAST; Saturday has no TWSE regular trading session.
INPUT_AS_OF: 2026-11-07 08:38 Asia/Taipei; pinned snapshot above.
VERIFICATION: NOT_APPLICABLE; no 09:00 TWSE open on Saturday.
FORMAL_SAMPLE_ELIGIBLE: false
[/PREDICTION_LEDGER]
[ROLLING_ERROR_LOG]
PARENT: 2026-11-06-PM read and contains all three original sections.
PARENT_NEW_SCORED_FORECASTS: 0
PRIOR_OPEN_20261106_AM: unscoreable N/A; provider observed 38915.76; no signed forecast error.
CURRENT_OPEN: N/A_MARKET_CLOSED_WEEKEND
ROLLING_5_20: NOT_AUDITED
SCORE_100: N/A (25/25/15/25/10 components cannot be scored without eligible original predictions/outcomes)
DATA: 2026-11-07 morning report not generated as Saturday closed; 2026-11-06 evening bundle DATA_PARTIAL, VIX delayed.
CORRECTIONS: AM-1105-TIME: nightclose 5-minute bars are not certified US regular close; weekend no Asia cash open. CLOSE-DAILY-1106: use same-session daily_ohlcv.data.close.
[/ROLLING_ERROR_LOG]
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-07-AM","parent_report_id":"2026-11-06-PM","updated_at_taipei":"2026-11-07T08:40:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"半導體相對弱勢與全球重新定價","status":"WATCH","evidence":[{"source":"reports/2026-11-06/evening.json","observed_at":"2026-11-06T22:54:07+08:00","detail":"台股半導體類股-4.71%對加權-4.51%，電子零組件-7.12%"}],"change_reason":"週末無台股新交易日，不將美股延長時段K棒當正常盤收盤","next_check":"2026-11-09交易日台股半導體相對大盤、廣度與法人","falsifier":"半導體持續跑贏大盤且廣度轉強"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"槓桿ETF與融資波動放大","status":"WATCH","evidence":[{"source":"reports/2026-11-06/evening.json","observed_at":"2026-11-06T22:54:07+08:00","detail":"00631L收26.30，0050融資增加10673原生張"}],"change_reason":"週末無新信用餘額，不能推論斷頭","next_check":"2026-11-09交易日信用餘額和價格","falsifier":"信用餘額回落且價格穩定"}],"pending_checks":[],"corrections_applied":[{"id":"AM-1105-TIME","evidence":"週末不把06:10美股盤後5m K棒冒充正式收盤"},{"id":"CLOSE-DAILY-1106","evidence":"六檔收盤以2026-11-06 evening.json stock_close_table_markdown與daily_ohlcv.data.close同口徑"}]}
[/RESEARCH_STATE]
