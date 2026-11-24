"""Read-only teacher audit: executable queue and replay settlement."""
import json
import sys
import math
from urllib.request import urlopen, Request
from pathlib import Path
from opening_baseline import settle
from execution_supervisor import stop_gate

OFFICIAL_URL = "https://openapi.twse.com.tw/v1/indicesReport/MI_5MINS_HIST"

def official_open(day, rows):
    year, month, date = day.split("-")
    accepted = {day, day.replace("-", ""), f"{int(year)-1911}/{month}/{date}", f"{int(year)-1911}{month}{date}"}
    for row in rows:
        if str(row.get("Date")) in accepted:
            value = float(str(row["OpeningIndex"]).replace(",", ""))
            if math.isfinite(value) and value > 0:
                return {"status":"PASS", "source_date":day, "source":"TWSE MI_5MINS_HIST direct", "open":value}
    return {}

def fetch_official():
    with urlopen(Request(OFFICIAL_URL, headers={"User-Agent":"tw-stock-agent teacher audit"}), timeout=15) as response:
        return json.load(response)

def audit(queue, root, official_loader=None):
    root = Path(root)
    result = {"gate": stop_gate(queue, []), "replays": [], "errors": []}
    official_rows = None
    for path in sorted((root / "ledger/replay").glob("*.json")):
        try:
            record = json.loads(path.read_text())
            day = record["date"]
            bundle = root / "reports" / day / "evening.json"
            row = json.loads(bundle.read_text()).get("market_context", {}).get("TAIEX", {}) if bundle.exists() else {}
            entry = {"date": day, "record": str(path.relative_to(root)), "models": record["models"]}
            actual_ref = str(bundle.relative_to(root))
            if not (row.get("status") == "PASS" and row.get("source_date") == day and row.get("source", "").startswith("TWSE MI_5MINS_HIST")) and official_loader:
                try:
                    if official_rows is None:
                        official_rows = official_loader()
                    row = official_open(day, official_rows)
                    actual_ref = OFFICIAL_URL + "#date=" + day
                except (ValueError, KeyError, TypeError, OSError) as exc:
                    entry["fallback_error"] = str(exc)
            if row.get("status") == "PASS" and row.get("source_date") == day and row.get("source", "").startswith("TWSE MI_5MINS_HIST"):
                entry["actual"] = row["open"]
                entry["scores"] = {k: settle(v["center"], row["open"], record["previous_close"]) for k,v in record["models"].items()}
                entry["actual_ref"] = actual_ref
                entry["actual_evidence"] = row
            else:
                entry["blocker"] = "Missing dated official TWSE opening in published evening bundle"
            result["replays"].append(entry)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            result["errors"].append({"path": str(path), "error": str(exc)})
    return result

if __name__ == "__main__":
    print(json.dumps(audit(json.loads(Path("docs/repair_queue.json").read_text()), sys.argv[1], fetch_official), indent=2))
