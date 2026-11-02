# Public market prediction ledger — 2026-11-02 PM
REPORT_ID: 2026-11-02-PM
PARENT_REPORT_ID: 2026-11-02-AM
PARENT_LEDGER_PATH: predictions/2026-11-02/morning.md
PARENT_LEDGER_STATUS: VALID_ORIGINAL_TWO_BLOCKS
REPORT_TARGET_TIME: 2026-11-02T23:00:00+08:00
DATA_CUTOFF: 2026-11-02T22:58:00+08:00
DATA_PACKAGE_PATH: reports/2026-11-02/evening.json
DATA_PACKAGE_STATUS: MISSING_404_CHECKED_AFTER_23_09
DATA_REPORT_ID: MISSING
DATA_READINESS: NOT_EVALUATED_FORMAL_PACKAGE_MISSING
DATA_SECTIONS: required_stock_data=NOT_EVALUATED_FORMAL_PACKAGE_MISSING; market_context=NOT_EVALUATED_FORMAL_PACKAGE_MISSING; us_intraday=NOT_EVALUATED_NO_QUALIFIED_5M_AT_23_00; tx_live=NOT_EVALUATED_NO_SHIOAJI_TICK_WITHIN_10_MIN; cutoff=FAILED_NO_FORMAL_PACKAGE_BY_22_58
DATA_PACKAGE_GENERATED_AT: MISSING
DATA_SNAPSHOT_STATUS: FORMAL_PACKAGE_MISSING; RAW_SNAPSHOT_PRESENT_2026-11-02/evening.json; RESEARCH_SUPPLEMENT_CREATED_AFTER_CUTOFF
SUPPLEMENTAL_RESEARCH_PATH: 2026-11-02/research-evening.json
SUPPLEMENTAL_RESEARCH_CREATED_AT: 2026-11-02T23:06:07.724776+08:00
SUPPLEMENTAL_RESEARCH_STATUS: research-v1, 9/9 same-date daily/institutional/margin coverage flags, not report-contract-v1 acceptance, not complete per-stock metrics
SUPPLEMENTAL_TAIEX_OPEN: 45034.53 at 2026-11-02 09:00, -177.30 points (-0.392154%) vs 2026-10-30 close 45211.83; source CNA 2026-11-02 09:06, https://www.cna.com.tw/news/afe/202611020017.aspx ; direct TWSE raw 09:00 record NOT_FETCHED
SUPPLEMENTAL_TAIEX_CLOSE: 44920.14, -291.69 (-0.645163%), high 45156.17 low 44399.10; source CNA 2026-11-02 13:45 https://www.cna.com.tw/news/afe/202611020116.aspx
SUPPLEMENTAL_BREADTH: 526 up, 456 down, 128 unchanged; declining/advancing=0.86692; CNA same article; direct official raw not fetched
SUPPLEMENTAL_SECTOR: TWSE semiconductor index 1491.61 vs prior 1510.66, return -1.261%, TAIEX -0.645%, relative -0.616 percentage points; source breadthdaily 2026-11-02 https://breadthdaily.com/tw/industry/semiconductor/ ; official raw direct NOT_FETCHED
SUPPLEMENTAL_INSTITUTIONAL_TOTALS: foreign -735.20億元, trust +361.17億元, dealer -152.88億元, total -526.91億元; secondary source https://news.cnyes.com/news/id/6643856
SUPPLEMENTAL_SIX_CLOSES: 0050=104.10; 006208=238.65; 00631L=33.83; 2330=2330.00; 3707=64.60; 5483=174.50; same-date research-evening.json and public closing quote corroboration; not 23:00 live
SUPPLEMENTAL_FINMIND_VOLUMES_SHARES: 0050=160932537; 006208=7352659; 00631L=205495353; 2330=41165068; 3707=3929544; 5483=5930322; research-evening.json; divide by 1000 for lots; DO NOT blend with Yahoo volumes
SUPPLEMENTAL_FINMIND_VOLUME_RATIO_20D: 0050=1.270; 006208=1.891; 00631L=0.988; 2330=1.433; 3707=0.242; 5483=0.327; same FinMind denominator; 5D ratio MISSING
SUPPLEMENTAL_DATA_SOURCE_CONFLICT: FinMind stock volumes differ from Yahoo/TPEx stock-volume quote conventions; preserve each source separately, never mix volume-ratio denominators
US_QUOTE_SOURCE: 2026-11-02 22:46 economic news early-session approximate index moves, NOT timestamped five-minute market quote; latest 5m unavailable
US_QUOTE_AGE: UNVERIFIABLE_NO_QUALIFIED_5M_AT_TARGET_OR_COMPLETION
TX_NIGHT_STATUS: UNVERIFIABLE_NO_SHIOAJI_TICK_WITHIN_10_MIN
TX_TRADE_TIME: MISSING_VALID_CURRENT_TICK
TX_AGE: UNVERIFIABLE
DELIVERY_ACK: UNKNOWN
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
FORECAST_TARGET: 2026-11-03 TWSE regular session, if open; no numeric forecast for 2026-11-02 09:00 retrospectively

