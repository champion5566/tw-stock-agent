"""Audit the original report chain at one data-branch revision."""
import argparse
from datetime import datetime, time
import json
from math import isfinite
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

from opening_review import review
from execution_supervisor import stop_gate
from paper_actions import evaluate, summarize
from teacher_audit import DATED_URL, fetch_official_month, official_open

TW = ZoneInfo("Asia/Taipei")
MODELS = {"V0-CARRY", "V1-TX-ZERO-BASIS", "V2-CROSS-BLEND", "V3-SHRINK-075"}


def git(*args):
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()


def original(ref, path):
    history = git("log", "--first-parent", "--format=%H %cI", "--diff-filter=A", ref, "--", path)
    if not history:
        return None
    commit, timestamp = history.splitlines()[-1].split(" ", 1)
    return {"ref": f"{commit}:{path}", "published": timestamp, "text": git("show", f"{commit}:{path}")}


def block(text, name):
    match = re.search(r"(?m)^\[" + re.escape(name) + r"\]\s*$", text)
    if not match:
        return ""
    return re.split(r"(?m)^\[[A-Z_]+\]\s*$", text[match.end():], maxsplit=1)[0].strip()


def prediction(text):
    section = block(text, "PREDICTION_LEDGER")
    start = section.find("{")
    if start < 0:
        raise ValueError("Forecast JSON missing")
    return json.JSONDecoder().raw_decode(section[start:])[0]


def local_time(value):
    stamp = datetime.fromisoformat(value)
    if stamp.tzinfo is None:
        raise ValueError("Missing timezone")
    return stamp.astimezone(TW)


def publication(ref, path):
    # The bundle can change later. Read the exact file-changing commit reachable
    # from the forecast's source revision, never the latest branch file.
    value = git("log", "-1", "--first-parent", "--format=%H %cI", ref, "--", path)
    if not value:
        raise ValueError("No source publication")
    commit, timestamp = value.split(" ", 1)
    return timestamp, json.loads(git("show", f"{commit}:{path}"))


def qualify(ref, day, record):
    if not record:
        return None, "MISSING_ORIGINAL"
    try:
        published = local_time(record["published"])
        if published.date().isoformat() != day or not time(8, 38) <= published.time() < time(9):
            return None, "OUTSIDE_PREOPEN_WINDOW"
        text = record["text"]
        if f"OPEN-{day.replace('-', '')}-AM" not in text:
            return None, "IDENTITY_MISMATCH"
        match = re.search(r"(?i)source ref[ :]+([0-9a-f]{40})", text)
        if not match or subprocess.run(
            ["git", "merge-base", "--is-ancestor", match[1], ref], capture_output=True
        ).returncode:
            return None, "UNVERIFIED_SOURCE_REF"
        timestamp, source = publication(match[1], f"reports/{day}/morning.json")
        clocks = [local_time(source["generated_at_taipei"]), local_time(timestamp)]
        fetched = source["source_fetched_at"]
        clocks.extend(local_time(fetched[key]) for key in ("market", "cross"))
        if any(stamp.date().isoformat() != day or not time(8, 20) <= stamp.time() <= time(8, 38)
               for stamp in clocks):
            return None, "SOURCE_OUTSIDE_CUTOFF"
        if (source.get("execution_kind") != "REPORT" or source.get("scenario") != "morning"
                or source.get("readiness", {}).get("sections", {}).get("cutoff", {}).get("status") != "PASS"):
            return None, "UNQUALIFIED_SOURCE"
        data = prediction(text)
        if data != source.get("opening_forecast"):
            return None, "MODEL_PAYLOAD_MISMATCH"
        if "V0-CARRY" not in data["models"] or not set(data["models"]) <= MODELS:
            return None, "UNSUPPORTED_MODELS"
        numbers = [data["previous_close"], *(model["center"] for model in data["models"].values())]
        if any(type(value) not in (int, float) or not isfinite(value) or value <= 0 for value in numbers):
            return None, "INVALID_MODEL_VALUES"
        return {"date": day, "original_ref": record["ref"], "published_at": record["published"],
                "source_ref": match[1], "models": data["models"],
                "previous_close": data["previous_close"]}, "VERIFIED_PREOPEN_ORIGINAL"
    except (AttributeError, KeyError, TypeError, ValueError, subprocess.CalledProcessError):
        return None, "INVALID_OR_UNAVAILABLE_EVIDENCE"


