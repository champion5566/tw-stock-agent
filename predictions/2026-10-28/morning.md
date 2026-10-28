# Public market prediction ledger — 2026-10-28 AM
REPORT_ID: 2026-10-28-AM
PARENT_REPORT_ID: 2026-10-27-PM
PARENT_LEDGER_PATH: predictions/2026-10-27/evening.md
PARENT_LEDGER_STATUS: VERIFIED_ORIGINAL_TWO_BLOCKS; TWO_2026-10-28_CLOSE_FORECASTS_PENDING
REPORT_TARGET_TIME: 2026-10-28T08:40:00+08:00
DATA_CUTOFF: 2026-10-28T08:38:00+08:00
DATA_PACKAGE_PATH: reports/2026-10-28/morning.json
DATA_REPORT_ID: MISSING
DATA_READINESS: DATA_PARTIAL
DATA_PACKAGE_STATUS: NOT_FOUND_AT_REPORT_CHECK
DATA_PACKAGE_GENERATED_AT: MISSING
DATA_INPUT_FINGERPRINTS: MISSING
DATA_SECTIONS: required_stock_data=MISSING_CURRENT_PACKAGE; market_context=MISSING_CURRENT_PACKAGE; us_regular_close=MISSING_CURRENT_PACKAGE_SUPPLEMENTAL_WEB_VERIFIED; asia_open=MISSING_2026-10-28_0820_QUOTES; tx_completed_night=MISSING_CURRENT_SESSION; cutoff=UNVERIFIABLE_NO_PACKAGE
HISTORICAL_REFERENCE_PACKAGE: reports/2026-10-27/evening.json
HISTORICAL_REFERENCE_GENERATED_AT: 2026-10-27T23:33:10.324342+08:00
HISTORICAL_REFERENCE_STATUS: DATA_PARTIAL; required_stock_data=PASS but generated AFTER 22:58 cutoff; not a current morning package
TW_PREVIOUS_CLOSE: 2026-10-27 TAIEX 46096.23 (+54.80), reported by CNA; direct TWSE 2026-10-27 table not separately fetched
US_REGULAR_CLOSE_REFERENCE: 2026-10-27 US 16:00 EDT = 2026-10-28 04:00 Taipei; Nasdaq 26477.81 (+1.18%), S&P500 7722.60 (+0.60%), SOX +3.6% (FT), TSM ADR 436.87 (+2.95%, stockanalysis); NVDA 217.94 (+0.90%), AVGO 342.33 (+4.00%)
ASIA_2026-10-28_OPEN: UNVERIFIED; do not substitute 2026-10-27 closes or TOPIX ETF proxy
TX_COMPLETED_NIGHT: UNVERIFIED; no fresh timestamp or reliable basis
FORECAST_METHOD: Uncalibrated low-confidence heuristic: US semiconductor/TSM strength positive, discounted for 2026-10-27 Taiwan opening fade and absent current TX/Asia quotes. Numeric contribution weights are estimates, NOT measured coefficients.
FORECAST_INPUT_OBSERVATION_TIME: US 2026-10-28T04:00:00+08:00; Taiwan 2026-10-27T13:30:00+08:00; Asia/TX not verified
FORECAST_CREATION_TIMESTAMP: REPORT_TARGET_TIME=2026-10-28T08:40:00+08:00; precise execution timestamp not independently verified
POINT_IN_TIME_VERIFIED: false
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
SCOREABLE_PREDICTIONS: 2
PREDICTION_ID: OPEN-20261028-AM
原始字句: 預測2026-10-28臺灣證券交易所加權股價指數09:00正式開盤指數為46,340.00點，較2026-10-27正式收盤46,096.23點上漲+243.77點（+0.529%）；預測區間46,060.00至46,620.00點，信心34%。
方向: UP_OPEN
信心: 0.34
預測開盤點位: 46340.00
預測漲跌點: +243.77
預測漲跌幅: +0.529%
預測區間: 46060.00..46620.00
前收基準: 46096.23 (2026-10-27)
數字門檻: official TAIEX 09:00 opening index; predicted center=46340.00; interval=[46060.00,46620.00]
期間: 2026-10-28 regular session 09:00 opening; postponed session follows next actual opening without changing baseline
失效條件: actual open <=46096.23 means UP direction MISS; actual open outside [46060,46620] means interval MISS; center point error=actual-predicted
驗證時點: 2026-10-28T23:00:00+08:00 or next actual trading session
當時證據: 2026-10-27 TAIEX 46096.23, US Nasdaq +1.18%, S&P500 +0.60%, SOX +3.6%, TSM ADR +2.95%; prior Taiwan day opening 46211.20 faded to close 46096.23; current TX basis and 08:20+ JP/KR quotes unavailable; scenario interval widened for missing inputs
分類: LOW_CONFIDENCE_HEURISTIC; NOT_POINT_IN_TIME_VERIFIED

