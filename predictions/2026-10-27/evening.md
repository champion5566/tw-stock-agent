# Public market prediction ledger — 2026-10-27 PM
REPORT_ID: 2026-10-27-PM
PARENT_REPORT_ID: 2026-10-27-AM
PARENT_LEDGER_PATH: predictions/2026-10-27/morning.md
PARENT_LEDGER_STATUS: VALID_TWO_DIRECTIONAL_OPEN_FORECASTS; ORIGINAL_POINT_OPEN_ID_MISSING
PRIOR_EVENING_LEDGER_PATH: predictions/2026-10-26/evening.md
PRIOR_EVENING_LEDGER_STATUS: VALID_TWO_CLOSE_FORECASTS
REPORT_TARGET_TIME: 2026-10-27T23:00:00+08:00
DATA_CUTOFF: 2026-10-27T22:58:00+08:00
DATA_PACKAGE_PATH: reports/2026-10-27/evening.json
DATA_REPORT_ID: DATA-2026-10-27-evening-40431861239
DATA_SCHEMA_VERSION: scenario-report-v2
DATA_READINESS_VERSION: report-contract-v1
DATA_READINESS: DATA_PARTIAL
DATA_PACKAGE_GENERATED_AT: 2026-10-27T09:20:43.421763+08:00
DATA_PACKAGE_EXECUTION_KIND: CURRENT_TIME_PREVIEW
DATA_POINT_IN_TIME_VERIFIED: false
DATA_PACKAGE_CUTOFF_STATUS: FAILED_NOT_A_2258_EVENING_MEASUREMENT
DATA_PACKAGE_SECTIONS: required_stock_data=PARTIAL_0_OF_6; market_context=PARTIAL; us_intraday=PARTIAL_ALL_STALE_AT_2300; tx_live=PARTIAL_STALE_AT_2300; cutoff=PARTIAL_MARKET_MISSING
DATA_INPUT_FINGERPRINTS: current/cross-evening sha256=941b40b34c68d33cbba1db184a02c801a44f661511f14f4c3c4496711c9d5c61; no verified current market input
SUPPLEMENTAL_MARKET: TAIEX 2026-10-27 open 46211.20 and close 46096.23 (CNA 09:03/13:54, official direct TAIEX index table not independently fetched); TAIEX prior close 46041.43; 2330 TWSE STOCK_DAY 2026-10-27 open 2380 close 2400; 5483 Yahoo 2026-10-27 close 184.50, TPEx official direct pending; other six-stock fields not fully official-verified
US_QUOTE_SOURCE: yfinance/Yahoo 5m historical, not formal closes
US_QUOTE_AGE_AT_2300: index last bar 2026-10-27T04:00+08:00 age 1140m STALE; selected stocks last after-hours bar 2026-10-27T07:55+08:00 age 905m STALE
US_DAILY_SOURCE_DATE: 2026-10-26 selected regular-session references, not 2026-10-27 live
TX_NIGHT_STATUS: STALE_NOT_CURRENT
TX_NIGHT_TRADE_TIME: 2026-10-27T09:20:40.809+08:00
TX_NIGHT_AGE_AT_2300: approximately 819m; cannot call current or compute current basis
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
SCOREABLE_PREDICTIONS: 2
FORECAST_CONTEXT: Low-confidence calibration hypotheses. Taiwan 2026-10-27 official market close is known, but the 22:58 contract was NOT produced; US 2026-10-27 intraday and TX night ticks are stale/unverified. Do not trade solely from these forecasts. No personal position, share count, cost, market value, profit/loss or account data is stored.

