# Public market prediction ledger — 2026-10-25 PM
REPORT_ID: 2026-10-25-PM
PARENT_REPORT_ID: 2026-10-25-AM
PARENT_LEDGER_PATH: predictions/2026-10-25/morning.md
PARENT_LEDGER_STATUS: VALID_ZERO_PREDICTIONS
REPORT_TARGET_TIME: 2026-10-25T23:00:00+08:00
DATA_CUTOFF: 2026-10-25T22:58:00+08:00
MARKET_SESSION_STATUS: TAIWAN_WEEKEND_CLOSED; US_SUNDAY_CLOSED
LATEST_TW_SESSION: 2026-10-22
NEXT_EXPECTED_TW_SESSION: 2026-10-27
DATA_REPORT_ID: MISSING
DATA_READINESS: DATA_PARTIAL
DATA_PACKAGE_PATH: reports/2026-10-25/evening.json
DATA_PACKAGE_STATUS: NOT_FOUND
DATA_GENERATED_AT: MISSING
DATA_INPUT_FINGERPRINTS: MISSING
DATA_SECTIONS: required_stock_data=NOT_EVALUATED_NO_CURRENT_PACKAGE_MARKET_CLOSED; market_context=NOT_EVALUATED_NO_CURRENT_PACKAGE_MARKET_CLOSED; us_intraday=MARKET_CLOSED_NO_CURRENT_PACKAGE; tx_live=MARKET_CLOSED_NO_VALID_TICK; cutoff=UNVERIFIABLE_NO_PACKAGE
HISTORICAL_REFERENCE_PACKAGE: reports/2026-10-22/evening.json
HISTORICAL_REFERENCE_STATUS: DATA_PARTIAL; required_stock_data=PASS only for 2026-10-22; generated 2026-10-22T23:21:42.759979+08:00 AFTER 22:58 cutoff
US_FRIDAY_CLOSE_DATE: 2026-10-23
US_FRIDAY_CLOSE_SP500: 7623.68
US_FRIDAY_CLOSE_NASDAQ: 25955.34
US_FRIDAY_CLOSE_DOW: 52215.16
US_FRIDAY_CLOSE_SOURCE: Reuters/AP 2026-10-23
US_SOX_HISTORICAL_5M: 10779.4638671875; 2026-10-24T04:00:00+08:00; not exchange-certified formal close
US_INTRADAY_STATUS: MARKET_CLOSED; latest available historical bar STALE relative to 2026-10-25T23:00+08:00
TX_NIGHT_STATUS: MARKET_CLOSED; no valid Sunday TXFR1 tick
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: true

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
SCOREABLE_PREDICTIONS: NONE
REASON: Sunday 2026-10-25 has no Taiwan or US regular trading session; Friday 2026-10-23 Taiwan was typhoon-closed and Monday 2026-10-26 is a scheduled Taiwan holiday. The 2026-10-25 evening contract is missing. A US trading session on 2026-10-26 remains before Taiwan 2026-10-27 reopening, so directional forecasts without fresh evidence would not be calibrated. The following are non-scoreable watch conditions, not predictions.
NON_SCOREABLE_WATCH_ID: 2026-10-25-PM-WATCH-MKT | 原文=2026-10-27台股復市時以2026-10-22加權收盤46041.43點作為歷史參考，依開盤高於46271.64、介於45811.22至46271.64、低於45811.22三情境觀察，不把歷史價當成即時訊號。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=46041.43；高開>46271.64；低開<45811.22 | 期間=2026-10-27日盤或下一實際交易日 | 失效條件=復市改期、開盤資料缺漏、正式量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-25-PM-WATCH-LEVERAGE | 原文=2026-10-27觀察00631L是否跌破2026-10-22歷史低點35.59元及2330是否跌破2385元；須結合正式成交量與市場廣度，不能以週末舊行情直接交易。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=00631L 35.59元；2330 2385元 | 期間=2026-10-27日盤或下一實際交易日 | 失效條件=交易日改期、正式行情缺漏、量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-25-PM-WATCH-SEMIS | 原文=2026-10-27觀察3707是否跌破70.30元、5483是否跌破185.50元，並在法人與融資資料公布後驗證是否持續弱勢，不將10月22日法人當成10月27日新流向。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=3707 70.30元；5483 185.50元 | 期間=2026-10-27日盤或下一實際交易日 | 失效條件=交易日改期、正式資料缺漏或價格結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-10-25-PM
PARENT_REPORT_ID: 2026-10-25-AM
PARENT_SOURCE: predictions/2026-10-25/morning.md
PARENT_STATUS: VALID_ZERO_PREDICTIONS; both original blocks present and PREDICTION_COUNT=0; eight non-scoreable watch IDs
PARENT_VERIFICATION: NOT_SCOREABLE; no original directional forecasts; no HIT/MISS or weighted score
CURRENT_VERIFICATION: NOT_SCOREABLE; PREDICTION_COUNT=0
ROLLING_5D_SCORE: MISSING
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING
TOP3_PRECISION: MISSING
DATA_ERROR_1: reports/2026-10-25/evening.json NOT_FOUND; schema/readiness.sections/input_fingerprints/generated_at unavailable.
DATA_ERROR_2: 2026-10-25/cross-evening.json and 2026-10-25/evening.json NOT_FOUND.
DATA_ERROR_3: Sunday Taiwan and US regular markets closed; no same-day stock OHLCV, Taiwan institutional flow, or valid TXFR1 night tick.
DATA_ERROR_4: 2026-10-22 historical report contract DATA_PARTIAL; required_stock_data PASS only for 2026-10-22, generated AFTER_CUTOFF, not current readiness.
DATA_ERROR_5: 2026-10-24 cross-nightclose.json Yahoo 5m bars are historical, including extended-hours observations; not official US formal close or Sunday live quotes.
DATA_ERROR_6: No current report package means 2026-10-25 22:58 cutoff and sections cannot be verified.
NEXT_CHECK: Verify 2026-10-27 Taiwan reopening, 2026-10-26 US market session, fresh 2026-10-27 report contract and TX tick; keep historical ledger immutable.
[/ROLLING_ERROR_LOG]
