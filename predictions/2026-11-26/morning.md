# OPEN-20261126-AM
[PREDICTION_LEDGER]
Target: 2026-11-26 09:00 TWSE opening
Source ref 2788a877019fd20f597faac52f08572145906b0c
Parent original: 2788a877019fd20f597faac52f08572145906b0c:predictions/2026-11-25/evening.md
Producer code c980fcd858fc5d9d1bc51cfebdaeb2bfa8454976; model blob c33efc90d5b0aff3ad93f221232a09c69e30ca49
Source commit 2026-11-26 08:28:26 Taipei; actual ledger commit clock authoritative; formal eligibility pending.
Input clocks {"market":"2026-11-26T08:24:37.198277+08:00","intraday":null,"cross":"2026-11-26T08:28:04.687492+08:00"}; TX 04:59:59.870, US regular close 05:00, TOPIX 08:27, KOSPI 08:28.
{
  "warnings": [],
  "status": "UNCALIBRATED",
  "previous_session": "2026-11-25",
  "source": "TWSE MI_5MINS_HIST + dated MI_INDEX market totals",
  "previous_close": 38195.43,
  "models": {
    "V0-CARRY": {
      "center": 38195.43,
      "delta": 0,
      "return_pct": 0,
      "formula": "previous_close"
    },
    "V1-TX-ZERO-BASIS": {
      "center": 38397,
      "delta": 201.5699999999997,
      "return_pct": 0.5277332916529431,
      "formula": "night_last_minus_assumed_zero_basis",
      "source": "Shioaji_futures_snapshot",
      "trade_time": "2026-11-26T04:59:59.870000+08:00",
      "limitation": "Unknown futures basis; experimental comparison only."
    },
    "V2-CROSS-BLEND": {
      "center": 38199.27723877683,
      "delta": 3.847238776826998,
      "return_pct": 0.010072510708279636,
      "inputs": {
        "TSM_ADR": -1.9644947392136736,
        "SOX": -0.6525637737050616,
        "NASDAQ": -0.6224791327410162,
        "TOPIX": 0.85,
        "KOSPI": 2.52,
        "TX": 0.5277332916529431
      },
      "weights": {
        "TSM_ADR": 0.2,
        "SOX": 0.15,
        "NASDAQ": 0.05,
        "TOPIX": 0.05,
        "KOSPI": 0.1,
        "TX": 0.45
      },
      "formula": "weighted_mean_of_available_returns",
      "limitation": "Heuristic weights; overlapping signals; not calibrated."
    },
    "V3-SHRINK-075": {
      "center": 38198.31542908262,
      "delta": 2.8854290826175895,
      "return_pct": 0.007554383031209727,
      "formula": "0.75 * V2 return",
      "limitation": "Post-replay candidate; prospective evaluation required."
    }
  },
  "interval": null,
  "confidence": null,
  "formal_sample_eligible": false,
  "note": "Experimental models; consumer must verify target trading day, publication cutoff and original ledger timing."
}
[ROLLING_ERROR_LOG]
Prior evening: formal n added 0; V1 signed -1501.91 abs 1501.91 direction true; official verification pending; 5/20 inventory unverified. No new ACT.
[RESEARCH_STATE]
{"version":"research-state-v1","report_id":"OPEN-20261126-AM","parent_report_id":"2026-11-25-PM","parent_ref":"2788a877019fd20f597faac52f08572145906b0c:predictions/2026-11-25/evening.md","data_ref":"2788a877019fd20f597faac52f08572145906b0c:reports/2026-11-26/morning.json","candidates":[{"idea_id":"SEMICONDUCTOR-REVERSAL","claim":"Taiwan semiconductor relative weakness","status":"REJECT","evidence":"2026-11-25 semiconductor -4.71% vs TAIEX -4.80%","change_reason":"relative outperformance meets parent falsifier; absolute decline remains","next_check":"2026-11-26 relative returns","falsifier":"renewed relative underperformance"},{"idea_id":"BREADTH-FLOW-DIVERGENCE","claim":"broad rally despite institutional net selling","status":"REJECT","evidence":"2026-11-25 TWSE stock-only 39 up 1033 down; combined institutions -85543641804 TWD","change_reason":"rally no longer present","next_check":"2026-11-26 breadth and institutional totals","falsifier":"broad rally resumes despite net selling"},{"idea_id":"ASIA-TECH-REBOUND","claim":"Asian tech rebound may transmit to Taiwan","status":"WATCH","evidence":"08:27 Advantest +10.30%, Tokyo Electron +6.01%; 08:28 SK Hynix +6.02%, KOSPI +2.52%; US regular SOX -0.65%","next_check":"2026-11-26 close semiconductor relative return and TWSE breadth","falsifier":"semiconductor underperforms TAIEX or TAIEX closes below prior close","change_reason":"new Asian observations"}],"pending_checks":["official opening 2026-11-25","parent publication timestamp","teacher handoff and due ACT inventory"],"corrections_applied":[],"decision":"WAIT; no ACT; observe 2330/0050/00631L after open through close","updated_at_taipei":"2026-11-26 morning run; actual commit clock authoritative"}
