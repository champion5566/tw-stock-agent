# Public market prediction ledger — 2026-10-29 PM
REPORT_ID: 2026-10-29-PM
PARENT_REPORT_ID: 2026-10-29-AM
PARENT_LEDGER_PATH: predictions/2026-10-29/morning.md
PARENT_LEDGER_STATUS: VALID_ORIGINAL_TWO_BLOCKS_OPEN_NOT_SCOREABLE
REPORT_TARGET_TIME: 2026-10-29T23:00:00+08:00
DATA_CUTOFF: 2026-10-29T22:58:00+08:00
DATA_PACKAGE_PATH: reports/2026-10-29/evening.json
DATA_PACKAGE_BLOB_SHA: 9942469b3dad48dacc636ca0702f203c114d0d34
DATA_PACKAGE_GENERATED_AT: 2026-10-29T08:48:04.227127+08:00
DATA_PACKAGE_EXECUTION_KIND: CURRENT_TIME_PREVIEW
DATA_READINESS: DATA_PARTIAL
DATA_SNAPSHOT_STATUS: MORNING_PREVIEW_NOT_NIGHT_REPORT
DATA_SECTIONS: required_stock_data=PARTIAL_6_OF_6_MISSING_TARGET_DAILY; market_context=PARTIAL_WRONG_SESSION; us_intraday=PARTIAL_ALL_STALE_AT_23; tx_live=PARTIAL_08_48_TICK_STALE_AT_23; cutoff=PARTIAL_NO_NIGHT_MARKET_INPUT
DATA_REPORT_ID: MISSING_OR_NOT_EXPOSED_IN_PACKAGE
DATA_INPUT_FINGERPRINTS: current/cross-evening snapshot 2026-10-29/cross-evening.json sha256 d94fd42c0dfb7d1370b93ae49a7b4d00cd013b22c0f9e52653c7a679cb4135e1; MORNING PREVIEW ONLY
DATA_SOURCE_FRESHNESS: market=null; intraday=null; cross=2026-10-29T08:47:06.960307+08:00
SUPPLEMENTAL_TAIEX_OFFICIAL_CLOSE: 2026-10-29 46368.33; change -667.25 (-1.42%), TWSE exchangeReport/MI_INDEX official table accessed in report
SUPPLEMENTAL_TAIEX_OPEN: 47014.87; prior close 47035.58; open change -20.71 (-0.0440%); contemporaneous news cross-check, TWSE direct official 09:00 raw index not obtained, PROVISIONAL
SUPPLEMENTAL_TPEX_CLOSE: 387.37 (-7.24, -1.83%); third-party market index sources, not TPEx direct original
SUPPLEMENTAL_MARKET_BREADTH: TWSE official MI_INDEX stocks advance 232, decline 737, unchanged 108; not entire TPEx
SUPPLEMENTAL_INSTITUTIONAL_TOTALS: foreign -688.15 TWD 100-million; trust +86.49; dealers -215.00; total -816.66; ToAlpha 2026-10-29, not contract PASS
SUPPLEMENTAL_REQUIRED_STOCK_OHLCV: TWSE direct 0050 108.65/108.65/106.60/107.25 volume_shares=86630134 turnover_twd=9292291798; 006208 248.45/249.00/244.60/245.75 volume_shares=4751256 turnover_twd=1168554393; 00631L 36.67/36.78/35.57/35.89 volume_shares=174651285 turnover_twd=6284401444; 2330 2420/2425/2390/2415 volume_shares=18403916 turnover_twd=44316626887. TPEx 3707 third-party 71.60/72.50/68.60/68.80, 3482 lots KGI; 5483 third-party 189/189/182/183.50, 2953 lots PChome mobile, desktop conflicting 184.00/4748 lots; 5483 official source and volume UNVERIFIED. All third-party OTC figures PROVISIONAL.
SUPPLEMENTAL_INSTITUTIONAL_PER_STOCK_5D_MARGIN: MISSING_CURRENT_VALIDATED
US_QUOTE_SOURCE: 2026-10-29 08:47 preview cross yfinance/Yahoo 5m HISTORICAL_BARS only
US_QUOTE_AGE: AT_23_APPROX_15_TO_19_HOURS_OR_UNKNOWN_PER_ASSET; STALE, no 2026-10-29 23:00 valid US intraday
TX_NIGHT_STATUS: STALE_08_48_SHIOAJI_TICK_NOT_CURRENT
TX_NIGHT_TRADE_TIME: 2026-10-29T08:48:01.795000+08:00
TX_NIGHT_AGE_AT_23: 14h11m58s
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
SCOREABLE_PREDICTIONS: 2
FORECAST_CONTEXT: Low-confidence hypotheses for next Taiwan trading session 2026-10-30. No current qualified US 5m or TX night tick, no certified individual institutional/credit 5d. These are not proven alpha or personalized trading instructions.
PREDICTION_ID: 2026-10-29-PM-MKT-01
原始字句: 預測2026-10-30臺灣證券交易所加權股價指數正常交易日正式收盤將低於2026-10-29正式收盤46,368.33點。
方向: DOWN
信心: 0.51
數字門檻: official 2026-10-30 TAIEX regular-session close < 46368.33
期間: 2026-10-30 regular Taiwan session, or next actual trading session if closed
失效條件: official close >=46368.33 is MISS; no official close is UNVERIFIABLE
驗證時點: 2026-10-30T23:00:00+08:00 or next actual session 23:00
當時證據: 2026-10-29 official TAIEX close 46368.33 (-667.25), TWSE stock breadth 232 up vs 737 down, institutional total -816.66億元; current US 5m and TXFR1 unverified. A rebound can invalidate this momentum-continuation hypothesis.
分類: HYPOTHESIS

