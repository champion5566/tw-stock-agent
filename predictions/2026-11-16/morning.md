# 2026-11-16 morning public original ledger
REPORT_ID: 2026-11-16-AM
OPEN_ID: OPEN-20261116-AM
PARENT_REPORT_ID: 2026-11-15-PM
SNAPSHOT_SHA: 972c8bd7ba009992f51e38f50c5f2a04695511dc
SOURCE_BUNDLE: reports/2026-11-16/morning.json
SOURCE_GENERATED: 2026-11-16T08:28:14.727467+08:00
INPUT_CUTOFF: 2026-11-16T08:38:00+08:00
TARGET_DELIVERY: 2026-11-16T08:40:00+08:00
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN-20261116-AM: target TWSE official TAIEX 09:00 opening 2026-11-16; previous TWSE close 2026-11-13 43675.12 (TWSE MI_5MINS_HIST historical provider bundle). CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; METHOD=No calibrated reproducible spot-open mapping; no numerical prediction; INPUTS=2026-11-13 US regular-session closes, 2026-11-13 TWSE close, completed TXFR1 night observation 2026-11-14 04:59:59 Taipei, Asia observations 2026-11-16 08:27-08:28 Taipei; VERIFY_AT=2026-11-16 09:00 TWSE official open; ELIGIBILITY=NOT_SCORED.
NEW_FORMAL_PREDICTIONS: NONE. Directional research is not a scored opening estimate.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-16-AM
PARENT: 2026-11-15-PM original has zero formal predictions and retains 5/20 calibration audit pending.
ROLLING_5_20: NOT_AUDITED; n unknown. SCORE_100: N/A; weights 25/25/15/25/10 retained.
SIX_CLOSES_2026_11_13: 0050=102.50;006208=235.05;00631L=31.92;2330=2350.00;3707=59.50;5483=162.50; from stock_close_table_markdown/daily_ohlcv.data.close.
US_REGULAR_2026_11_13: SP500 -0.40%;NASDAQ -0.91%;SOX -3.43%;TSM_ADR -1.67%;NVDA -2.01%;AMD -8.75%;AVGO -4.76%;MU -2.52%;VIX +3.21%; completed Yahoo/yfinance daily bars, not official direct.
ASIA_2026_11_16: TOPIX -0.06%, Advantest -6.91%, Tokyo Electron -3.02% at 08:27; KOSPI -0.31%, Samsung -0.24%, SK Hynix -1.56% at 08:28; Nikkei 08:12 STALE.
TXFR1: 43706 at 2026-11-14 04:59:59 completed night; not current and not contemporaneous basis.
SOURCE_STATUS: DATA_PARTIAL (Nikkei stale); bundle generated 08:28:14; branch commit dated 08:28:20.
OUTPUT_QUALITY: automated report_output_quality.py NOT_EXECUTED; six printed closes manually compared to stock_close_table_markdown and JSON.
HISTORICAL_DEFECT: 2026-11-13 PM source generated six seconds past 22:58; cannot retroactively qualify.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-16-AM","parent_report_id":"2026-11-15-PM","updated_at_taipei":"2026-11-16 08:36 Taipei","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor relative weakness persists","status":"WATCH","evidence":[{"source":"reports/2026-11-16/morning.json","observed_at":"2026-11-13 US regular close / 2026-11-16 08:27-08:28 Asia","detail":"SOX -3.43%, AMD -8.75%; Advantest -6.91%, Tokyo Electron -3.02%, SK Hynix -1.56%; Friday Taiwan semiconductor +1.23% versus TAIEX +1.35%"}],"change_reason":"Reopen WATCH from parent REJECT because new overseas semiconductor underperformance creates a material new test, not proof Taiwan already weakened","next_check":"2026-11-16 TWSE semiconductor relative return and breadth at close","falsifier":"Semiconductor outperformance and improving breadth despite overseas weakness"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"predictions/2026-11-15/evening.md","observed_at":"2026-11-13","detail":"00631L 31.92, margin +820 native units, five-day -63024"}],"change_reason":"No newer Taiwan margin data; retain WATCH","next_check":"2026-11-16 00631L exact-session price and margin balances","falsifier":"Sustained price recovery alongside declining credit balances"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"Formal 5/20 opening sample eligibility and calibration unknown"},{"id":"CUTOFF-DEFECT","detail":"2026-11-13 evening late source remains unqualified"}],"corrections_applied":[{"id":"AM-1105-TIME","evidence":"Explicit TX 04:59 versus Asia 08:27-08:28 observation order"},{"id":"AM-1105-CHANGE","evidence":"US previous/current dated regular closes and returns from deterministic table"},{"id":"AM-1105-COVERAGE","evidence":"Nikkei stale independently of valid TOPIX/Japan semiconductors"}]}
[/RESEARCH_STATE]
