# Public market prediction ledger — 2026-10-28 PM
REPORT_ID: 2026-10-28-PM
PARENT_REPORT_ID: 2026-10-28-AM
PARENT_LEDGER_PATH: predictions/2026-10-28/morning.md
PARENT_LEDGER_STATUS: VALID_ORIGINAL_TWO_BLOCKS_TWO_SCOREABLE_PREDICTIONS
REPORT_TARGET_TIME: 2026-10-28T23:00:00+08:00
DATA_CUTOFF: 2026-10-28T22:58:00+08:00
DATA_PACKAGE_PATH: reports/2026-10-28/evening.json
DATA_REPORT_ID: MISSING_AT_23_07_CHECK
DATA_READINESS: DATA_PARTIAL_PACKAGE_MISSING
DATA_PACKAGE_STATUS: NOT_FOUND_AT_REPORT_CHECK
DATA_PACKAGE_GENERATED_AT: MISSING
DATA_INPUT_FINGERPRINTS: MISSING
DATA_SECTIONS: required_stock_data=NOT_EVALUATED_NO_PACKAGE; market_context=NOT_EVALUATED_NO_PACKAGE; us_intraday=UNVERIFIABLE_NO_CURRENT_5M; tx_live=UNVERIFIABLE_NO_PASS_TICK; cutoff=UNVERIFIABLE_NO_PACKAGE
SUPPLEMENTAL_SNAPSHOT: 2026-10-28/evening.json exists, 2415145 bytes, blob af6a5936cebb841b1b824caba7f70e78e45e7130; connector returned no parseable content, so cannot certify full metrics or contract. 2026-10-28/research-evening.json created 2026-10-28T23:05:33+08:00, after cutoff; nine stocks daily/institutional/margin availability reported by downstream research, not contract PASS.
SUPPLEMENTAL_TAIEX: 2026-10-28 09:00 open 46402.79, close 47035.58, high 47060.46, low 46402.79, previous close 46096.23; CNA 09:03/13:49 and Yahoo corroborated; TWSE direct official raw index response unavailable, status PROVISIONAL_SOURCE_VERIFICATION.
SUPPLEMENTAL_2330: 2026-10-28 open 2420, close 2425; Yahoo Taiwan daily market, TWSE direct individual daily table not separately fetched.
SUPPLEMENTAL_5483: 2026-10-28 close 188.50; PChome/HiStock corroborated, TPEx direct original response not fetched.
US_QUOTE_SOURCE: 2026-10-28 US current 5m NOT_VERIFIED; 2026-10-27 regular close context from morning ledger only, not current live.
US_QUOTE_AGE: UNKNOWN_NO_QUALIFIED_5M; do not call real-time.
US_DAILY_SOURCE_DATE: 2026-10-27 historical references from parent morning ledger; FinMind USStockPrice not independently fetched.
TX_NIGHT_STATUS: UNVERIFIABLE_NO_CURRENT_PASS_TICK
TX_NIGHT_TRADE_TIME: MISSING
TX_NIGHT_AGE: UNKNOWN
SPCX_IDENTITY: VERIFIED_AS_SPACE_EXPLORATION_TECHNOLOGIES_CORP_CLASS_A_COMMON_STOCK; SEC 2026 Form 10-Q CIK 0001181412 and issuer 2026-06-15 IPO release identify Nasdaq SPCX.
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
SCOREABLE_PREDICTIONS: 2
FORECAST_CONTEXT: Low-confidence conditional research forecasts for 2026-10-29, made after a strong 2026-10-28 Taiwan rebound; current US 5m and TXFR1 ticks are not verified, so no evidence of an empirical edge. These forecasts are calibration hypotheses, not investment instructions. No personal holdings, costs, share counts, account value or P/L.