PREDICTION_ID: 2026-10-29-PM-5483-01
原始字句: 預測2026-10-30中美晶5483正常交易日正式收盤將低於2026-10-29暫定收盤183.50元。
方向: DOWN
信心: 0.51
數字門檻: official TPEx 5483 regular-session close < TWD 183.50, conditional on official confirmation of 2026-10-29 183.50 reference
期間: 2026-10-30 regular Taiwan session, or next actual trading session if closed
失效條件: official 2026-10-30 close >=183.50 is MISS; official 2026-10-29 baseline differs from 183.50 => UNVERIFIABLE_BASELINE_CONFLICT, do not rewrite threshold
驗證時點: 2026-10-30T23:00:00+08:00 or next actual session 23:00
當時證據: 2026-10-29 5483 third-party cross-checked close 183.50 (-2.65%), open 189, high 189, low 182; TPEx direct daily official not fetched and PChome desktop has conflicting 184.00 quote. Broader OTC index -1.83%. Unverified source conflict explicitly limits confidence.
分類: HYPOTHESIS
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-10-29-PM
PARENT_REPORT_ID: 2026-10-29-AM
PARENT_SOURCE: predictions/2026-10-29/morning.md
PARENT_STATUS: VALID_ORIGINAL_TWO_BLOCKS; OPEN-20261029-AM numeric forecast N/A, NOT_SCOREABLE, no fabrication.
OPEN_RECAP_ID: OPEN-20261029-AM
OPEN_RECAP_ORIGINAL_TEXT: 2026-10-29臺灣證券交易所加權股價指數09:00正式開盤單一中心點位N/A；相對2026-10-28正式收盤47,035.58點之預估漲跌點數N/A、漲跌幅N/A、區間N/A、信心N/A。方向性背景偏多但不足以形成合格數值預測；不得事後補值。
OPEN_RECAP_FORECAST_POINT: N/A
OPEN_RECAP_FORECAST_CHANGE: N/A
OPEN_RECAP_FORECAST_INTERVAL: N/A
OPEN_RECAP_FORECAST_CONFIDENCE: N/A
OPEN_RECAP_ORIGINAL_BASELINE: 47035.58
OPEN_RECAP_ORIGINAL_TIME: REPORT_TARGET_TIME=2026-10-29T08:40:00+08:00; ACTUAL_EXECUTION_START=2026-10-29T08:44:53+08:00; DATA_CUTOFF=2026-10-29T08:38:00+08:00; POINT_IN_TIME_VERIFIED=false
OPEN_RECAP_ACTUAL_OPEN: 47014.87 at 2026-10-29 09:00, independent news corroboration; TWSE official direct opening raw NOT_VERIFIED
OPEN_RECAP_ACTUAL_CHANGE: -20.71 points, -0.0440% vs 47035.58
OPEN_RECAP_SIGNED_ERROR_ACTUAL_MINUS_PREDICTED: N/A
OPEN_RECAP_ABSOLUTE_ERROR: N/A
OPEN_RECAP_DIRECTION: UNVERIFIABLE_NO_NUMERIC_FORECAST; conditional up bias is NOT scoreable
OPEN_RECAP_INTERVAL: UNVERIFIABLE_NO_INTERVAL
OPEN_RECAP_TODAY_MAE: N/A, n=0/1
OPEN_RECAP_LAST5_MAE: PROVISIONAL_62.79_POINTS_N1_OF5 (2026-10-28 only); strict TWSE-direct n=0/5
OPEN_RECAP_LAST20_MAE: PROVISIONAL_62.79_POINTS_N1_OF20 (2026-10-28 only); strict TWSE-direct n=0/20
OPEN_RECAP_DIRECTION_RATE: today's N/A n=0/1; prior original directional 2026-10-27 and 2026-10-28 provisionally 2/2, historical denominator incomplete; no new hit
OPEN_RECAP_INTERVAL_COVERAGE: today's N/A n=0/1; prior 2026-10-28 provisional 1/1; strict direct verification n=0
OPEN_RECAP_ATTRIBUTION_PREKNOWN: 2026-10-28 US Nasdaq +0.27%, S&P +0.28%, SOX +1.76%, TSM ADR +0.60% in morning ledger; without numeric forecast there is no numeric error to attribute. Morning was missing qualified 08:20-08:38 JP/KR and completed TX night basis; currency and news timestamps unverified. Conditional up bias would have opposed actual opening down but cannot be scored.
OPEN_RECAP_ATTRIBUTION_POSTFORECAST: 2026-10-29 09:00 opening and subsequent intraday slide to 46368.33 happened after the forecast cutoff; cannot be retrofitted into ex-ante features.
OPEN_RECAP_NEXT_TEST_RULE: preserve N/A and report timestamps, no backfill; collect >=10 genuine numeric forecasts for interval calibration, >=20 out-of-sample observations for any weight change, require >=5% out-of-sample MAE improvement; no tuning from unscoreable observation.
PARENT_PM_PREDICTION_1: 2026-10-28-PM-MKT-01 original close >=47035.58; official actual close 46368.33; MISS, error -667.25 points versus threshold.
PARENT_PM_PREDICTION_2: 2026-10-28-PM-5483-01 original close <188.50; provisional 2026-10-29 5483 close 183.50 (also PChome desktop stale quote 184.00, both below threshold); PROVISIONAL_HIT, TPEx direct official still pending.
PARENT_PM_WEIGHTED_SCORE: NOT_SCOREABLE_FULL_100; only original two forecasts, missing Top3 and risk categories.
ROLLING_5D_SCORE: MISSING
ROLLING_20_PREDICTIONS_HIT_RATE: MISSING
TOP3_PRECISION: MISSING
DATA_ERROR_1: reports/2026-10-29/evening.json exists but generated 08:48:04 CURRENT_TIME_PREVIEW, not valid 23:00 night package; 6 required stocks have SESSION_NOT_CLOSED and missing OHLCV/institutions/credit.
DATA_ERROR_2: preview readiness.cutoff.generation=PASS is only generation timestamp <=22:58 and does not prove a night report; report overall cutoff PARTIAL; no night-session run by 23:06.
DATA_ERROR_3: 2026-10-29/cross-evening.json was collected 08:47; US 5m bars stale by 23:00 and TX Shioaji tick 08:48 is >14h old; do not label live.
DATA_ERROR_4: TWSE official direct 10/29 closing/index breadth and 4 listed stock OHLCV were supplemented; OTC 3707/5483 third-party only; TPEx official and full per-stock 5d institutional, financing/margin data unavailable.
DATA_ERROR_5: 5483 third-party desktop/mobile quote conflict 184.00 vs 183.50; historical market snapshot not certified; official TPEx daily required before strict verification.
DATA_ERROR_6: US live quote and TX basis missing; Top3 capital flows and score missing, do not invent.
NEXT_CHECK: 2026-10-30 morning read this unchanged ledger, preserve OPEN N/A; 2026-10-30 23:00 verify the two new original predictions. Repair 22:58 formal evening report scheduling without overwriting prior records.
[/ROLLING_ERROR_LOG]
