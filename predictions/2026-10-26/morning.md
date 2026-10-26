# Public market prediction ledger — 2026-10-26 AM
REPORT_ID: 2026-10-26-AM
PARENT_REPORT_ID: 2026-10-25-PM
PARENT_LEDGER_PATH: predictions/2026-10-25/evening.md
PARENT_LEDGER_STATUS: VALID_ZERO_PREDICTIONS
LAST_COMPLETED_TW_TRADING_SESSION: 2026-10-22
LAST_TRADING_SESSION_EVENING_LEDGER: predictions/2026-10-22/evening.md
LAST_TRADING_SESSION_LEDGER_STATUS: MISSING_FILE
REPORT_TARGET_TIME: 2026-10-26T08:50:00+08:00
DATA_CUTOFF: 2026-10-26T08:45:00+08:00
MARKET_SESSION_STATUS: TAIWAN_HOLIDAY_CLOSED; US_2026-10-26_REGULAR_SESSION_NOT_YET_OPEN
NEXT_EXPECTED_TW_SESSION: 2026-10-27
DATA_REPORT_ID: MISSING
DATA_READINESS: DATA_PARTIAL
DATA_PACKAGE_PATH: reports/2026-10-26/morning.json
DATA_PACKAGE_STATUS: NOT_FOUND
DATA_GENERATED_AT: MISSING
DATA_INPUT_FINGERPRINTS: MISSING
DATA_SECTIONS: required_stock_data=MISSING_CURRENT_PACKAGE_MARKET_CLOSED; market_context=MISSING_CURRENT_PACKAGE_MARKET_CLOSED; us_regular_close=MISSING_CURRENT_PACKAGE_HISTORICAL_REFERENCE_ONLY; asia_open=MISSING_CURRENT_PACKAGE_UNVERIFIED; tx_completed_night=MARKET_CLOSED_NO_NEW_NIGHT_SESSION; cutoff=UNVERIFIABLE_NO_PACKAGE
HISTORICAL_REFERENCE_PACKAGE: reports/2026-10-22/evening.json
HISTORICAL_REFERENCE_STATUS: DATA_PARTIAL; required_stock_data=PASS for 2026-10-22 only; generated 2026-10-22T23:21:42.759979+08:00 after its 22:58 cutoff
US_REFERENCE: 2026-10-23 regular-session daily close via 2026-10-24/cross-nightclose.json; not 2026-10-26 close
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 0
SCOREABLE_PREDICTIONS: NONE
REASON: Taiwan markets closed 2026-10-26 for Taiwan Retrocession Day observed holiday, 2026-10-23 closed for typhoon, and 2026-10-24/25 weekend. Current morning data contract missing; US 2026-10-26 regular session remains ahead of Taiwan reopening 2026-10-27. No verified directional edge; conditions below are non-scoreable watches, not forecasts.
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-MKT | 原文=2026-10-27復市先觀察加權指數相對2026-10-22收盤46041.43點的高平低開位置，不能將10月26日休市價當成行情。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=46041.43點；高開>46271.64；低開<45811.22 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-FLOW | 原文=2026-10-27正式外資買賣超公布後，以淨額0億元判斷資金流向，不沿用10月22日法人資料。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=外資淨額0億元 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-0050 | 原文=2026-10-27觀察0050相對10月22日低點106.75元與高點109.15元的價格反應，並待成交量確認。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=106.75與109.15元 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-006208 | 原文=2026-10-27觀察006208相對10月22日低點244.70元與高點249.90元的價格反應，並待成交量確認。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=244.70與249.90元 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-00631L | 原文=2026-10-27觀察00631L相對10月22日低點35.59元與高點37.00元的價格反應，留意槓桿風險。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=35.59與37.00元 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-2330 | 原文=2026-10-27觀察2330相對10月22日低點2385元與高點2435元的價格反應，並核對TSM及量價。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=2385與2435元 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-3707 | 原文=2026-10-27觀察3707相對10月22日低點70.30元與高點75.20元的價格反應，等待法人籌碼。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=70.30與75.20元 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-26-AM-WATCH-5483 | 原文=2026-10-27觀察5483相對10月22日低點185.50元與高點201.00元的價格反應，等待法人籌碼。 | 方向=CONDITIONAL_ONLY | 信心=N/A_NOT_A_PREDICTION | 數字門檻=185.50與201.00元 | 期間=2026-10-27台股日盤或下一實際交易日 | 失效條件=復市改期、正式行情缺漏或當日量價結構改變 | 驗證時間=2026-10-27T23:00:00+08:00
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-10-26-AM
PARENT_REPORT_ID: 2026-10-25-PM
PARENT_SOURCE: predictions/2026-10-25/evening.md
PARENT_STATUS: VALID_ZERO_PREDICTIONS; both required original blocks present, PREDICTION_COUNT=0
PARENT_VERIFICATION: NOT_SCOREABLE; no directional predictions; do not assign hit/miss
LAST_TRADING_SESSION_PARENT: predictions/2026-10-22/evening.md MISSING_FILE; no reconstruction
CURRENT_VERIFICATION: NOT_SCOREABLE; PREDICTION_COUNT=0; eight conditional watch IDs excluded
ROLLING_5D_SCORE: MISSING
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING
TOP3_PRECISION: MISSING
DATA_ERROR_1: reports/2026-10-26/morning.json 404; schema/readiness.sections/input_fingerprints/generated_at unavailable.
DATA_ERROR_2: 2026-10-26 morning and cross-morning directory unavailable; no valid current package.
DATA_ERROR_3: Taiwan closed for holiday, no same-day TW OHLCV, institutions or new TX night session; do not classify as upstream price failure.
DATA_ERROR_4: 2026-10-22 historical report contract DATA_PARTIAL; stock subset PASS for historical session only; generated after its own cutoff.
DATA_ERROR_5: US 2026-10-23 historical regular-session close available, but 2026-10-26 US session has not opened; no invented future close.
DATA_ERROR_6: 2026-10-26 JP/KR morning open unverified from current contract; do not substitute prior close or TOPIX ETF proxy.
DATA_ERROR_7: Without current package, 2026-10-26 08:45 cutoff and current readiness cannot be verified.
NEXT_CHECK: 2026-10-27 Taiwan reopening and 2026-10-26 US formal close, fresh 2026-10-27 report package, actual TX tick.
[/ROLLING_ERROR_LOG]
