# Public market prediction ledger — 2026-11-04 AM
REPORT_ID: 2026-11-04-AM
PARENT_REPORT_ID: 2026-11-03-PM
PARENT_SOURCE: predictions/2026-11-03/evening.md
DATA_PACKAGE_PATH: reports/2026-11-04/morning.json
DATA_PACKAGE_STATUS: MISSING_404_AT_0838_CHECK
DATA_READINESS: DATA_PARTIAL
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 1
PREDICTION_ID: OPEN-20261104-AM
原始字句: 預測2026-11-04臺灣證交所加權指數09:00官方開盤單一中心點位N/A、相對2026-11-03前收43,307.54點的預估漲跌點N/A、預估漲跌幅N/A、合理區間N/A、數值信心N/A。正式晨報JSON於08:38檢查時404；沒有08:20至08:38合格的日韓開盤及匯率觀測，且沒有校準的期現貨基差，不得以夜盤43,779點或美股完成日線直接代替開盤點位。2026-11-03美股完成日線Nasdaq 25,372.01、SOX 10,600.40、TSM ADR 404.80；2026-11-04完成夜盤Shioaji snapshot 43,779，末筆時間04:59:58.571。此為資料不完整的不可計分數值預測，方向不作正式判定。
方向: N/A_INSUFFICIENT_POINT_IN_TIME_INPUTS
信心: N/A
中心點位: N/A
漲跌點數: N/A
漲跌幅: N/A
預測區間: N/A
前收基準: 2026-11-03 TAIEX close 43307.54; secondary provider from previous evening ledger, official direct verification pending
數字門檻: N/A
資料輸入時間: US 2026-11-04T05:00:00+08:00 completed regular session; TX 2026-11-04T04:59:58.571+08:00 completed night; 2026-11-04T08:38:00+08:00 formal report cutoff
主要正負貢獻: US semiconductor recovery relative to prior session potentially positive; TX night price not comparable to spot without calibration; calibrated point contributions and weights N/A
期間: 2026-11-04 09:00 official TWSE TAIEX opening
失效條件: Official opening auction, 08:20-08:38 Asia prices, FX, and policy/news may change direction; do not backfill a numerical forecast
驗證時點: 2026-11-04T09:00:00+08:00; numeric error N/A; 2026-11-04T23:00:00+08:00 ledger audit
分類: UNSCOREABLE_MISSING_QUALIFIED_INPUTS
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-04-AM
PARENT_REPORT_ID: 2026-11-03-PM
PARENT_SOURCE: predictions/2026-11-03/evening.md
PARENT_STATUS: VALID_ORIGINAL_TWO_BLOCKS
PARENT_PENDING_1: 2026-11-03-PM-MKT-01; original 2026-11-04 official TAIEX close <43307.54; confidence 0.51; PENDING
PARENT_PENDING_2: 2026-11-03-PM-2330-01; original 2026-11-04 official 2330 close <2295.00; confidence 0.51; PENDING
TODAY_OPEN_SCORE: N/A_NO_NUMERIC_FORECAST
TODAY_OPEN_MAE: N/A
ROLLING_5D_MAE: STRICT_TWSE_DIRECT_N0_OF5; unverified historic provisional samples excluded
ROLLING_20D_MAE: STRICT_TWSE_DIRECT_N0_OF20
TOP3_PRECISION: MISSING_NO_VERIFIED_ALL_MARKET_RANKING
DATA_ERROR_1: reports/2026-11-04/morning.json missing at cutoff check.
DATA_ERROR_2: 2026-11-03 evening package generated 23:30:28 after 22:58 cutoff; historic six-stock rows usable only as explicitly labeled delayed data.
DATA_ERROR_3: 2026-11-04 nightclose snapshot 06:17:15 contains 2026-11-03 US regular-session daily bars and 2026-11-04 TX 04:59:58.571 snapshot; TX not live at 08:40.
DATA_ERROR_4: TAIFEX official daily data embedded in nightclose snapshot is dated 2026-11-02 and must not be called current 2026-11-03 settlement.
DATA_ERROR_5: no qualified 2026-11-04 08:20-08:38 Japan/Korea open or FX inputs; TOPIX ETF proxy prohibited.
DATA_ERROR_6: GitHub workflow schedule delays previously observed; no assumption that collection executed on time.
NEXT_CHECK: 2026-11-04 23:00 official close verification and formal package timing audit; do not overwrite any historical predictions.
[/ROLLING_ERROR_LOG]