def session_file(paths, before, slot):
    return next((path for path in reversed(paths)
                 if path.endswith(f"/{slot}.md") and path.split("/")[1] < before), None)


def report_chain(ref, day, paths, actual_loader):
    evening_path = session_file(paths, day, "evening")
    parent = original(ref, evening_path) if evening_path else None
    current = original(ref, f"predictions/{day}/morning.md")
    forecast, status = qualify(ref, day, current)
    result = {
        "date": day, "morning_ref": current["ref"] if current else None,
        "opening_status": status,
        "previous_evening_ref": parent["ref"] if parent else None,
        "previous_evening_state": "AVAILABLE" if parent and block(parent["text"], "RESEARCH_STATE") else "MISSING",
        "same_day_evening_ref": None,
        "next_morning_ref": None,
        "next_morning_handoff": "PENDING",
    }
    evening = original(ref, f"predictions/{day}/evening.md")
    if evening:
        result["same_day_evening_ref"] = evening["ref"]
        following = next((p for p in paths if p.endswith("/morning.md") and p.split("/")[1] > day), None)
        next_morning = original(ref, following) if following else None
        if next_morning:
            state = block(next_morning["text"], "RESEARCH_STATE")
            result["next_morning_ref"] = next_morning["ref"]
            result["next_morning_handoff"] = "VERIFIED" if evening["ref"] in state else "PARENT_REF_MISSING"
    if forecast:
        result.update(forecast)
        try:
            actual = actual_loader(day)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            result["settlement_status"] = "OFFICIAL_SOURCE_UNAVAILABLE"
            result["actual_error"] = type(exc).__name__
        else:
            if actual:
                result.update(actual=actual["open"], actual_ref=actual["ref"], eligible=True,
                              settlement_status="OFFICIAL_SETTLED")
            else:
                result["settlement_status"] = "OFFICIAL_SESSION_UNAVAILABLE"
    return result


def paper_review(ref, paths, as_of):
    quotes = {}
    rows = []
    seen = set()

    def quote(symbol, day):
        if day not in quotes:
            path = f"reports/{day}/evening.json"
            try:
                _, bundle = publication(ref, path)
                quotes[day] = bundle
            except (ValueError, subprocess.CalledProcessError):
                quotes[day] = {}
        bundle = quotes[day]
        item = bundle.get("stocks", {}).get(symbol, {}).get("daily_ohlcv", {})
        if item.get("status") != "PASS" or item.get("source_date") != day:
            return None
        values = item.get("data") or {}
        return {"open": values.get("open"), "high": values.get("max"), "low": values.get("min"),
                "volume": values.get("Trading_Volume"), "ref": f"{ref}:reports/{day}/evening.json"}

    for path in paths[-80:]:
        if not path.endswith(("/morning.md", "/evening.md")) or path.split("/")[1] > as_of:
            continue
        record = original(ref, path)
        if not record:
            continue
        for section in re.finditer(r"(?ms)^\\[ACT\\][ \\t]*\\n(.*?)(?=^\\[[A-Z_]+\\][ \\t]*$|\\Z)", record["text"]):
            raw = section[1].strip()
            if raw.startswith("```json"):
                raw = raw.removeprefix("```json").removesuffix("```").strip()
            try:
                action = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(action, dict) or not isinstance(action.get("id"), str):
                continue
            if action["id"] in seen:
                continue
            seen.add(action["id"])
            row = evaluate(action, local_time(record["published"]), quote, as_of)
            rows.append({**row, "original_ref": record["ref"]})
    return {"rows": rows, "metrics": summarize(rows)}


def document_status(paths, required):
    return {path: "PRESENT_AT_PINNED_COMMIT" if path in paths else "MISSING_AT_PINNED_COMMIT"
            for path in required}


