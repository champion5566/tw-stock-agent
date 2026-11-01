# Public market prediction ledger — 2026-11-01 PM
REPORT_ID: 2026-11-01-PM
PARENT_REPORT_ID: 2026-11-01-AM
PARENT_LEDGER_PATH: predictions/2026-11-01/morning.md
PARENT_LEDGER_STATUS: VALID_ORIGINAL_TWO_BLOCKS
REPORT_TARGET_TIME: 2026-11-01T23:00:00+08:00
DATA_CUTOFF: 2026-11-01T22:58:00+08:00
MARKET_CALENDAR: 2026-11-01 SUNDAY; TWSE/TPEx/US cash markets closed; next expected Taiwan regular session 2026-11-02
DATA_PACKAGE_PATH: reports/2026-11-01/evening.json
DATA_PACKAGE_STATUS: MISSING_404
DATA_REPORT_ID: MISSING
DATA_READINESS: DATA_PARTIAL_PACKAGE_MISSING_MARKET_CLOSED
DATA_SECTIONS: required_stock_data=NOT_APPLICABLE_NO_SUNDAY_TWSE_SESSION; market_context=NOT_APPLICABLE_NO_SUNDAY_TWSE_SESSION; us_intraday=NOT_APPLICABLE_US_WEEKEND_NO_5M; tx_live=NOT_APPLICABLE_SESSION_CLOSED_NO_CURRENT_TICK; cutoff=FAILED_NO_FORMAL_PACKAGE_BY_22_58
DATA_PACKAGE_GENERATED_AT: MISSING
HISTORICAL_STOCK_PACKAGE_PATH: reports/2026-10-30/evening.json
HISTORICAL_STOCK_PACKAGE_SCHEMA: scenario-report-v2; readiness.version=report-contract-v1
HISTORICAL_STOCK_PACKAGE_GENERATED_AT: 2026-10-30T23:36:30.915213+08:00; AFTER 2026-10-30T22:58:00+08:00 cutoff
HISTORICAL_STOCK_PACKAGE_STATUS: DATA_PARTIAL; required_stock_data=PASS 6/6 for 2026-10-30 ONLY; market_context=PARTIAL; us_intraday=PARTIAL_FUTURE_TIMESTAMP; tx_live=PARTIAL_FUTURE_TIMESTAMP; cutoff=PARTIAL
HISTORICAL_STOCK_PACKAGE_INPUT_FINGERPRINTS: market/evening sha256=3d716a6423ee4bc0b8336eabe6dc77712f651e6398ce676aa38330178aba5d4d; current/cross-evening sha256=d72db7138a07496130f28af685fda165fe1db4267e5289ed07984c5786c5d12d
HISTORICAL_TAIEX_CLOSE: 2026-10-30 45211.83 (-1156.50, -2.49%); NOT 2026-11-01 quote
HISTORICAL_TAIEX_BREADTH: 2026-10-30 TWSE listed stocks 92 up / 941 down / 45 unchanged; NOT SUNDAY
HISTORICAL_US_SOURCE: 2026-10-31/cross-nightclose.json; Yahoo/yfinance 2026-10-30 completed regular-session daily bars; NOT exchange-certified settlement or Sunday live
HISTORICAL_US_CLOSE: SP500=7580.07(-1.82%); NASDAQ=25437.00(-2.86%); SOX=10688.80(-7.20%); VIX=19.42(+12.91%); TSM_ADR=406.13(-5.95%); NVDA=204.64(-4.22%); AMD=504.80(-10.88%); AVGO=326.08(-5.48%); MU=884.74(-5.30%)
HISTORICAL_TX_COMPLETED_NIGHT_OBSERVATION: Shioaji TXFR1 44433 at 2026-10-31T04:59:59.598+08:00; NOT LIVE 2026-11-01 23:00; NOT EXCHANGE-CERTIFIED SETTLEMENT; NO CALIBRATED SAME-MATURITY BASIS
HISTORICAL_STOCK_VOLUME_CONFLICT: 2026-10-30 FinMind 3707 volume 4300220 shares, 5483 volume 7194140 shares versus prior TPEx supplemental 4227000 and 6937000 shares; preserve source-specific data, do not mix volume-ratio denominators
US_QUOTE_SOURCE: Yahoo/yfinance Friday 2026-10-30 completed daily bars only; no Sunday 23:00 live 5m
US_QUOTE_AGE: SESSION_CLOSED; Friday US regular close 2026-10-31T04:00:00+08:00, ~43 hours old at Sunday 23:00
TX_NIGHT_STATUS: STALE_COMPLETED_SESSION_NOT_LIVE
TX_TRADE_TIME: 2026-10-31T04:59:59.598+08:00
TX_AGE: ~42 HOURS AT 2026-11-01 23:00
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
SCOREABLE_PREDICTIONS_TODAY: 0
FORECAST_TARGET: 2026-11-02 regular Taiwan trading session, or next actual trading session if market closed
FORECAST_CONTEXT: Sunday low-confidence, weekend-gap-exposed hypotheses. Friday US and TX completed sessions are historical; Monday Japan/Korea opens, FX, valid Shioaji TX tick, weekend catalysts and Monday cash order flow unknown. These do not substitute for the separately required Monday 08:50 official opening forecast.

