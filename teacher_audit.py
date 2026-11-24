"""Read-only teacher audit: executable queue and replay settlement."""
import json
import sys
import math
from urllib.request import urlopen, Request
from pathlib import Path
from opening_baseline import settle
from execution_supervisor import stop_gate

OFFICIAL_URL = "https://openapi.twse.com.tw/v1/indicesReport/MI_5MINS_HIST"
DATED_URL = "https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_HIST?date={}&response=json"

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

def fetch_official_month(day):
    url = DATED_URL.format(day[:7].replace("-", "") + "01")
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as response:
        payload = json.load(response)
    if payload.get("stat") != "OK" or not isinstance(payload.get("data"), list):
        raise ValueError("TWSE did not return the requested monthly index history")
    fields = [str(field).strip() for field in payload.get("fields", [])]
    date_index = fields.index("日期")
    opening_index = fields.index("開盤指數")
    return [
        {"Date": row[date_index], "OpeningIndex": row[opening_index]}
        for row in payload["data"] if len(row) > max(date_index, opening_index)
    ]


def audit(queue, root, official_loader=None, month_loader=None):
    root = Path(root)
    result = {"gate": stop_gate(queue, []), "replays": [], "errors": []}
    official_rows = None
    monthly_rows = {}
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
                    row = {}
            if not (row.get("status") == "PASS" and row.get("source_date") == day and row.get("source", "").startswith("TWSE MI_5MINS_HIST")) and month_loader:
                try:
                    month = day[:7]
                    if month not in monthly_rows:
                        monthly_rows[month] = month_loader(day)
                    row = official_open(day, monthly_rows[month])
                    actual_ref = DATED_URL.format(month.replace("-", "") + "01")
                except (ValueError, KeyError, TypeError, OSError) as exc:
                    entry["monthly_fallback_error"] = str(exc)
            if row.get("status") == "PASS" and row.get("source_date") == day and row.get("source", "").startswith("TWSE MI_5MINS_HIST"):
                entry["actual"] = row["open"]
                entry["scores"] = {k: settle(v["center"], row["open"], record["previous_close"]) for k,v in record["models"].items()}
                entry["actual_ref"] = actual_ref
                entry["actual_evidence"] = row
            else:
                entry["blocker"] = "Missing exact-session official TWSE opening in available sources"
            result["replays"].append(entry)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            result["errors"].append({"path": str(path), "error": str(exc)})
    return result

if __name__ == "__main__":
    print(json.dumps(audit(json.loads(Path("docs/repair_queue.json").read_text()), sys.argv[1], fetch_official, fetch_official_month), indent=2))