PREDICTION_ID: 2026-10-28-PM-MKT-01
原始字句: 預測2026-10-29臺灣證券交易所加權指數正式收盤將不低於2026-10-28正式收盤47,035.58點。
方向: UP_OR_FLAT
信心: 0.51
數字門檻: official 2026-10-29 TAIEX close >=47035.58
期間: 2026-10-29 regular session or next actual Taiwan trading session if closed
失效條件: official close <47035.58 is MISS; missing official close is UNVERIFIABLE; postponed session changes validation date, not baseline
驗證時點: 2026-10-29T23:00:00+08:00 or next actual session 23:00
當時證據: 2026-10-28 TAIEX 47035.58 (+939.35, +2.04%), 724 advancing and 287 declining listed shares per CNA, listed institutional net approximately +298.95 TWD billion? No: +298.95 TWD 100-million units (億元), source ToAlpha; current US 5m and TX night unavailable. This is a low-confidence continuation hypothesis and not a calibrated model.
分類: HYPOTHESIS

PREDICTION_ID: 2026-10-28-PM-5483-01
原始字句: 預測2026-10-29中美晶5483正式收盤將低於2026-10-28收盤188.50元。
方向: DOWN
信心: 0.51
數字門檻: official TPEx 5483 close < TWD 188.50
期間: 2026-10-29 regular session or next actual Taiwan trading session if closed
失效條件: official close >= TWD 188.50 is MISS; missing official close is UNVERIFIABLE
驗證時點: 2026-10-29T23:00:00+08:00 or next actual session 23:00
當時證據: 2026-10-28 5483 close 188.50 (+2.17%) and FinMind-derived same-provider 20d volume ratio 0.240 (research-evening.json), below SMA20 by 7.04%; rebound lacked confirmation from strong relative volume. No same-day complete institutional numbers in verified report contract.
分類: HYPOTHESIS
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-10-28-PM
PARENT_REPORT_ID: 2026-10-28-AM
PARENT_SOURCE: predictions/2026-10-28/morning.md
PARENT_STATUS: VALID_ORIGINAL_TWO_BLOCKS; original PREDICTION_ID OPEN-20261028-AM and 2026-10-28-AM-2330-OPEN-01; both source texts retained in parent; do not rewrite.

OPEN_RECAP_ID: OPEN-20261028-AM
OPEN_RECAP_ORIGINAL_TEXT: 預測2026-10-28臺灣證券交易所加權股價指數09:00正式開盤指數為46,340.00點，較2026-10-27正式收盤46,096.23點上漲+243.77點（+0.529%）；預測區間46,060.00至46,620.00點，信心34%。
OPEN_RECAP_ORIGINAL_FORECAST_POINT: 46340.00
OPEN_RECAP_ORIGINAL_FORECAST_CHANGE: +243.77 points; +0.529%
OPEN_RECAP_ORIGINAL_INTERVAL: [46060.00,46620.00]
OPEN_RECAP_ORIGINAL_CONFIDENCE: 0.34
OPEN_RECAP_ORIGINAL_BASELINE: 46096.23
OPEN_RECAP_ORIGINAL_TIME: REPORT_TARGET_TIME=2026-10-28T08:40:00+08:00; precise actual creation timestamp not independently verified; POINT_IN_TIME_VERIFIED=false
OPEN_RECAP_ACTUAL_OPEN: 46402.79 at 2026-10-28 09:00, CNA 09:03 and Yahoo corroborated; direct TWSE official index table fetch unavailable; PROVISIONAL
OPEN_RECAP_ACTUAL_CHANGE: +306.56 points, +0.6650%
OPEN_RECAP_SIGNED_ERROR_ACTUAL_MINUS_PREDICTED: +62.79 points
OPEN_RECAP_ABSOLUTE_ERROR: 62.79 points
OPEN_RECAP_DIRECTION: PROVISIONAL_HIT (UP)
OPEN_RECAP_INTERVAL: PROVISIONAL_HIT (46402.79 within [46060,46620])
OPEN_RECAP_TODAY_MAE: 62.79 points, provisional n=1/1; formally TWSE-direct-verified n=0/1
OPEN_RECAP_LAST5_MAE: 62.79 points, provisional n=1/5 most recent Taiwan sessions; earlier 2026-10-27 morning had directional only, no original numeric point; 2026-10-26 had no scoreable numeric open; other recent files absent
OPEN_RECAP_LAST20_MAE: 62.79 points, provisional n=1/20; no synthetic history
OPEN_RECAP_DIRECTION_RATE: provisional today 1/1, last5 2/2 available original directional forecasts (10/27 and 10/28), last20 2/2 available; 10/27 provisional too
OPEN_RECAP_INTERVAL_COVERAGE: provisional today 1/1, last5 1/1 available, last20 1/1 available; denominators for full windows 1/5 and 1/20
OPEN_RECAP_ORIGINAL_2330_TEXT: 預測2026-10-28台積電2330正式開盤價高於2026-10-27正式收盤價2,400元。
OPEN_RECAP_2330_OPEN: 2420; change +20 (+0.8333%) versus 2400; PROVISIONAL_HIT, official TWSE direct not fetched
OPEN_RECAP_ATTRIBUTION_PREKNOWN: 2026-10-27 US Nasdaq +1.18%, SOX +3.6%, TSM ADR +2.95% were available at forecast time; forecast underpredicted positive spillover by 62.79 points. Current TX basis and 08:20 JP/KR prices missing, cannot assign quantitative error contributions. FX and surprise-news timestamp attribution unverified.
OPEN_RECAP_ATTRIBUTION_POSTFORECAST: 2026-10-28 daytime continuation to close 47035.58 and intraday SK chip earnings response occurred after the 08:40 forecast, cannot be used as ex-ante inputs or fitted explanations.
OPEN_RECAP_NEXT_TEST_RULE: preserve all original forecast fields and source quote timestamps; after >=10 qualified original numeric opening forecasts, test interval half-width=max(150,1.28*rolling MAE) against fixed baseline; only adjust cross-market weights after >=20 out-of-sample observations and >=5% MAE improvement; no tuning from one error.

