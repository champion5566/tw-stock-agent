# Public market prediction ledger — 2026-11-04 PM
REPORT_ID: 2026-11-04-PM
PARENT_REPORT_ID: 2026-11-04-AM
PARENT_SOURCE: predictions/2026-11-04/morning.md
DATA_PACKAGE_PATH: reports/2026-11-04/evening.json
DATA_PACKAGE_STATUS: MISSING_404_AT_2300_CHECK
DATA_READINESS: DATA_PARTIAL
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
PREDICTION_ID: 2026-11-04-PM-MKT-01
原始字句: 預測2026-11-05臺灣證交所加權指數正常交易日官方收盤低於2026-11-04收盤42,948.91點。
方向: DOWN
信心: 0.50 LOW
數字門檻: TAIEX official close <42948.91
期間: 2026-11-05 regular session
失效條件: Official close >=42948.91; missing official close makes UNVERIFIABLE
驗證時點: 2026-11-05 23:00 Asia/Taipei
證據: 2026-11-04 close 42948.91, low 41855.82, high 43741.54, volume value TWD 11148.21 billion, CNA 13:48; large intraday reversal.
反證: Recovery from intraday low 41855.82 to close 42948.91 suggests dip-buying; US/TX current data unavailable.
分類: LOW_CONFIDENCE_HYPOTHESIS

PREDICTION_ID: 2026-11-04-PM-2330-01
原始字句: 預測2026-11-05台積電2330正常交易日官方收盤低於2026-11-04收盤2,260元。
方向: DOWN
信心: 0.50 LOW
數字門檻: TWSE 2330 official close <2260.00
期間: 2026-11-05 regular session
失效條件: Official close >=2260.00; missing official close makes UNVERIFIABLE
驗證時點: 2026-11-05 23:00 Asia/Taipei
證據: 2026-11-04 TSMC close 2260, down 35 from 2295; Yahoo secondary market report.
反證: Intraday rebound from 2235; current US TSM ADR and TX night tick unavailable.
分類: LOW_CONFIDENCE_HYPOTHESIS
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-04-PM
PARENT_REPORT_ID: 2026-11-04-AM
PARENT_STATUS: VALID_ORIGINAL_TWO_BLOCKS
OPEN_PREDICTION_ID: OPEN-20261104-AM
OPEN_ORIGINAL_CENTER: N/A
OPEN_ORIGINAL_CHANGE: N/A
OPEN_ORIGINAL_PERCENT: N/A
OPEN_ORIGINAL_RANGE: N/A
OPEN_ORIGINAL_CONFIDENCE: N/A
OPEN_ORIGINAL_PREVIOUS_CLOSE: 43307.54
OPEN_ORIGINAL_INPUT_CUTOFF: 2026-11-04T08:38:00+08:00
OPEN_ACTUAL: 43449.45; +141.91 (+0.3277%) versus previous close; CNA and NOWnews secondary sources, TWSE direct not verified
OPEN_ERROR_SIGNED: N/A
OPEN_ABSOLUTE_ERROR: N/A
OPEN_DIRECTION_HIT: UNVERIFIABLE
OPEN_INTERVAL_COVERAGE: UNVERIFIABLE
OPEN_TODAY_MAE: N/A n=0/1
OPEN_ROLLING_5_MAE: N/A strict qualified n=0/5 based on accessible parent log, historic audit not independently completed
OPEN_ROLLING_20_MAE: N/A strict qualified n=0/20 based on accessible parent log, historic audit not independently completed
OPEN_ATTRIBUTION: Pre-forecast US semiconductor recovery and completed TX 43779 were known but uncalibrated; Asia FX and opening quotes absent. No numeric forecast to attribute an error to. Do not backfill weights.
PARENT_PREDICTION_1: 2026-11-03-PM-MKT-01; original close <43307.54; actual 42948.91; provisional HIT from CNA secondary, TWSE direct pending
PARENT_PREDICTION_2: 2026-11-03-PM-2330-01; original close <2295; actual 2260; provisional HIT from Yahoo secondary, TWSE direct pending
OFFICIAL_SCORE: UNVERIFIABLE pending primary TWSE data and market ranking
DATA_ERROR_1: reports/2026-11-04/evening.json 404 at scheduled run; no schema/readiness sections available.
DATA_ERROR_2: 2026-11-04/cross-evening.json and evening.json 404.
DATA_ERROR_3: No verified current US five-minute quote and TXFR1 tick within ten minutes.
DATA_ERROR_4: Six stock full OHLCV/metrics/flows not contract verified; market ranking Top3 unavailable.
NEXT_CHECK: Validate 2026-11-05 official TWSE close, refresh real-time US and TX ticks, and audit contract package. Keep historical files immutable.
[/ROLLING_ERROR_LOG]
