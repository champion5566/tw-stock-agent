"""Read-only TX night-session quote snapshot using the validated Shioaji SDK.
No orders, no CA activation, no secret values in output.
"""
import json
import os
from datetime import datetime
from pathlib import Path

from quote_quality import TW
from shioaji_quotes import collect_quotes
from snapshot_io import write_snapshot


def main():
    now = datetime.now(TW)
    slot = os.getenv("REPORT_SLOT", "evening")
    path = Path("out") / now.date().isoformat() / ("cross-" + slot + ".json")
    if not path.exists():
        raise SystemExit("Cross-market snapshot must exist before quote enrichment")
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    result = (collect_quotes(wait_seconds=35) if slot == "evening" else
              collect_quotes(future_snapshot=True, stream=False))
    key = "shioaji_live_tx" if slot == "evening" else "shioaji_session_tx"
    snapshot.setdefault("taifex", {})[key] = result
    write_snapshot(snapshot, now.date().isoformat(), "cross-" + slot)
    print("SHIOAJI_TX", result["status"], result.get("price"),
          result.get("trade_time"), "age_min", result.get("age_minutes"))


if __name__ == "__main__":
    main()