def audit(ref, as_of):
    paths = sorted(path for path in git("ls-tree", "-r", "--name-only", ref, "--", "predictions").splitlines()
                   if re.fullmatch(r"predictions/\d{4}-\d{2}-\d{2}/(morning|evening)\.md", path))
    days = sorted({p.split("/")[1] for p in paths if re.fullmatch(
        r"predictions/\d{4}-\d{2}-\d{2}/morning\.md", p) and p.split("/")[1] <= as_of})[-20:]
    days = sorted({*days, as_of})
    months = {}

    def actual(day):
        month = day[:7]
        if month not in months:
            try:
                months[month] = fetch_official_month(day)
            except (ValueError, KeyError, TypeError, OSError) as exc:
                months[month] = exc
        if isinstance(months[month], Exception):
            raise months[month]
        row = official_open(day, months[month])
        if row:
            row["ref"] = DATED_URL.format(month.replace("-", "") + "01") + "#session=" + day
        return row

    chain = [report_chain(ref, day, paths, actual) for day in days]
    latest = chain[-1]
    try:
        _, morning = publication(ref, f"reports/{as_of}/morning.json")
        breadth = morning.get("market_context", {}).get("breadth", {})
    except (ValueError, subprocess.CalledProcessError):
        breadth = {}
    corrections = []
    if breadth.get("status") == "PASS" and breadth.get("declines", 0) > 0:
        corrections.append({
            "id": f"BREADTH-{as_of}", "scope": "prior-session TWSE stocks",
            "source": breadth,
            "rule": "Describe breadth with counts. Broad advance does not establish limit-up breadth or a confirmed reversal.",
        })

    code = git("rev-parse", "HEAD")
    tree = set(git("ls-tree", "-r", "--name-only", code).splitlines())
    required = ("docs/REPORT_CONTRACT.md", "docs/OPERATIONS.md", "docs/PROVIDER_POLICY.md",
                "docs/REVIEW_AGENT.md", "docs/REPORT_PLAYBOOK.md")
    documents = document_status(tree, required)
    raw_queue = git("show", f"{code}:docs/repair_queue.json")
    queue = json.loads(raw_queue)
    attempts = []
    gate = stop_gate(queue, attempts)
    # Each entry gets an actual evidence lookup. Retain continuation for items
    # that still require a patch or independent report-consumer verification.
    for pending in gate["unattempted_or_incomplete"]:
        issue = pending["id"]
        evidence = {
            "opening-directional-model": latest["opening_status"],
            "opening-producer": latest["morning_ref"],
            "opening-settlement": latest.get("settlement_status"),
            "extreme-event-research": [record["id"] for record in corrections],
            "stock-close-regression": "reports",
            "nikkei-fresh-fallback": "cross_market",
            "evening-publication-gap": latest["same_day_evening_ref"],
            "private-draft-validation": "PRIVATE_DRAFT_REQUIRES_CONSUMER_EVIDENCE",
        }.get(issue)
        if evidence in ("reports", "cross_market"):
            try:
                _, bundle = publication(ref, f"reports/{as_of}/morning.json")
                sections = bundle.get("readiness", {}).get("sections", {})
                evidence = sections.get("asia_open" if issue == "nikkei-fresh-fallback" else "required_stock_data")
            except (ValueError, subprocess.CalledProcessError):
                evidence = None
        attempts.append({"id": issue, "action": pending["next"], "outcome": "CHECKED",
                         "evidence": evidence, "data_revision": ref})
    gate = stop_gate(queue, attempts)
    return {"data_revision": ref, "code_revision": code, "as_of_taipei": as_of,
            "chain": chain, "formal_opening": review(chain), "corrections": corrections,
            "paper_research": paper_review(ref, paths, as_of),
            "documentation": documents, "attempts": attempts, "repair_gate": gate}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-ref", required=True)
    parser.add_argument("--as-of", default=datetime.now(TW).date().isoformat())
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    ref = git("rev-parse", "--verify", "--end-of-options", args.data_ref + "^{commit}")
    result = audit(ref, args.as_of)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"latest": result["chain"][-1], "formal_opening": result["formal_opening"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
