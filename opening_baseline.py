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
    models = {"V0-CARRY": {"center": close, "delta": 0, "return_pct": 0, "formula": "previous_close"}}
    tx = bundle.get("futures", {}).get("TXFR1", {})
    ready = bundle.get("readiness", {}).get("sections", {}).get("tx_completed_night", {})
    price = tx.get("price")
    if (ready.get("status") == "PASS" and tx.get("status") == "COMPLETED_NIGHT_LAST_OBSERVATION"
            and tx.get("is_live") is False and isinstance(price, (int, float))
            and not isinstance(price, bool) and math.isfinite(price) and price > 0):
        # Explicit zero-basis proxy, not a same-contract return or calibrated cash forecast.
        models["V1-TX-ZERO-BASIS"] = {"center": price, "delta": price-close,
            "return_pct": (price/close-1)*100, "formula": "night_last_minus_assumed_zero_basis",
            "source": tx.get("source"), "trade_time": tx.get("trade_time"),
            "limitation": "Unknown futures basis; experimental comparison only."}
    sections = bundle.get("readiness", {}).get("sections", {})
    us = bundle.get("us_regular_close", {})
    cross = bundle.get("cross_market", {})
    factors = {}
    for key in ("TSM_ADR", "SOX", "NASDAQ"):
        v = us.get(key, {})
        p = v.get("change_pct")
        if (sections.get("us_regular_close", {}).get("items", {}).get(key) == "PASS"
                and v.get("change_status") == "PASS" and isinstance(p, (int, float))
                and not isinstance(p, bool) and math.isfinite(p)):
            factors[key] = p
    for region, key in (("jp", "TOPIX"), ("kr", "KOSPI")):
        p = cross.get(region, {}).get(key, {}).get("change_pct")
        if (sections.get("asia_open", {}).get("items", {}).get(region+"/"+key) == "PASS"
                and isinstance(p, (int, float)) and not isinstance(p, bool) and math.isfinite(p)):
            factors[key] = p
    # Blend overlapping signals rather than adding their full returns.
    weights = {"TSM_ADR": .20, "SOX": .15, "NASDAQ": .05, "TOPIX": .05, "KOSPI": .10}
    if "V1-TX-ZERO-BASIS" in models:
        factors["TX"] = models["V1-TX-ZERO-BASIS"]["return_pct"]
        weights["TX"] = .45
    if factors:
        total = sum(weights[k] for k in factors)
        ret = sum(weights[k]*v for k,v in factors.items())/total
        center = close*(1+ret/100)
        if center > 0:
            models["V2-CROSS-BLEND"] = {"center": center, "delta": center-close,
                "return_pct": ret, "inputs": factors,
                "weights": {k: weights[k]/total for k in factors},
                "formula": "weighted_mean_of_available_returns",
                "limitation": "Heuristic weights; overlapping signals; not calibrated."}
    if "V2-CROSS-BLEND" in models:
        raw = models["V2-CROSS-BLEND"]
        ret = raw["return_pct"] * .75
        models["V3-SHRINK-075"] = {"center": close*(1+ret/100),
            "delta": close*ret/100, "return_pct": ret,
            "formula": "0.75 * V2 return", "limitation": "Post-replay candidate; prospective evaluation required."}
    return {"warnings": warnings, "status": "UNCALIBRATED", "previous_session": date,
            "source": row.get("source"), "previous_close": close,
            "models": models,
            "interval": None, "confidence": None,
            "formal_sample_eligible": False,
            "note": "Experimental models; consumer must verify target trading day, publication cutoff and original ledger timing."}

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