PREDICTION_ID: 2026-11-02-PM-MKT-01
原始字句: 預測2026-11-03臺灣證券交易所加權股價指數正常交易日官方收盤點位高於2026-11-02正式收盤44,920.14點。
方向: UP
信心: 0.53
數字門檻: 2026-11-03 official TAIEX regular-session close > 44920.14
期間: 2026-11-03 regular TWSE session or next actual trading session if closed
失效條件: official close <=44920.14 is MISS; no verified official close is UNVERIFIABLE
驗證時點: 2026-11-03T23:00:00+08:00
當時證據: 2026-11-02 TAIEX opened 45034.53, intraday low 44399.10, recovered to 44920.14; 526 advancing vs 456 declining stocks; 2026-11-02 22:46 published early US rebound news. Counterevidence: foreign net sell 735.20億元, TWSE semiconductor index -1.26% vs TAIEX -0.65%, US 5m and TX current tick unverified. Evidence is from secondary public reports and 23:06 research supplement, not accepted formal package.
分類: LOW_CONFIDENCE_HYPOTHESIS_NOT_BACKTESTED

PREDICTION_ID: 2026-11-02-PM-BREADTH-01
原始字句: 預測2026-11-03臺灣證券交易所上市股票正常交易日收盤上漲家數將大於下跌家數。
方向: POSITIVE_BREADTH
信心: 0.52
數字門檻: official TWSE listed-stock advancing count > declining count, unchanged excluded
期間: 2026-11-03 regular TWSE session or next actual trading session if closed
失效條件: advancing <= declining is MISS; no verifiable official breadth is UNVERIFIABLE
驗證時點: 2026-11-03T23:00:00+08:00
當時證據: 2026-11-02 526 advancing vs 456 declining despite TAIEX -0.65%; intraday low recovered by 521.04 index points; 22:46 US early rebound report. Counterevidence: foreign cash selling and semiconductor relative weakness may continue. No qualified current US 5m or TX tick; avoid overstating confidence.
分類: LOW_CONFIDENCE_HYPOTHESIS_NOT_BACKTESTED
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-02-PM
PARENT_REPORT_ID: 2026-11-02-AM
PARENT_SOURCE: predictions/2026-11-02/morning.md
PARENT_STATUS: VALID_ORIGINAL_TWO_BLOCKS
OPEN_RECAP_ID: OPEN-20261102-AM
OPEN_RECAP_ORIGINAL_TEXT: 預測2026-11-02臺灣證券交易所加權股價指數09:00官方開盤之單一中心點位N/A；相對2026-10-30官方前收45,211.83點的預估漲跌點N/A、預估漲跌幅N/A、合理預測區間N/A、數值信心N/A。盤前方向性風險偏空，理由為2026-10-30美股費半-7.20%、Nasdaq-2.86%、TSM ADR-5.95%與2026-10-31完成夜盤台指期末筆44,433點；但無合格08:20至08:38日韓觀測與有效校準期現貨基差，且正式2026-11-02晨報資料包截至08:38缺失，故不發布不可驗證的數值預測，不把44,433點當成現貨開盤。
OPEN_RECAP_ORIGINAL_TIME: REPORT_TARGET_TIME=2026-11-02T08:40:00+08:00; DATA_CUTOFF=2026-11-02T08:38:00+08:00; original ledger does not give an independently confirmed actual run timestamp
OPEN_RECAP_ORIGINAL_BASELINE: 2026-10-30 official TAIEX close 45211.83
OPEN_RECAP_FORECAST_POINT: N/A
OPEN_RECAP_FORECAST_CHANGE: N/A
OPEN_RECAP_FORECAST_PERCENT: N/A
OPEN_RECAP_FORECAST_INTERVAL: N/A
OPEN_RECAP_FORECAST_CONFIDENCE: N/A
OPEN_RECAP_ACTUAL_OPEN: 45034.53 (CNA 09:06; direct TWSE raw NOT_FETCHED)
OPEN_RECAP_ACTUAL_CHANGE: -177.30 points, -0.392154%
OPEN_RECAP_SIGNED_ERROR_ACTUAL_MINUS_PREDICTED: N/A_NO_NUMERIC_FORECAST
OPEN_RECAP_ABSOLUTE_ERROR: N/A_NO_NUMERIC_FORECAST
OPEN_RECAP_DIRECTION: UNVERIFIABLE_BACKGROUND_BEARISH_NOT_NUMERIC_FORECAST
OPEN_RECAP_INTERVAL: UNVERIFIABLE_NO_FORECAST_INTERVAL
OPEN_RECAP_TODAY_MAE: N/A_N0
OPEN_RECAP_LAST5_MAE: STRICT_TWSE_DIRECT_N0_OF5; PRIOR_PROVISIONAL_62.79_POINTS_N1_OF5_NOT_REVERIFIED
OPEN_RECAP_LAST20_MAE: STRICT_TWSE_DIRECT_N0_OF20; PRIOR_PROVISIONAL_62.79_POINTS_N1_OF20_NOT_REVERIFIED
OPEN_RECAP_DIRECTION_RATE: STRICT_N0; TODAY_EXCLUDED; prior provisional 2/2 NOT_REVERIFIED
OPEN_RECAP_INTERVAL_COVERAGE: STRICT_N0; TODAY_EXCLUDED; prior provisional 1/1 NOT_REVERIFIED
OPEN_RECAP_ATTRIBUTION_PREKNOWN: 2026-10-30 completed US tech selloff and 2026-10-31 completed TX last observation available but insufficient to calibrate cash open; forecast declined numeric estimate because qualified same-morning Asia and FX missing.
OPEN_RECAP_ATTRIBUTION_POSTFORECAST: 2026-11-02 09:00 cash open 45034.53, subsequent intraday recovery and later US early-session news were not available at 08:38; cannot backfill.
OPEN_RECAP_NEXT_TEST_RULE: Do not change weights after N/A; next numeric open forecast only if contemporaneous 08:20-08:45 Asia, FX, TX same-contract basis and report package qualify. After >=20 qualified ex-ante samples compare holdout MAE and interval coverage before revising weights.

