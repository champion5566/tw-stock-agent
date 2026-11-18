# 2026-11-18 morning public original ledger
REPORT_ID: 2026-11-18-AM
PARENT_REPORT_ID: 2026-11-17-PM
DATA_BLOB_SHA: 22b302e2c87609ee6bee1fda91f5c08b991c7f2f
DATA_GENERATED_AT: 2026-11-18T08:28:19.405208+08:00
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN_ID: OPEN-20261118-AM
ORIGINAL: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=40092.11.
METHOD: No calibrated, reproducible cash-open mapping; no futures-last-trade substitution.
INPUT_TIME: 2026-11-18 08:25:13 market; 08:28:00 cross; report generated 08:28:19 Taipei.
DATA_CUTOFF: 2026-11-18T08:38:00+08:00.
TARGET_VALIDATION: 2026-11-18T09:00:00+08:00 TWSE official TAIEX opening.
ELIGIBILITY: NOT_SCORED; no numeric original; publication timing and delivery not independently certified.
NEW_FORMAL_PREDICTIONS: NONE. Research scenarios are unscored conditional checks.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
PARENT: 2026-11-17-PM original morning numeric forecast N/A, actual provider opening 40546.64; not official direct; unscored.
ROLLING_5_20: Qualified n/5 and n/20 NOT_AUDITED; MAE/direction/range N/A.
SCORE_100: N/A; weights 25/25/15/25/10 retained; independent of teacher quality.
TAIEX: 2026-11-17 close 40092.11, -2.31%; TPEX 306.61; TWSE breadth 234 up / 789 down.
SIX_EXACT_SESSION_CLOSES: 0050 94.00; 006208 211.90; 00631L 26.86; 2330 2170.00; 3707 52.00; 5483 144.00. All 2026-11-17 daily_ohlcv.data.close; no broker snapshot.
US_2026-11-17_REGULAR: SP500 7340.53 (-1.03%); NASDAQ 24328.38 (-0.74%); SOX 9642.88 (+0.34%); TSM ADR 359.69 (-3.68%); NVDA 155.46 (-0.44%); AVGO 341.60 (+2.46%); MU 712.42 (-0.92%); VIX 25.46 (+11.13%). Yahoo provider completed daily bars, not exchange-certified.
JP_KR_2026-11-18_0827_0828: TOPIX -0.23%; Advantest +3.08%; Tokyo Electron +1.62%; KOSPI +2.49%; Samsung +3.57%; SK Hynix +5.83%; Nikkei 08:12 STALE only.
TX_COMPLETED_NIGHT: TXFR1 39792 at 2026-11-18 04:59:59.640 Taipei; not 08:40 live or cash-open forecast.
MARGIN: 00631L +31328 provider-native lots; five-session +19396; TWSE -15035; TPEx -32658 separately scoped.
QUALITY: report_output_quality.py NOT_EXECUTED; six close values manually checked against pinned JSON blob; full checker status UNKNOWN.
PUBLICATION: source bundle publication_status=PENDING_PUSH_AND_READBACK at generation; branch file fetched; exact branch commit SHA not independently pinned.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-18-AM","parent_report_id":"2026-11-17-PM","updated_at_taipei":"2026-11-18T08:28:19+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-17 TWSE sector index","observed_at":"2026-11-17 close","detail":"Semiconductor -2.16% versus TAIEX -2.31%; relative +0.15pp"},{"source":"2026-11-17 US completed regular bars and 2026-11-18 Asia 08:27-08:28","observed_at":"2026-11-18 08:28 Taipei","detail":"SOX +0.34%, TSM ADR -3.68%; Japan equipment and Korean memory rise"}],"change_reason":"US sector and TSM diverge, Asia rebounds; cannot conclude persistent Taiwan weakness without today's sector breadth and close","next_check":"2026-11-18 TWSE semiconductor close-to-close return minus TAIEX return and TWSE breadth; 2330 foreign net shares","falsifier":"Repeated semiconductor relative outperformance with broad TWSE participation"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"2026-11-17 FinMind 00631L daily and credit","observed_at":"2026-11-17 close","detail":"00631L -3.90%, margin +31328 native lots, five-day +19396; TWSE overall margin -15035"}],"change_reason":"Individual leveraged ETF margin grows despite declining price; no evidence of forced liquidation","next_check":"2026-11-18 00631L close, financing daily and five-day change, TWSE breadth","falsifier":"00631L price stabilizes with declining margin balance"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"No calibrated original cash-open model; 5/20 qualified sample not audited"},{"id":"NIKKEI-STALE","detail":"08:12 Nikkei stale; retain valid TOPIX and equipment observations"},{"id":"PUBLICATION-PIN","detail":"Need independent branch commit publication and delivery readback; bundle marks pending"}],"corrections_applied":[{"id":"AM-1105-CHANGE","evidence":"US dated prior/current regular closes and returns in bundle and report"},{"id":"AM-1105-TIME","evidence":"TX 04:59 explicitly separated from Asia 08:27-08:28"},{"id":"AM-1105-COVERAGE","evidence":"Stale Nikkei does not suppress valid TOPIX and Japanese semiconductor equities"}]}
[/RESEARCH_STATE]
