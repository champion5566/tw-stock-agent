# Public market prediction ledger — 2026-11-05 AM
REPORT_ID: 2026-11-05-AM
PARENT_REPORT_ID: 2026-11-04-PM
PARENT_SOURCE: predictions/2026-11-04/evening.md
DATA_REVISION: ada6ff8159dbf15439f5d08d9476900bc7e62dc8
DATA_PACKAGE: reports/2026-11-05/morning.json
DATA_PACKAGE_GENERATED_AT: 2026-11-05T08:28:18+08:00
DATA_PACKAGE_FILE_COMMIT_AT: 2026-11-05T08:28:23+08:00
DATA_CUTOFF: 2026-11-05T08:38:00+08:00
ACTUAL_REPORT_STARTED_AFTER_TARGET: TRUE
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
PREDICTION_COUNT: 1
PREDICTION_ID: OPEN-20261105-AM
原始字句: 2026-11-05 TWSE加權指數09:00官方開盤中心點N/A；相對2026-11-04官方前收42,948.91點之漲跌點N/A、漲跌幅N/A、區間N/A、數值信心N/A。原因：缺少已用原始預測與正式開盤結果校準且可重算的期現貨傳導模型，且本次報告實際開始晚於08:40。不得以TX夜盤末筆43,404點冒充現貨開盤預測。盤前證據顯示美國費半疲弱、韓國半導體大跌而台指夜盤相對前收偏高，方向分化；沒有可交易的經校準開盤點數優勢。
方向: MIXED_UNCALIBRATED
中心點位: N/A
漲跌點數: N/A
漲跌幅: N/A
合理區間: N/A
信心: N/A_UNCALIBRATED
前收: 42948.91 (TWSE 2026-11-04)
數字門檻: N/A
資料來源及時間: TWSE 2026-11-04 close 42948.91; Yahoo 2026-11-04 US regular session SOX 10268.6543 NASDAQ 25736.5137 SP500 7688.6201 TSM 395.75 NVDA 200.13 (completed 2026-11-05 05:00 Taipei); Shioaji TXFR1 completed-night last observation 43404 at 2026-11-05 04:59:53 Taipei; Yahoo Japan TOPIX 3974.08 at 08:27 Taipei; Naver KOSPI 5521.65 (-2.85%) at 08:28, Samsung 208750 (-4.24%) at 08:28, SK Hynix 1296000 (-7.16%) at 08:28; Nikkei 62455.33 at 08:13 (DELAYED; excluded).
計算方法: No calibrated point estimate; no fabricated weights or contributions. TX minus previous cash close = +455.09 arithmetic points only, not adjusted cash-futures basis.
失效條件: Valid ex-ante calibrated point forecast with verified original inputs could supersede this N/A only in a separate future report; no retroactive replacement.
驗證時點: 2026-11-05 09:00 Asia/Taipei official TWSE opening; numeric error N/A and excluded from formal scoring.
分類: UNSCOREABLE_UNCALIBRATED
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
REPORT_ID: 2026-11-05-AM
PARENT_REPORT_ID: 2026-11-04-PM
PARENT_STATUS: VALID_TWO_BLOCKS_NO_RESEARCH_STATE
PARENT_PENDING_1: 2026-11-04-PM-MKT-01; original 2026-11-05 TAIEX close <42948.91; PENDING_TARGET_SESSION
PARENT_PENDING_2: 2026-11-04-PM-2330-01; original 2026-11-05 2330 close <2260.00; PENDING_TARGET_SESSION
OPEN_NUMERIC_SCORE: N/A_N0
FORMAL_OPEN_SAMPLE_ELIGIBLE: FALSE
PREVIOUS_OPEN_ORIGINAL: OPEN-20261104-AM N/A; cannot score
EVALUATION_SOURCE: evaluations/ledger-review-historical-20261105.json
EVALUATION_LIMITATION: PROVIDER_MATCHED is not OFFICIAL_DIRECT; pending target-day outcomes remain pending.
DATA_EXCEPTION_1: asia_open PARTIAL because jp/NIKKEI225 DELAYED (08:13 local Taiwan observation); other seven required regional observations PASS at 08:27-08:28.
DATA_EXCEPTION_2: TPEx four-digit breadth missing due to ChunkedEncodingError; market_context section PASS applies its defined contract scope, not all optional detail.
DATA_EXCEPTION_3: 2026-11-04 evening package generated 23:45:05 after 22:58 cutoff; not a valid timely evening package.
DATA_EXCEPTION_4: Morning bundle point_in_time_verified=false and formal_sample_eligible=false; report file changing commit at 08:28:23 is before cutoff, but model prediction and platform delivery are separate.
NEXT_CHECK: 2026-11-05 09:00 official TWSE opening for factual observation only; 2026-11-05 official close to settle original parent thresholds; next morning check source timeliness and calibration evidence.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-05-AM","parent_report_id":"2026-11-04-PM","updated_at_taipei":"2026-11-05T08:42:18+08:00","state_initialised_now":true,"initialisation_note":"Parent ledger has no RESEARCH_STATE; initialised only from currently verified observations, not historical reconstruction.","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor exposures face near-term risk from US SOX weakness and Korean chip declines, despite completed Taiwan futures night strength.","evidence":[{"source":"reports/2026-11-05/morning.json pinned data revision","observed_at":"2026-11-05T08:28:18+08:00","detail":"SOX completed 10268.65; Samsung -4.24%; SK Hynix -7.16%; TX last 43404 versus prior cash 42948.91"}],"status":"WATCH","change_reason":"New Asia observations conflict with positive Taiwan futures arithmetic spread; cannot infer opening index point move.","next_check":"2026-11-05 09:00 TWSE opening and sector breadth, followed by 13:30 official closes","falsifier":"TSMC and broad semiconductor sector sustain relative strength despite Korea weakness"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leverage and concentrated ETF activity may amplify index volatility; do not treat ETF dealer flows as directional cash flow.","evidence":[{"source":"reports/2026-11-05/morning.json","observed_at":"2026-11-04 completed session","detail":"0050 margin +4532 provider-native lots; 0050 dealer net -225287986 shares includes hedging; 00631L metrics require monitoring"}],"status":"WATCH","change_reason":"New observed credit/ETF activity; causal direction and liquidation risk not proven.","next_check":"2026-11-05 close, credit changes and dealer component classification","falsifier":"Credit exposure contracts while price volatility normalizes"}],"pending_checks":["2026-11-04-PM-MKT-01","2026-11-04-PM-2330-01"],"corrections_applied":[]}
[/RESEARCH_STATE]
