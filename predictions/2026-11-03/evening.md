# Public market prediction ledger — 2026-11-03 PM
REPORT_ID: 2026-11-03-PM
PARENT_REPORT_ID: 2026-11-03-AM
PARENT_SOURCE: predictions/2026-11-03/morning.md
DATA_PACKAGE_PATH: reports/2026-11-03/evening.json
DATA_PACKAGE_STATUS: MISSING_404_AT_REPORT
DATA_READINESS: DATA_PARTIAL
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 2
PREDICTION_ID: 2026-11-03-PM-MKT-01
原始字句: 預測2026-11-04 TWSE加權指數正常交易日官方收盤低於2026-11-03收盤43,307.54點。
方向: DOWN
信心: 0.51
數字門檻: 2026-11-04 official TAIEX regular close <43307.54
期間: 2026-11-04 TWSE regular session
失效條件: official close >=43307.54 is MISS; official close unavailable is UNVERIFIABLE
驗證時點: 2026-11-04T23:00:00+08:00
當時證據: 2026-11-03 secondary-provider TAIEX close 43307.54 (-3.59%), wide intraday decline; 反證: sharp selloff could produce technical rebound; no qualified current US/TX quotes or formal report.
分類: LOW_CONFIDENCE_HYPOTHESIS_NOT_BACKTESTED

PREDICTION_ID: 2026-11-03-PM-2330-01
原始字句: 預測2026-11-04台積電2330正常交易日官方收盤低於2026-11-03收盤2,295元。
方向: DOWN
信心: 0.51
數字門檻: 2026-11-04 official 2330 regular close <2295.00 TWD
期間: 2026-11-04 regular session
失效條件: official close >=2295.00 is MISS; missing official close is UNVERIFIABLE
驗證時點: 2026-11-04T23:00:00+08:00
當時證據: 2026-11-03 secondary-provider 2330 close 2295 versus prior 2330; 反證: 2330 fell less than index and may show relative strength; no current verified US/TX feed.
分類: LOW_CONFIDENCE_HYPOTHESIS_NOT_BACKTESTED
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-03-PM
OPEN-20261103-AM: UNVERIFIABLE_NUMERIC_NA; original center=N/A, delta=N/A, range=N/A, confidence=N/A, prior close=44920.14; secondary opening reference 44481.59 (-438.55, -0.9763%); numeric error=N/A; direction score=N/A.
TODAY_OPEN_MAE: N/A_N0
ROLLING_5D_MAE: STRICT_TWSE_DIRECT_N0_OF5
ROLLING_20D_MAE: STRICT_TWSE_DIRECT_N0_OF20
2026-11-03-AM-MKT-01: PROVISIONAL_HIT_SECONDARY; original close <44920.14, secondary close 43307.54.
2026-11-03-AM-2330-01: PROVISIONAL_HIT_SECONDARY; original close <2330, secondary close 2295.
FORMAL_SCORE: UNVERIFIABLE_NO_DIRECT_TWSE_AND_NO_FULL_MARKET_DATA
ERROR_CAUSE: Missing formal reports/2026-11-03/evening.json and no direct official TWSE raw open/close verification. Missing US live quote, TX current tick, breadth and six-stock contract.
NEXT_CALIBRATION_RULE: Do not fit coefficients from today's N/A prediction. Collect >=20 qualifying timestamped open predictions before evaluating fixed weight changes; compare against no-change baseline.
NEXT_CHECK: Fetch TWSE official opening and closes, all required sections and new formal package before grading; preserve morning original.
[/ROLLING_ERROR_LOG]
