# Public market prediction ledger — 2026-10-27 AM
REPORT_ID: 2026-10-27-AM
PARENT_REPORT_ID: 2026-10-26-PM
PARENT_LEDGER_PATH: predictions/2026-10-26/evening.md
PARENT_LEDGER_STATUS: VALID_PENDING_TWO_PREDICTIONS
LAST_COMPLETED_TW_TRADING_SESSION: 2026-10-22
LAST_TRADING_SESSION_EVENING_LEDGER: predictions/2026-10-22/evening.md
LAST_TRADING_SESSION_LEDGER_STATUS: MISSING_FILE
REPORT_TARGET_TIME: 2026-10-27T08:50:00+08:00
DATA_CUTOFF: 2026-10-27T08:45:00+08:00
DATA_REPORT_ID: MISSING
DATA_READINESS: DATA_PARTIAL
DATA_PACKAGE_PATH: reports/2026-10-27/morning.json
DATA_PACKAGE_STATUS: NOT_FOUND_AT_REPORT_CHECK
DATA_GENERATED_AT: MISSING
DATA_INPUT_FINGERPRINTS: MISSING
DATA_SECTIONS: required_stock_data=MISSING_CURRENT_PACKAGE_HISTORICAL_2026-10-22_ONLY; market_context=MISSING_CURRENT_PACKAGE; us_regular_close=MISSING_CURRENT_PACKAGE_SUPPLEMENTAL_WEB_VERIFICATION; asia_open=MISSING_VERIFIED_2026-10-27_0820_QUOTES; tx_completed_night=MISSING_CURRENT_SESSION_AND_SOURCE_CONFLICT; cutoff=UNVERIFIABLE_NO_PACKAGE
HISTORICAL_REFERENCE_PACKAGE: reports/2026-10-22/evening.json
HISTORICAL_REFERENCE_STATUS: DATA_PARTIAL; required_stock_data=PASS for 2026-10-22 only; generated 2026-10-22T23:21:42.759979+08:00 after 22:58 cutoff
LATEST_CROSS_NIGHTCLOSE: 2026-10-27/cross-nightclose.json; fetched_at=2026-10-27T06:05:20.861350+08:00; 5m bars are NOT formal regular-session closes
US_REFERENCE: 2026-10-26 regular-session S&P500 7676.77, Nasdaq 26169.38 independently supported by AP; SOX 11083.5 historical daily close corroborated by Investing; individual close provenance varies; VIX formal close unverified
TX_REFERENCE: 2026-10-22 TAIFEX TX 202611 after-hours Last=47482 versus Shioaji prior-session snapshot price=45654 trade_time=2026-10-23T04:59:59+08:00; inconsistent and NOT current tick; do not treat as certified night settlement
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
SCOREABLE_PREDICTIONS: 2
FORECAST_CONTEXT: Pre-open low-confidence hypotheses based on verified US 2026-10-26 regular-session rebound, Taiwan last completed session 2026-10-22, and missing current 2026-10-27 report contract/Asia 08:20 quotes/current TX tick. These are calibration forecasts, not trading instructions. They do not alter or overwrite parent forecasts.
PREDICTION_ID: 2026-10-27-AM-MKT-OPEN-01
原始字句: 2026-10-27台股正式開盤時，加權指數開盤點位將高於上一有效台股交易日2026-10-22的正式收盤46,041.43點。
方向: UP_OPEN
信心: 0.55
數字門檻: official TAIEX opening index > 46041.43 points
期間: 2026-10-27 regular Taiwan opening auction; if session postponed, next actual session
失效條件: official open <= 46041.43 means forecast MISS; no official opening observation means UNVERIFIABLE; session postponement moves validation date
驗證時點: 2026-10-27T23:00:00+08:00 or 23:00 on next actual session
當時證據: 2026-10-26 S&P500 7676.77 (+0.70%), Nasdaq 26169.38 (+0.82%), SOX about 11083.5 (+2.82%); US rally is a counterweight to 2026-10-22 Taiwan weakness; current Asia/TX quotes unverified
分類: HYPOTHESIS
PREDICTION_ID: 2026-10-27-AM-2330-OPEN-01
原始字句: 2026-10-27台積電2330正式開盤價將高於2026-10-22正式收盤價2,385元。
方向: UP_OPEN
信心: 0.56
數字門檻: 2330 official opening price > TWD 2385
期間: 2026-10-27 regular Taiwan opening auction; if session postponed, next actual session
失效條件: official open <= TWD 2385 means forecast MISS; no official opening price means UNVERIFIABLE; session postponement moves validation date
驗證時點: 2026-10-27T23:00:00+08:00 or 23:00 on next actual session
當時證據: 2026-10-22 2330 official historical close 2385; 2026-10-26 TSM ADR regular-session close 424.37 (+1.40%) independently sourced from Investing, but ADR is not a deterministic Taiwan price conversion; no current TX tick
分類: HYPOTHESIS
NON_SCOREABLE_WATCH_ID: 2026-10-27-AM-WATCH-FLOW | 原文=等待2026-10-27官方外資、投信、自營商買賣超與全市場Top3金額公布後再判斷流向，不使用10月22日舊籌碼冒充當日資金。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 數字門檻=當日外資淨額0億元；正式金額Top3 | 期間=2026-10-27日盤 | 失效條件=正式資料缺漏則UNVERIFIABLE | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-27-AM-WATCH-0050 | 原文=0050觀察2026-10-22低點106.75元及高點109.15元，待10月27日正式量價確認。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 數字門檻=106.75/109.15元 | 期間=2026-10-27日盤 | 失效條件=當日價格結構改變或資料缺漏 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-27-AM-WATCH-006208 | 原文=006208觀察2026-10-22低點244.70元及高點249.90元，待10月27日正式量價確認。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 數字門檻=244.70/249.90元 | 期間=2026-10-27日盤 | 失效條件=當日價格結構改變或資料缺漏 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-27-AM-WATCH-00631L | 原文=00631L觀察2026-10-22低點35.59元及高點37.00元，注意槓桿及隔日跳空風險。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 數字門檻=35.59/37.00元 | 期間=2026-10-27日盤 | 失效條件=當日價格結構改變或資料缺漏 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-27-AM-WATCH-2330 | 原文=2330除獨立開盤預測外，盤中觀察2026-10-22低點2385元及高點2435元與成交量，不將舊區間當成即時訊號。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 數字門檻=2385/2435元 | 期間=2026-10-27日盤 | 失效條件=當日價格結構改變或資料缺漏 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-27-AM-WATCH-3707 | 原文=3707觀察2026-10-22低點70.30元及高點75.20元，待10月27日正式量價與法人籌碼確認。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 數字門檻=70.30/75.20元 | 期間=2026-10-27日盤 | 失效條件=當日價格結構改變或資料缺漏 | 驗證時間=2026-10-27T23:00:00+08:00
NON_SCOREABLE_WATCH_ID: 2026-10-27-AM-WATCH-5483 | 原文=5483觀察2026-10-22低點185.50元及高點201.00元，注意先前放量下跌與法人賣超，等待當日正式量價確認。 | 方向=CONDITIONAL_ONLY | 信心=N/A | 數字門檻=185.50/201.00元 | 期間=2026-10-27日盤 | 失效條件=當日價格結構改變或資料缺漏 | 驗證時間=2026-10-27T23:00:00+08:00
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-10-27-AM
PARENT_REPORT_ID: 2026-10-26-PM
PARENT_SOURCE: predictions/2026-10-26/evening.md
PARENT_STATUS: VALID_PENDING_TWO_PREDICTIONS; both required original blocks present; original REPORT_ID=2026-10-26-PM; original scoreable IDs 2026-10-26-PM-MKT-01 and 2026-10-26-PM-5483-01 preserved without rewriting
PARENT_VERIFICATION: PENDING_OFFICIAL_2026-10-27_CLOSE; cannot score prior evening's close forecasts before Taiwan close
LAST_TRADING_SESSION_PARENT: predictions/2026-10-22/evening.md MISSING_FILE; historical chain not reconstructed
CURRENT_VERIFICATION: PENDING; two current opening forecasts await official opening values and evening scoring
ROLLING_5D_SCORE: MISSING
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING
TOP3_PRECISION: MISSING
DATA_ERROR_1: reports/2026-10-27/morning.json NOT_FOUND; cannot inspect current schema_version, readiness.sections, input_fingerprints, generated_at, or cutoff PASS.
DATA_ERROR_2: 2026-10-27 directory contains cross-nightclose.json and observations only; current morning.json and cross-morning.json NOT_FOUND.
DATA_ERROR_3: historical 2026-10-22 report has complete six stock subset but overall DATA_PARTIAL and was generated after its 22:58 cutoff; do not inherit PASS for 2026-10-27.
DATA_ERROR_4: 2026-10-27 06:05 cross-nightclose US 5m bars are not certified US 2026-10-26 regular close; separately verified selected closes from AP/market history; supplemental verification cannot change missing package.
DATA_ERROR_5: 2026-10-27 JP/KR 08:20+ opening index values were not independently verified; no prior-close or TOPIX ETF substitution.
DATA_ERROR_6: TX 2026-10-22 after-hours official Last 47482 conflicts with prior-session Shioaji snapshot 45654, and neither is current TX tick; no certified current night close.
DATA_ERROR_7: VIX 2026-10-26 formal closing value not confirmed; 5m last bar 18.39, external provisional 18.38, and 18.27 intraday must not be equated.
DATA_ERROR_8: 2026-10-26 MU regular close 903.70 independently reported, while 06:05 2026-10-27 snapshot 909.25 is after-hours; no substitution.
DATA_ERROR_9: 2026-10-27 08:45 data preparation cutoff missed/UNVERIFIABLE because current package missing; no delivery acknowledgment.
NEXT_CHECK: 2026-10-27 23:00 verify both 2026-10-26-PM close forecasts and both 2026-10-27-AM opening forecasts against official TWSE/TPEx values; retain original text and no fabricated rolling scores.
[/ROLLING_ERROR_LOG]
