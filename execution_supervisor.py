"""Deterministic repair queue gate; no autonomous agent invocation."""
import json
import sys

STAGES = ("OPEN", "PR", "CI", "MERGED", "VERIFIED")
NEXT = ("reproduce_and_patch", "check_exact_head_ci", "review_and_merge", "verify_production", "done")

def supervise(items):
    pending = []
    for item in items:
        stage = item["stage"]
        index = STAGES.index(stage)
        evidence = item.get("evidence", {})
        for required in STAGES[1:index+1]:
            if not evidence.get(required):
                raise ValueError(f"{item['id']}: missing {required} evidence")
        if stage != "VERIFIED":
            pending.append({"id": item["id"], "next": NEXT[index],
                            "priority": item["priority"], "blocked": item.get("blocked")})
    pending.sort(key=lambda x: (x["priority"], x["id"]))
    return {"status": "ACTION_REQUIRED" if any(not x["blocked"] for x in pending)
            else "BLOCKED" if pending else "COMPLETE", "pending": pending,
            "next": next((x for x in pending if not x["blocked"]), None)}

if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        result = supervise(json.load(f))
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["status"] == "ACTION_REQUIRED" else 2 if result["status"] == "BLOCKED" else 0)
