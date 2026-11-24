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

def stop_gate(items, attempts):
    """Require a current-run attempt for every unresolved item before yielding."""
    result = supervise(items)
    by_id = {a["id"]: a for a in attempts}
    actionable = []
    waiting = []
    for item in result["pending"]:
        a = by_id.get(item["id"], {})
        # A prior queue blocker is not sufficient: recheck it this run.
        if (a.get("outcome") in ("EXTERNAL_BLOCKER", "WAITING_FUTURE_SESSION")
                and a.get("evidence") and a.get("retry_condition")
                and a.get("action") == item["next"]):
            waiting.append(item["id"])
        else:
            actionable.append(item)
    return {"stop_allowed": not actionable,
            "next": actionable[0] if actionable else None,
            "unattempted_or_incomplete": actionable,
            "waiting": waiting,
            "status": "CONTINUE" if actionable else "WAIT" if waiting else "COMPLETE"}

if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        result = supervise(json.load(f))
    if len(sys.argv) > 2:
        with open(sys.argv[2], encoding="utf-8") as f:
            result = stop_gate(json.load(open(sys.argv[1], encoding="utf-8")), json.load(f))
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["stop_allowed"] else 1)
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["status"] == "ACTION_REQUIRED" else 2 if result["status"] == "BLOCKED" else 0)
