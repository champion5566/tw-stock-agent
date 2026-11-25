# OPEN-20261125-AM
[PREDICTION_LEDGER]
Target: TWSE official 2026-11-25 09:00 opening. Run requested 08:40 Taipei; source committed 08:28:24 Taipei. Actual ledger creation time is Git commit timestamp. Source ref d16152e83a643326fcdfaa214b59a5633c56b03d; model blob c33efc90d5b0aff3ad93f221232a09c69e30ca49. Source timing eligible but formal_sample_eligible=false in producer; do not promote without independent verification.
{
  "warnings": [],
  "status": "UNCALIBRATED",
  "previous_session": "2026-11-24",
  "source": "TWSE MI_5MINS_HIST + dated MI_INDEX market totals",
  "previous_close": 40122.35,
  "models": {
    "V0-CARRY": {
      "center": 40122.35,
      "delta": 0,
      "return_pct": 0,
      "formula": "previous_close"
    },
    "V1-TX-ZERO-BASIS": {
      "center": 38482,
      "delta": -1640.3499999999985,
      "return_pct": -4.088369699182626,
      "formula": "night_last_minus_assumed_zero_basis",
      "source": "Shioaji_futures_snapshot",
      "trade_time": "2026-11-25T04:59:57.724000+08:00",
      "limitation": "Unknown futures basis; experimental comparison only."
    },
    "V2-CROSS-BLEND": {
      "center": 38368.09740073792,
      "delta": -1754.2525992620795,
      "return_pct": -4.37225785444293,
      "inputs": {
        "TSM_ADR": -3.960394294488745,
        "SOX": -7.880109547987746,
        "NASDAQ": -1.4779239742967576,
        "TOPIX": -0.23,
        "KOSPI": -4.73,
        "TX": -4.088369699182626
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
      "center": 38806.66055055343,
      "delta": -1315.6894494465623,
      "return_pct": -3.2791933908321975,
      "formula": "0.75 * V2 return",
      "limitation": "Post-replay candidate; prospective evaluation required."
    }
  },
  "interval": null,
  "confidence": null,
  "formal_sample_eligible": false,
  "note": "Experimental models; consumer must verify target trading day, publication cutoff and original ledger timing."
}
Input times: {"market":"2026-11-25T08:21:00.233106+08:00","intraday":null,"cross":"2026-11-25T08:28:00.594567+08:00"}. US regular close 05:00, TX 04:59:57, TOPIX 08:27, KOSPI 08:28. V1 primary experimental baseline. Interval/confidence uncalibrated.
[ROLLING_ERROR_LOG]
Prior original evening ledger unavailable at pinned ref; rolling formal score N/A. Do not reconstruct.
[RESEARCH_STATE]
Initialized from current verified snapshot, not historical reconstruction.
SEMICONDUCTOR-REVERSAL WATCH: SOX -7.88%, MU -11.01%, Japan semiconductor weakness and Korea decline suggest reversal risk; check Taiwan semiconductor relative return versus TAIEX at close; reject if semiconductor outperforms.
BREADTH-FLOW-DIVERGENCE WATCH: prior broad rally despite institutional net selling; check official breadth and institutional totals at close; no causal attribution.
