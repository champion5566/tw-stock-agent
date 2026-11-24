"""Uncalibrated opening benchmark; no trading or historical ledger writes."""
import json
import math
import sys

def forecast(bundle):
    date = bundle.get("target_session_date")
    row = bundle.get("market_context", {}).get("TAIEX", {})
    close = row.get("close")
    if (not date or row.get("source_date") != date or row.get("status") != "PASS"
            or isinstance(close, bool) or not isinstance(close, (int, float))
            or not math.isfinite(close) or close <= 0):
        return {"status": "MISSING_VERIFIED_PREVIOUS_CLOSE", "models": {}}
    adr = bundle.get("us_regular_close", {}).get("TSM_ADR", {})
    pct = adr.get("change_pct")
    warnings = []
    if isinstance(pct, (int, float)) and not isinstance(pct, bool) and math.isfinite(pct) and abs(pct) >= 10:
        warnings.append("ADR_EXTREME_RETURN_REQUIRES_INDEPENDENT_CHECK")
    return {"warnings": warnings, "status": "UNCALIBRATED", "previous_session": date,
            "source": row.get("source"), "previous_close": close,
            "models": {"V0-CARRY": {"center": close, "delta": 0, "return_pct": 0,
                                     "formula": "previous_close"}},
            "interval": None, "confidence": None,
            "formal_sample_eligible": False,
            "note": "Benchmark only; consumer must verify target trading day, publication cutoff and original ledger timing."}

def settle(center, actual, previous_close):
    for x in (center, actual, previous_close):
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x <= 0:
            raise ValueError("invalid index level")
    sign = lambda x: (x > 0) - (x < 0)
    return {"signed_error": center - actual, "absolute_error": abs(center - actual),
            "direction_match": sign(center - previous_close) == sign(actual - previous_close)}

if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        print(json.dumps(forecast(json.load(f)), ensure_ascii=False, indent=2))
