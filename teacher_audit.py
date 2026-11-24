"""Read-only teacher audit: executable queue and replay settlement."""
import json
import sys
from pathlib import Path
from opening_baseline import settle
from execution_supervisor import stop_gate

def audit(queue, root):
    root = Path(root)
    result = {"gate": stop_gate(queue, []), "replays": [], "errors": []}
    for path in sorted((root / "ledger/replay").glob("*.json")):
        try:
            record = json.loads(path.read_text())
            day = record["date"]
            bundle = root / "reports" / day / "evening.json"
            row = json.loads(bundle.read_text()).get("market_context", {}).get("TAIEX", {}) if bundle.exists() else {}
            entry = {"date": day, "record": str(path.relative_to(root)), "models": record["models"]}
            if row.get("status") == "PASS" and row.get("source_date") == day and row.get("source", "").startswith("TWSE MI_5MINS_HIST"):
                entry["actual"] = row["open"]
                entry["scores"] = {k: settle(v["center"], row["open"], record["previous_close"]) for k,v in record["models"].items()}
                entry["actual_ref"] = str(bundle.relative_to(root))
            else:
                entry["blocker"] = "Missing dated official TWSE opening in published evening bundle"
            result["replays"].append(entry)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            result["errors"].append({"path": str(path), "error": str(exc)})
    return result

if __name__ == "__main__":
    print(json.dumps(audit(json.loads(Path("docs/repair_queue.json").read_text()), sys.argv[1]), indent=2))