PRIOR_PREDICTION_2026-10-30-PM-MKT-01: HIT_PROVISIONAL_SECONDARY_SOURCE; original <45211.83; observed TAIEX 44920.14; confidence 0.52; original evidence Friday cash crash, weak breadth, contemporaneous tech selloff; actual -291.69 (-0.645%); official raw direct not fetched; recovered from 44399.10 low, so magnitude not implied.
PRIOR_PREDICTION_2026-10-30-PM-5483-01: MISS_PROVISIONAL_SECONDARY_SOURCE; original <174.00; observed 174.50; confidence 0.51; original evidence prior TPEx close 174 and low 170.50, OTC weakness; actual +0.50 (+0.287%); intraday low 163.50 then rebound; official TPEx raw direct not fetched.
PRIOR_PREDICTION_2026-10-31-PM-2330-01: HIT_PROVISIONAL_SECONDARY_SOURCE; original <2370.00; observed 2330.00; confidence 0.56; original evidence US SOX -7.20%, TSM ADR -5.95%; actual -40 (-1.688%); original weekend reversal risk did not overturn close; official TWSE raw direct not fetched.
PRIOR_PREDICTION_2026-10-31-PM-00631L-01: HIT_PROVISIONAL_SECONDARY_SOURCE; original <34.16; observed 33.83; confidence 0.54; original evidence US Nasdaq -2.86%, SOX -7.20%; actual -0.33 (-0.966%); intraday rebound capped losses; official TWSE raw direct not fetched.
PRIOR_PREDICTION_2026-11-01-PM-BREADTH-01: MISS_PROVISIONAL_SECONDARY_SOURCE; original declining/advancing >=2.00; observed 456/526=0.86692; confidence 0.55; original evidence Friday 941 down/92 up, SOX -7.20%; actual broad rebound despite index falling; official TWSE raw direct not fetched.
PRIOR_PREDICTION_2026-11-01-PM-SECTOR-01: HIT_PROVISIONAL_SECONDARY_SOURCE; original semiconductor index return minus TAIEX return <0.00pp; observed -1.261%-(-0.645%)=-0.616pp; confidence 0.54; original evidence Friday SOX -7.20% and TSM ADR -5.95%; actual semiconductor lag; official sector raw direct not fetched.
PRIOR_SIX_PREDICTIONS_PROVISIONAL: HIT=4; MISS=2; DIRECT_OFFICIAL_VERIFIED=0; do not treat as formally weighted score.
WEIGHTED_100_SCORE: NOT_SCOREABLE; no verified original full-market Top3 prediction/actual all-market rankings; preserve direction/style25, inflowTop3 25, outflowTop3 15, holdings25, risk10.
TOP3_PRECISION: MISSING_NO_QUALIFIED_ALL_MARKET_RANKING
DATA_ERROR_1: reports/2026-11-02/evening.json missing 404 at 23:09+, despite 2026-11-02/evening.json raw 2.4MB snapshot existing; formal report contract not accepted.
DATA_ERROR_2: 2026-11-02/research-evening.json generated 23:06:07 after 22:58 cutoff; not formal six-stock report, and cannot be promoted to timely DATA_READY.
DATA_ERROR_3: 2026-11-02 morning original ledger cutoff 08:38 target 08:40, no numeric opening prediction, so official opening movement does not create a valid MAE or hit.
DATA_ERROR_4: current 23:00 US five-minute quotes missing qualified timestamps, 22:46 news is not a live 5m quote; TX Shioaji true tick <=10min missing.
DATA_ERROR_5: FinMind versus Yahoo/TPEx volume discrepancies persist; same-source 20d volume ratios only; per-stock 5d ratios and numerical institutional/credit details not in compact research file.
DATA_ERROR_6: direct TWSE/TPEx raw official 2026-11-02 open, close, breadth, sector, stock close not fetched; secondary sources independently corroborate prices, keep provisional classification.
DATA_ERROR_7: prior original morning target 08:40 cutoff 08:38 differs from current contract 08:50 cutoff 08:45; preserve original, no backfill.
NEXT_CHECK: 2026-11-03 morning verify qualified 08:20-08:45 inputs and report availability; evening verify today's two new predictions; reconcile official TWSE/TPEx raw, stock source volume conflicts, current Shioaji Tick and timestamped US 5m. No overwrite.
[/ROLLING_ERROR_LOG]