PREDICTION_ID: 2026-11-01-PM-BREADTH-01
原始字句: 預測2026-11-02臺灣證券交易所上市股票下跌家數至少為上漲家數的2倍（下跌家數／上漲家數≥2.00）。
方向: BEARISH_BREADTH
信心: 0.55
數字門檻: official TWSE 2026-11-02 regular-session listed-stock declining count / advancing count >= 2.00; unchanged stocks excluded from ratio
期間: 2026-11-02 regular TWSE session, or next actual trading session if closed
失效條件: verified official declining/advancing ratio < 2.00 is MISS; zero advances or missing/unreliable official breadth is UNVERIFIABLE unless the exchange provides a defined valid ratio
驗證時點: 2026-11-02T23:00:00+08:00 or next actual session 23:00
當時證據: Friday 2026-10-30 TWSE listed-stock breadth 941 declining vs 92 advancing; Friday completed US Nasdaq -2.86%, SOX -7.20%; Monday Asian session and currency unknown. Counterevidence: Friday Taiwan stocks already sold off sharply, short-covering and oversold rebound may reverse breadth.
分類: LOW_CONFIDENCE_HYPOTHESIS

PREDICTION_ID: 2026-11-01-PM-SECTOR-01
原始字句: 預測2026-11-02臺灣證券交易所半導體類指數單日漲跌幅低於同日加權股價指數單日漲跌幅。
方向: SEMICONDUCTOR_UNDERPERFORM
信心: 0.54
數字門檻: official TWSE 2026-11-02 semiconductor sector index regular-session percent change minus official TAIEX regular-session percent change < 0.00 percentage points
期間: 2026-11-02 regular TWSE session, or next actual trading session if closed
失效條件: official sector return minus TAIEX return >=0.00 percentage points is MISS; missing either official index return is UNVERIFIABLE
驗證時點: 2026-11-02T23:00:00+08:00 or next actual session 23:00
當時證據: Friday completed US SOX -7.20%, TSM ADR -5.95%, AMD -10.88%; Taiwan semiconductor shares may reprice Monday. Counterevidence: Taiwan already fell Friday, index heavyweight TSM may outperform smaller technology stocks in a relief rebound; no Monday FX/Asia live confirmation.
分類: LOW_CONFIDENCE_HYPOTHESIS
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-01-PM
PARENT_REPORT_ID: 2026-11-01-AM
PARENT_SOURCE: predictions/2026-11-01/morning.md
PARENT_STATUS: VALID_ORIGINAL_TWO_BLOCKS
OPEN_RECAP_ID: OPEN-20261101-AM
OPEN_RECAP_ORIGINAL_TEXT: 2026-11-01星期日臺灣證券交易所休市，不存在當日09:00官方加權股價指數開盤。單一中心點位N/A、相對最近正式前收45,211.83點的預估漲跌點N/A、預估漲跌幅N/A、合理預測區間N/A、信心N/A。10月31日04:59:59台指期夜盤末筆44,433點不是11月1日現貨開盤，也不是11月2日現貨開盤預測；週一2026-11-02的正式預測須於當日08:38前依當時有效市場資料獨立產生，不得事後回填。週五費半-7.20%及台指夜盤走弱屬週一風險背景，不是可計分開盤預測。
OPEN_RECAP_ORIGINAL_TIME: REPORT_TARGET_TIME=2026-11-01T08:40:00+08:00; ACTUAL_RUN_START=2026-11-01T08:43:47+08:00; DATA_CUTOFF=2026-11-01T08:38:00+08:00
OPEN_RECAP_ORIGINAL_BASELINE: 2026-10-30 official TAIEX close 45211.83
OPEN_RECAP_FORECAST_POINT: N/A
OPEN_RECAP_FORECAST_CHANGE: N/A
OPEN_RECAP_FORECAST_PERCENT: N/A
OPEN_RECAP_FORECAST_INTERVAL: N/A
OPEN_RECAP_FORECAST_CONFIDENCE: N/A
OPEN_RECAP_ACTUAL_OPEN: N/A_MARKET_CLOSED
OPEN_RECAP_ACTUAL_CHANGE: N/A_MARKET_CLOSED
OPEN_RECAP_SIGNED_ERROR_ACTUAL_MINUS_PREDICTED: N/A
OPEN_RECAP_ABSOLUTE_ERROR: N/A
OPEN_RECAP_DIRECTION: UNVERIFIABLE_MARKET_CLOSED
OPEN_RECAP_INTERVAL: UNVERIFIABLE_MARKET_CLOSED
OPEN_RECAP_TODAY_MAE: N/A_N0_OF1_CALENDAR_DAY
OPEN_RECAP_LAST5_MAE: STRICT_TWSE_DIRECT_N0_OF5; PROVISIONAL_62.79_POINTS_N1_OF5_INHERITED_NOT_REVERIFIED
OPEN_RECAP_LAST20_MAE: STRICT_TWSE_DIRECT_N0_OF20; PROVISIONAL_62.79_POINTS_N1_OF20_INHERITED_NOT_REVERIFIED
OPEN_RECAP_DIRECTION_RATE: TODAY_NA; PRIOR_PROVISIONAL_2_OF2_AMONG_AVAILABLE_DIRECTION_RECORDS; STRICT_TWSE_DIRECT_N0; NO_SUNDAY_SAMPLE
OPEN_RECAP_INTERVAL_COVERAGE: TODAY_NA; PRIOR_PROVISIONAL_1_OF1; STRICT_TWSE_DIRECT_N0; NO_SUNDAY_SAMPLE
OPEN_RECAP_ATTRIBUTION_PREKNOWN: Friday completed US SOX -7.20%, Nasdaq -2.86%, completed Saturday 04:59:59 TX 44433 were available by Sunday morning, but Sunday had no TWSE opening and no numerical forecast error to attribute; the -778.83-point raw TX-versus-cash difference is not calibrated same-maturity basis.
OPEN_RECAP_ATTRIBUTION_POSTFORECAST: Monday 2026-11-02 JP/KR opens, FX, valid Shioaji tick, cash open and any new weekend announcements occur after Sunday morning; must not be backfilled as ex-ante inputs.
OPEN_RECAP_NEXT_TEST_RULE: Exclude Sunday N/A from all hit rates and MAE; Monday formal opening prediction only before Monday cash open using then-available inputs; no weight change until >=20 qualified out-of-sample forecasts and >=5% MAE gain. Preserve original 08:40/08:38 ledger timestamps despite newer 08:50/08:45 instruction.
PENDING_2026_10_30_PM_MKT_01: official 2026-11-02 TAIEX close <45211.83; confidence 0.52; PENDING_NOT_YET_TRADED.
PENDING_2026_10_30_PM_5483_01: official 2026-11-02 5483 close <174.00; confidence 0.51; PENDING_NOT_YET_TRADED.
PENDING_2026_10_31_PM_2330_01: official 2026-11-02 2330 close <2370.00; confidence 0.56; PENDING_NOT_YET_TRADED.
PENDING_2026_10_31_PM_00631L_01: official 2026-11-02 00631L close <34.16; confidence 0.54; PENDING_NOT_YET_TRADED.
PENDING_2026_11_01_PM_BREADTH_01: TWSE declining/advancing ratio >=2.00; confidence 0.55; PENDING_NOT_YET_TRADED.
PENDING_2026_11_01_PM_SECTOR_01: TWSE semiconductor index daily percent change minus TAIEX daily percent change <0.00pp; confidence 0.54; PENDING_NOT_YET_TRADED.
WEIGHTED_100_SCORE: NOT_SCOREABLE_NO_SUNDAY_TAIWAN_SESSION; preserve direction/style25, inflowTop3 25, outflowTop3 15, holdings25, risk10.
ROLLING_5D_SCORE: MISSING_INSUFFICIENT_QUALIFIED_SAMPLES
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING_INSUFFICIENT_QUALIFIED_SAMPLES
TOP3_PRECISION: MISSING_NO_SUNDAY_SESSION
DATA_ERROR_1: reports/2026-11-01/evening.json missing 404 and reports/2026-11-01 directory missing; no report-contract-v1 readiness evaluated for Sunday, no cutoff PASS.
DATA_ERROR_2: 2026-11-01 Sunday TWSE/TPEx/US cash closed; no Sunday 09:00 official TAIEX open or Sunday six-stock OHLCV, institutional, breadth or new margin/short data.
DATA_ERROR_3: Friday 2026-10-30 historical package generated 23:36:30 after its 22:58 cutoff; readiness DATA_PARTIAL despite six-stock section PASS; cannot be relabeled as Sunday PASS.
DATA_ERROR_4: Friday US daily bars from 2026-10-31 completed session are ~43h old Sunday 23:00; not current 5m quotes; some 2026-10-30 evening package 23:35 bars were future timestamps relative to Friday 23:00 target.
DATA_ERROR_5: Shioaji TXFR1 2026-10-31T04:59:59.598 is ~42h old Sunday 23:00, no <=10min live tick or calibrated cash-futures basis.
DATA_ERROR_6: FinMind and earlier TPEx supplemental 2026-10-30 volume figures differ for 3707/5483; no source mixing in ratios.
DATA_ERROR_7: Sunday morning original report target 08:40 and cutoff 08:38 differs from current 08:50 and 08:45 instructions; do not rewrite original.
NEXT_CHECK: Monday 2026-11-02 08:20-08:45 contemporaneous JP/KR/FX/TX, then formal opening forecast; Monday 23:00 verify all six pending predictions against TWSE/TPEx official source with original thresholds, and reconcile 3707/5483 source differences.
[/ROLLING_ERROR_LOG]
