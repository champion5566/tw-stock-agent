"""Review immutable forecast records; caller supplies verified actual and timing evidence."""
import json
import sys
from opening_baseline import settle

def review(records):
    rows = []
    seen = set()
    for r in records:
        if not r.get("eligible") or not r.get("original_ref") or not r.get("actual_ref"):
            continue
        day = r["date"]
        if day in seen:
            raise ValueError("duplicate session")
        seen.add(day)
        scores = {k: settle(v["center"], r["actual"], r["previous_close"])
                  for k,v in r["models"].items()}
        rows.append({"date": day, "scores": scores})
    rows.sort(key=lambda x:x["date"])
    metrics = {}
    for n in (5,20):
        window = rows[-n:]
        model_names = sorted({key for row in window for key in row["scores"]})
        baseline = "V0-CARRY" if "V0-CARRY" in model_names else "V0"
        paired = {}
        for key in model_names:
            samples = [row for row in window if key in row["scores"] and baseline in row["scores"]]
            if not samples:
                continue
            n_common = len(samples)
            paired[key] = {
                "n": n_common,
                "dates": [row["date"] for row in samples],
                "mae": sum(row["scores"][key]["absolute_error"] for row in samples) / n_common,
                "bias": sum(row["scores"][key]["signed_error"] for row in samples) / n_common,
                "direction_rate": sum(row["scores"][key]["direction_match"] for row in samples) / n_common,
                "v0_mae_same_dates": sum(row["scores"][baseline]["absolute_error"] for row in samples) / n_common,
            }
        metrics[str(n)] = {"n": len(window), "models": paired}
    return {"rows":rows,"paired_metrics":metrics}

if __name__ == "__main__":
    with open(sys.argv[1],encoding="utf-8") as f:
        print(json.dumps(review(json.load(f)),indent=2))