PREDICTION_ID: 2026-10-27-PM-MKT-01
原始字句: 2026-10-28台股正常交易日，加權指數正式收盤將低於2026-10-27正式收盤46,096.23點。
方向: DOWN
信心: 0.51
數字門檻: official TAIEX close < 46096.23 points
期間: 2026-10-28 Taiwan regular session, or next actual session if closed
失效條件: official close >= 46096.23 means MISS; absent official close means UNVERIFIABLE; postponed session shifts verification date without changing threshold
驗證時點: 2026-10-28T23:00:00+08:00 or next actual session at 23:00
當時證據: 2026-10-27 TAIEX opened 46211.20, intraday high 46585.45, closed 46096.23 (+54.80 from prior close); closing below open by 114.97 and below high by 489.22; 479 advancing versus 534 declining listed issues; no qualified US/TX live quote at 23:00
分類: HYPOTHESIS

PREDICTION_ID: 2026-10-27-PM-5483-01
原始字句: 2026-10-28中美晶5483正常交易日正式收盤將不高於2026-10-27收盤184.50元。
方向: DOWN_OR_FLAT
信心: 0.52
數字門檻: 5483 official close <= TWD 184.50
期間: 2026-10-28 Taiwan regular session, or next actual session if closed
失效條件: official close > TWD 184.50 means MISS; missing official TPEx close means UNVERIFIABLE
驗證時點: 2026-10-28T23:00:00+08:00 or next actual session at 23:00
當時證據: Yahoo 2026-10-27 14:30 5483 open 190.0, high 193.5, low 183.5, close 184.5 versus 2026-10-22 prior close 186.0; fresh same-day institutional data and 22:58 US/TX contract missing
分類: HYPOTHESIS
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-10-27-PM
PARENT_REPORT_ID: 2026-10-27-AM
PARENT_SOURCE: predictions/2026-10-27/morning.md
PARENT_STATUS: VALID_TWO_DIRECTIONAL_OPEN_FORECASTS; two original scoreable IDs present; OPEN-20261027-AM point-prediction ID NOT_PRESENT; numeric point estimate, signed point change, predicted percent change, predicted interval, and original numeric timestamp NOT_PRESENT
OPEN_RECAP_ORIGINAL_MARKET_ID: 2026-10-27-AM-MKT-OPEN-01
OPEN_RECAP_ORIGINAL_MARKET_TEXT: 2026-10-27台股正式開盤時，加權指數開盤點位將高於上一有效台股交易日2026-10-22的正式收盤46,041.43點。
OPEN_RECAP_ORIGINAL_MARKET_DIRECTION: UP_OPEN
OPEN_RECAP_ORIGINAL_MARKET_CONFIDENCE: 0.55
OPEN_RECAP_ORIGINAL_MARKET_BASELINE: 46041.43
OPEN_RECAP_ORIGINAL_MARKET_TIMESTAMP: REPORT_TARGET_TIME=2026-10-27T08:50:00+08:00; forecast creation timestamp not separately present
OPEN_RECAP_ACTUAL_TAIEX_OPEN: 46211.20 (2026-10-27 09:00; CNA 09:03 and TVBS; TWSE direct index table verification pending)
OPEN_RECAP_ACTUAL_CHANGE: +169.77 points, +0.3687% versus 46041.43
OPEN_RECAP_DIRECTION_RESULT: PROVISIONAL_HIT (UP)
OPEN_RECAP_POINT_FORECAST: MISSING; signed point error=UNVERIFIABLE; absolute error=UNVERIFIABLE; range coverage=UNVERIFIABLE
OPEN_RECAP_TODAY_MAE: N/A n=0/1 eligible numeric opening forecasts
OPEN_RECAP_5_SAMPLE_MAE: N/A n=0/5 retrievable numeric original forecasts
OPEN_RECAP_20_SAMPLE_MAE: N/A n=0/20 retrievable numeric original forecasts; historical missing files are NOT reconstructed
OPEN_RECAP_DIRECTION_HIT_RATE: 1/1 provisional market direction, not numeric point calibration
OPEN_RECAP_INTERVAL_COVERAGE: N/A n=0/1; 5/20 samples not established
OPEN_RECAP_ORIGINAL_2330_ID: 2026-10-27-AM-2330-OPEN-01
OPEN_RECAP_ORIGINAL_2330_TEXT: 2026-10-27台積電2330正式開盤價將高於2026-10-22正式收盤價2,385元。
OPEN_RECAP_ORIGINAL_2330_CONFIDENCE: 0.56
OPEN_RECAP_2330_OFFICIAL_TWSE_OPEN: 2380
OPEN_RECAP_2330_DIRECTION_RESULT: MISS; 2380 <= 2385; opening change -5 TWD (-0.2096%)
OPEN_RECAP_ATTRIBUTION_PREKNOWN: US 2026-10-26 S&P500 +0.70%, Nasdaq +0.82%, SOX +2.82% and TSM ADR +1.40% were available before 08:50; broad index opened up, but the ADR proxy overpredicted 2330 opening direction; JP/KR 08:20 quotes and current TX basis were unverified and cannot be assigned a measured effect
OPEN_RECAP_ATTRIBUTION_POSTFORECAST: TAIEX intraday high 46585.45 and closing fade to 46096.23 occurred AFTER the opening forecast and cannot explain its original error; do not use post-open facts as forecast inputs
OPEN_RECAP_NEXT_TEST_RULE: For next original numeric opening predictions record predicted index points, +/- points and percent, interval, prior-close basis, forecast timestamp, US/TX/JP/KR quote timestamps. Candidate interval half-width=max(150 points,1.28*rolling eligible MAE) only after >=10 valid original numeric samples; change cross-market weights only if out-of-sample 20-session MAE improves >=5%, not from one observation.
PRIOR_EVENING_VERIFICATION_ID_1: 2026-10-26-PM-MKT-01; original threshold TAIEX close < 46041.43; actual 46096.23; MISS
PRIOR_EVENING_VERIFICATION_ID_2: 2026-10-26-PM-5483-01; original threshold 5483 close <=186.00; observed 184.50 Yahoo 14:30; PROVISIONAL_HIT_PENDING_TPEX_DIRECT
PRIOR_EVENING_WEIGHTED_SCORE: NOT_SCOREABLE_FULL_100; only 2 original forecasts and incomplete categories
CURRENT_VERIFICATION: PENDING 2026-10-28 official close
ROLLING_5D_SCORE: MISSING
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING
TOP3_PRECISION: MISSING
DATA_ERROR_1: reports/2026-10-27/evening.json exists but is a 09:20 CURRENT_TIME_PREVIEW, not the 22:58 evening observation; source_fetched_at market=null; point_in_time_verified=false.
DATA_ERROR_2: report contract readiness required_stock_data PARTIAL all six MISSING_OR_INVALID_FIELDS; supplemental web checks cannot rewrite original readiness.
DATA_ERROR_3: market_context PARTIAL: TAIEX/TPEX/breadth/institutional totals/margin totals/futures positioning NOT_COLLECTED_OR_WRONG_SESSION in original package.
DATA_ERROR_4: US intraday section PARTIAL: all nine required symbols STALE at 23:00, historical/after-hours 5m bars are not live.
DATA_ERROR_5: TXFR1 09:20:40 tick is about 13h39m old at 23:00; snapshot PASS at 09:20 cannot be inherited as live.
DATA_ERROR_6: cutoff PARTIAL; market=MISSING_OR_AFTER_CUTOFF; cross/generation PASS only for morning preview, not 22:58.
DATA_ERROR_7: 006208 current official OHLCV and all six same-day institutional/credit metrics not completely verified; no fabricated figures, no source-mixed volume ratios.
DATA_ERROR_8: Historical OPEN-YYYYMMDD-AM numeric forecast and 5/20 original point-prediction sample missing; no retroactive reconstruction or synthetic MAE.
NEXT_CHECK: 2026-10-28 morning issue original numeric OPEN-20261028-AM with timestamp and quote freshness; 2026-10-28 evening validate both original 2026-10-27 PM predictions and numeric opening forecast against official TWSE/TPEx; do not modify existing ledgers.
[/ROLLING_ERROR_LOG]
