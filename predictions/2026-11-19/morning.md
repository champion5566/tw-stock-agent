# 2026-11-19 morning public original ledger
REPORT_ID: 2026-11-19-AM
OPEN_ID: OPEN-20261119-AM
PARENT_REPORT_ID: 2026-11-18-PM
DATA_BLOB_SHA: e2babe40c7d8bd13e10efe9b250569d715b8d7b0
DATA_GENERATED_AT: 2026-11-19T08:28:15.392791+08:00
DATA_SOURCE_WINDOW: market 08:20:27; cross through 08:28:01 Taipei
CUTOFF: 2026-11-19T08:38:00+08:00
VERIFY_AT: 2026-11-19T09:00:00+08:00 TWSE official TAIEX opening
METHOD: No calibrated, reproducible spot-opening estimator; do not substitute TXFR1 night last trade.
PUBLIC_ONLY: TRUE

[PREDICTION_LEDGER]
OPEN-20261119-AM: CENTER=N/A; DELTA_POINTS=N/A; DELTA_PERCENT=N/A; RANGE=N/A; CONFIDENCE=UNCALIBRATED; PREVIOUS_CLOSE=40194.91 (2026-11-18 TWSE dated index).
ELIGIBILITY: NOT_SCORED; no original numeric forecast. Data publication commit/time not independently verified; formal sample not certified.
TXFR1: 39987, last completed night trade 2026-11-19T04:59:56.284+08:00, not current and not spot forecast.
NEW_FORMAL_PREDICTIONS: NONE. Scenarios are unscored research checks.
[/PREDICTION_LEDGER]

[ROLLING_ERROR_LOG]
ROLLING_5_20: Qualified sample counts NOT_AUDITED; MAE/direction/range N/A.
SCORE_100: N/A; weights 25/25/15/25/10 preserved.
PRIOR_REPORT: 2026-11-18-PM ledger read. Its original opening forecast N/A; actual provider-matched open 40720.09, not official-direct; no scored error.
US_REGULAR_CLOSE: 2026-11-18 versus 2026-11-17: SP500 7323.63 -0.23%; NASDAQ 24429.88 +0.42%; SOX 9652.80 +0.10%; TSM ADR 362.62 +0.81%; NVDA 150.96 -2.89%; AMD 530.14 +5.31%; AVGO 354.05 +3.64%; MU 705.27 -1.00%; VIX 24.56 -3.53%. Yahoo/yfinance completed regular session, not after-hours bars.
ASIA: 08:27 TOPIX -0.38%; Advantest -0.77%; Tokyo Electron +0.68%. Nikkei 08:12 STALE; Korean 08:28 KOSPI, Samsung, SK Hynix reported 0.00%, not evidence of directional move.
TW_2026-11-18: TAIEX close 40194.91 +0.26%; semiconductor +0.64%; TWSE breadth 492/520; TWSE+TPEx institutional net -67715947112 TWD; TWSE margin +105588 native lots.
SIX_CLOSES: 0050=94.10; 006208=212.00; 00631L=26.84; 2330=2175.00; 3707=51.50; 5483=142.00. Exact 2026-11-18 daily_ohlcv.data.close, not broker snapshot.
CREDIT: 00631L margin +48725 native lots; five-session +82772; 0050 margin +19877; 2330 foreign net -15452.905 lots (shares /1000).
QUALITY: report_output_quality.py NOT_EXECUTED; six closes manually compared with JSON and deterministic table.
PUBLICATION: source blob SHA pinned; branch commit publication time NOT_INDEPENDENTLY_VERIFIED. No automatic PASS.
[/ROLLING_ERROR_LOG]

[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"2026-11-19-AM","parent_report_id":"2026-11-18-PM","updated_at_taipei":"2026-11-19T08:38:00+08:00","candidates":[{"idea_id":"AI_SEMI_RELATIVE_WEAKNESS","claim":"Taiwan semiconductor persistent relative weakness","status":"WATCH","evidence":[{"source":"2026-11-18 TWSE sector and 2026-11-18 US regular close; 2026-11-19 08:27 Japan","observed_at":"2026-11-19 08:28 Taipei","detail":"Taiwan semiconductor +0.64% versus TAIEX +0.26%; US SOX +0.10%, NVDA -2.89%; TOPIX -0.38%, Advantest -0.77%, Tokyo Electron +0.68%"}],"change_reason":"Maintain WATCH: Taiwan outperformance opposes persistent weakness; overseas mixed without uniform deterioration or fundamental catalyst","next_check":"2026-11-19 Taiwan semiconductor relative close, breadth and 2330 foreign net","falsifier":"Repeated relative outperformance and broadening breadth would reject persistent weakness"},{"idea_id":"LEVERAGED_ETF_CREDIT_RISK","claim":"Leveraged ETF credit exposure and volatility risk","status":"WATCH","evidence":[{"source":"2026-11-18 FinMind 00631L daily and margin","observed_at":"2026-11-18 close","detail":"00631L close 26.84, margin +48725 native lots and +82772 over five sessions; TWSE margin +105588"}],"change_reason":"Maintain WATCH; credit exposure expanded despite flat leveraged ETF price, not proof of forced liquidation","next_check":"2026-11-19 00631L price and credit, TWSE breadth","falsifier":"Sustained margin contraction with price stabilization"}],"pending_checks":[{"id":"OPEN-CALIBRATION","detail":"No qualified numeric model; 5/20 samples unaudited"},{"id":"PUBLICATION-PIN","detail":"Blob SHA known, exact branch commit and timestamp not independently certified"},{"id":"QUALITY-CHECK","detail":"Script not executed; manually checked six closes"}],"corrections_applied":[{"id":"AM-1105","evidence":"US dated regular-close table used; TX completed-night timestamp distinguished from 08:28 Asian quotes; stale Nikkei isolated while valid Japan equipment observations retained"}]}
[/RESEARCH_STATE]
