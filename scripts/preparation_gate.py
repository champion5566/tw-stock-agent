"""Choose whether an existing preparation trigger needs provider work."""
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, time

from scripts.publish_overlay import timestamp
from scripts.resolve_preparation import SLOTS, TW, resolve

WINDOWS = {"morning": (time(8, 20), time(8, 38)), "evening": (time(22, 50), time(22, 58))}
PREPARATION_KINDS = {"SCHEDULED_PREPARATION", "REQUEST_PREPARATION"}


def within_window(slot, now):
    start, cutoff = WINDOWS[slot]
    return now.weekday() < 5 and start <= now.time() < cutoff


def complete_publication(slot, now, bundle, committed_at):
    if not bundle or not committed_at:
        return False
    generated = timestamp(bundle.get("generated_at_taipei"))
    published = timestamp(committed_at)
    if not generated or not published:
        return False
    generated, published = generated.astimezone(TW), published.astimezone(TW)
    start, cutoff = WINDOWS[slot]
    readiness = bundle.get("readiness", {})
    return (
        bundle.get("scenario") == slot
        and bundle.get("execution_kind") == "REPORT"
        and generated.date() == published.date() == now.date()
        and start <= generated.time() <= published.time() <= cutoff
        and published <= now
        and readiness.get("data_readiness") == "DATA_READY"
        and readiness.get("sections", {}).get("cutoff", {}).get("status") == "PASS"
    )


def decision(slot, kind, now, bundle=None, published_at=None):
    if kind not in PREPARATION_KINDS or slot not in WINDOWS:
        return "COLLECT"
    if not within_window(slot, now):
        return "SKIP_OUTSIDE_WINDOW"
    if complete_publication(slot, now, bundle, published_at):
        return "SKIP_DUPLICATE_READY"
    return "COLLECT"


def published_bundle(slot, now):
    path = f"reports/{now.date().isoformat()}/{slot}.json"
    subprocess.run(["git", "fetch", "origin", "refs/heads/data/snapshots"], check=True)
    revision = subprocess.check_output(["git", "rev-parse", "FETCH_HEAD"], text=True).strip()
    info = subprocess.check_output(
        ["git", "log", "-1", "--first-parent", "--format=%H %cI", revision, "--", path],
        text=True,
    ).strip()
    if not info:
        return None, None, revision
    commit, published = info.split(" ", 1)
    body = subprocess.check_output(["git", "show", f"{revision}:{path}"], text=True)
    return json.loads(body), published, commit


def main():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    event_name = os.environ["GITHUB_EVENT_NAME"]
    changed = []
    if event_name == "push":
        # The push can contain more than one commit; inspect the event's whole range.
        before, after = event["before"], event["after"]
        if subprocess.run(["git", "cat-file", "-e", before], capture_output=True).returncode:
            subprocess.run(["git", "fetch", "origin", before], check=True)
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=AM", before, after], text=True
        ).splitlines()
    now = datetime.now(TW)
    scheduled_slot = SLOTS.get(event.get("schedule")) if event_name == "schedule" else None
    if event_name == "push" and not any(path.startswith("preparation/requests/") and path.endswith(".json") for path in changed):
        slot, kind = "none", "PREVIEW"
    elif scheduled_slot in WINDOWS and not within_window(scheduled_slot, now):
        slot, kind = scheduled_slot, "SCHEDULED_PREPARATION"
    else:
        slot, kind = resolve(event, event_name, now, changed)
    selected = decision(slot, kind, now)
    revision = published = error = None
    if event_name == "push" and kind == "PREVIEW":
        selected = "SKIP_CODE_PUSH"
    elif selected == "COLLECT" and kind in PREPARATION_KINDS and slot in WINDOWS:
        try:
            bundle, published, revision = published_bundle(slot, now)
            selected = decision(slot, kind, datetime.now(TW), bundle, published)
        except (ValueError, subprocess.CalledProcessError) as exc:
            error = type(exc).__name__
            selected = decision(slot, kind, datetime.now(TW))
    evidence = {"slot": slot, "mode": kind, "trigger": event_name, "observed_at_taipei": now.isoformat(),
                "decision": selected, "published_revision": revision, "published_at": published,
                "readback_error": error}
    body = json.dumps(evidence, sort_keys=True)
    Path("preparation-gate.json").write_text(body + "\n", encoding="utf-8")
    print(f"PREPARATION_GATE {body}")
    if selected == "SKIP_OUTSIDE_WINDOW":
        print("::warning::Preparation reached the runner outside its Taipei collection window")
    with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as stream:
        print(f"REPORT_SLOT={slot}", f"PREPARATION_KIND={kind}",
              f"PREPARATION_STARTED_AT={now.isoformat()}", sep="\n", file=stream)
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
        print(f"collect={'true' if selected == 'COLLECT' else 'false'}", file=stream)


if __name__ == "__main__":
    main()
