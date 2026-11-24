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
        common = set.intersection(*(set(x["scores"]) for x in window)) if window else set()
        metrics[str(n)] = {"n":len(window), "models":{
            k: {"mae":sum(x["scores"][k]["absolute_error"] for x in window)/len(window),
                "bias":sum(x["scores"][k]["signed_error"] for x in window)/len(window),
                "direction_rate":sum(x["scores"][k]["direction_match"] for x in window)/len(window)}
            for k in sorted(common)}}
    return {"rows":rows,"paired_metrics":metrics}

if __name__ == "__main__":
    with open(sys.argv[1],encoding="utf-8") as f:
        print(json.dumps(review(json.load(f)),indent=2))