PRIOR_PM_PREDICTION_1: 2026-10-27-PM-MKT-01; original 2026-10-28 TAIEX official close <46096.23; actual 47035.58; MISS (CNA/Yahoo corroborated; direct TWSE index table pending)
PRIOR_PM_PREDICTION_2: 2026-10-27-PM-5483-01; original 2026-10-28 5483 close <=184.50; actual 188.50; PROVISIONAL_MISS pending direct TPEx official table
PRIOR_PM_WEIGHTED_SCORE: NOT_SCOREABLE_FULL_100; only two prior original forecasts, missing original Top3 and risk categories
CURRENT_VERIFICATION: PENDING 2026-10-29 official closes
ROLLING_5D_SCORE: MISSING
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING
TOP3_PRECISION: MISSING

DATA_ERROR_1: reports/2026-10-28/evening.json NOT_FOUND at 23:07, no formal schema/readiness/sections/input_fingerprints/cutoff to validate.
DATA_ERROR_2: 2026-10-28/evening.json was committed after initial check, 2415145 bytes, but fetch_file returned empty content for oversized file; cannot validate individual fields from that connector result. Do not call file corrupt.
DATA_ERROR_3: 2026-10-28/research-evening.json generated 23:05:33 after 22:58 cutoff; 9/9 historical daily, institutions, margin marked available, but this is not the formal report contract.
DATA_ERROR_4: 2026-10-28/cross-evening.json NOT_FOUND at 23:07; no qualified US current 5m or TXFR1 PASS tick <=10m; US intraday and TX live UNVERIFIABLE.
DATA_ERROR_5: TWSE official index raw 2026-10-28 09:00 table blocked by web access; CNA 09:03 and Yahoo corroborate open 46402.79, provisional rather than direct-official VERIFIED.
DATA_ERROR_6: current-day six-stock full institutional per-stock net, 5d institutional cumulative, credit details, 5d volume ratios not read from validated small report; do not fill with 2026-10-27 data or mix volume definitions.
DATA_ERROR_7: historic 5/20 numeric opening forecasts absent; no retroactive synthesis, no calibration from one point.
DATA_ERROR_8: US daily historical FinMind USStockPrice not independently fetched, 2026-10-27 regular-close context only; US intraday portfolio P/L and concentration NOT_CALCULATED.
NEXT_CHECK: 2026-10-29 08:40 morning read this unchanged original evening ledger; 2026-10-29 23:00 validate two original PM predictions and fresh numeric morning opening forecast; repair upstream 22:58 small report generation without modifying historical ledgers.
[/ROLLING_ERROR_LOG]
