"""Backward-compatible latest snapshots plus immutable observation history."""
import json
import os
import re
from datetime import date
from pathlib import Path
from uuid import uuid4


def write_snapshot(payload, collection_date, name, root="out"):
    date.fromisoformat(collection_date)
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise ValueError("Invalid snapshot name")
    directory = Path(root) / collection_date
    directory.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False, default=str) + "\n"
    run = os.getenv("GITHUB_RUN_ID", "local")
    attempt = os.getenv("GITHUB_RUN_ATTEMPT", "1")
    # UUID also distinguishes multiple writes in the same run.
    archive = directory / "observations" / name / f"{run}-{attempt}-{uuid4().hex}.json"
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_text(body, encoding="utf-8")
    latest = directory / (name + ".json")
    temporary = latest.with_suffix(".tmp")
    temporary.write_text(body, encoding="utf-8")
    temporary.replace(latest)
    return latest