PREDICTION_ID: 2026-10-28-AM-2330-OPEN-01
原始字句: 預測2026-10-28台積電2330正式開盤價高於2026-10-27正式收盤價2,400元。
方向: UP_OPEN
信心: 0.52
數字門檻: TWSE 2330 opening price > TWD 2400
期間: 2026-10-28 regular opening or next actual session
失效條件: official opening price <= TWD 2400 means MISS; missing official opening price means UNVERIFIABLE
驗證時點: 2026-10-28T23:00:00+08:00
當時證據: 2026-10-27 2330 FinMind close 2400; 2026-10-27 US TSM ADR regular close 436.87 (+2.95%); previous ADR-positive 2026-10-27 morning 2330 forecast missed, so confidence discounted
分類: LOW_CONFIDENCE_HYPOTHESIS

NON_SCOREABLE_WATCH_ID: 2026-10-28-AM-WATCH-FLOW | 原文=等當日正式外資、投信、自營商淨額與Top3流向公開後才判斷資金，盤前不將昨日法人資料當今日資金流。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 門檻=official 2026-10-28 institutional flow | 期間=當日日盤 | 失效條件=資料缺漏 | 驗證時間=2026-10-28T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-28-AM-WATCH-0050 | 原文=0050觀察昨日低點105.80與高點107.55；未突破不追價，跌破低點視為轉弱。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 門檻=105.80/107.55 | 期間=當日日盤 | 失效條件=當日正式量價結構改變 | 驗證時間=2026-10-28T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-28-AM-WATCH-006208 | 原文=006208觀察昨日低點242.95與高點247.75；未確認量價突破前不追高。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 門檻=242.95/247.75 | 期間=當日日盤 | 失效條件=當日正式量價結構改變 | 驗證時間=2026-10-28T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-28-AM-WATCH-00631L | 原文=00631L觀察昨日低點35.23與高點36.25；槓桿ETF高開勿無條件追價。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 門檻=35.23/36.25 | 期間=當日日盤 | 失效條件=當日正式量價結構改變 | 驗證時間=2026-10-28T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-28-AM-WATCH-2330 | 原文=2330觀察昨日低點2380與高點2405；2405上方站穩才視為短線突破。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 門檻=2380/2405 | 期間=當日日盤 | 失效條件=當日正式量價結構改變 | 驗證時間=2026-10-28T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-28-AM-WATCH-3707 | 原文=3707觀察昨日低點68.30與高點72.00；跌破68.30維持弱勢。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 門檻=68.30/72.00 | 期間=當日日盤 | 失效條件=當日正式量價結構改變 | 驗證時間=2026-10-28T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-28-AM-WATCH-5483 | 原文=5483觀察昨日低點183.50與高點193.50；突破193.50前不視為反轉。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 門檻=183.50/193.50 | 期間=當日日盤 | 失效條件=當日正式量價結構改變 | 驗證時間=2026-10-28T23:00:00+08:00
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-10-28-AM
PARENT_REPORT_ID: 2026-10-27-PM
PARENT_SOURCE: predictions/2026-10-27/evening.md
PARENT_STATUS: VERIFIED_ORIGINAL_LEDGER_WITH_TWO_2026-10-28_CLOSE_FORECASTS
PARENT_PREDICTION_1: 2026-10-27-PM-MKT-01; original threshold official 2026-10-28 TAIEX close <46096.23; PENDING
PARENT_PREDICTION_2: 2026-10-27-PM-5483-01; original threshold official 2026-10-28 5483 close <=184.50; PENDING
PRIOR_OPEN_RECAP: 2026-10-27 original 2026-10-27-AM-MKT-OPEN-01 direction UP vs actual 46211.20 above 46041.43, provisional HIT; 2330 original 2026-10-27-AM-2330-OPEN-01 predicted open >2385 vs actual 2380, MISS; original numeric point forecast missing, no MAE
CURRENT_OPEN_POINT_FORECAST: OPEN-20261028-AM center 46340.00, baseline 46096.23, +243.77, +0.529%, interval [46060,46620], confidence 34%, scheduled 08:40, official 09:00 verification pending
ROLLING_5D_POINT_MAE: N/A no 5 original verified numeric forecasts
ROLLING_20D_POINT_MAE: N/A no 20 original verified numeric forecasts
ROLLING_5D_SCORE: MISSING
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING
TOP3_PRECISION: MISSING
DATA_ERROR_1: reports/2026-10-28/morning.json NOT_FOUND; current contract, source timestamps and fingerprints cannot be validated
DATA_ERROR_2: no 2026-10-28 08:20+ JP/KR live opening observations; previous-day market closes are not current quotes
DATA_ERROR_3: no completed 2026-10-28 Taiwan TX night tick with verified source timestamp/basis
DATA_ERROR_4: historical 2026-10-27 evening report generated 23:33 after 22:58 cutoff; cannot inherit its readiness for today
DATA_ERROR_5: no official current-day market-wide institutional flows or six-stock same-day bars before Taiwan open
DATA_ERROR_6: numeric opening forecast uses transparent uncalibrated heuristic; cannot claim empirical calibration or point-in-time verification
NEXT_CHECK: 2026-10-28 23:00 verify OPEN-20261028-AM official opening point, direction, range and point error; verify 2330 opening and parent two closing forecasts; never rewrite original ledger
[/ROLLING_ERROR_LOG]
