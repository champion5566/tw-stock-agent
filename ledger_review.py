"""Read-only settlement of explicit close rules; never reconstruct predictions.

Uses an exact data branch revision. Outcomes are provider matches, not proof of
forecast publication, tradability, calibration, or a composite prediction score.
"""
import argparse
from collections import Counter
from datetime import datetime, time
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Taipei")


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def finite(value):
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def mapping(value):
    return value if isinstance(value, dict) else {}


def predictions(text):
    """Only parse original prediction block, not repeated recap text."""
    block = re.search(r"\[PREDICTION_LEDGER\](.*?)\[/PREDICTION_LEDGER\]", text, re.S)
    if not block:
        return []
    chunks = re.split(r"(?m)^PREDICTION_ID:\s*", block.group(1))[1:]
    output = []
    for chunk in chunks:
        lines = chunk.splitlines()
        fields = {key.strip(): value.strip() for line in lines[1:]
                  if ":" in line for key, value in [line.split(":", 1)]}
        output.append({"id": lines[0].strip(), "fields": fields})
    return output


def settle(prediction, load, as_of):
    fields, pid = prediction["fields"], prediction["id"]
    result = {"id": pid, "original_text": fields.get("原始字句"),
              "original_threshold": fields.get("數字門檻"),
              "formal_score_eligible": False}
    threshold = fields.get("數字門檻", "")
    if threshold.startswith("N/A") or pid.startswith("OPEN-"):
        return dict(result, status="NOT_TESTED", reason="NO_SUPPORTED_CLOSE_RULE")
    # Conditions require explicit evaluation; silently discarding them creates false hits.
    if "conditional" in threshold.lower():
        return dict(result, status="UNVERIFIABLE", reason="CONDITIONAL_RULE_NEEDS_REVIEW")
    rule = re.fullmatch(
        r"([A-Za-z0-9 -]+?)\s+close\s*(<=|>=|<|>)\s*(?:TWD\s*)?"
        r"((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(?:\s+TWD)?", threshold)
    if not rule:
        return dict(result, status="UNVERIFIABLE", reason="RULE_NOT_SUPPORTED_NO_INFERENCE")
    tokens = rule.group(1).split()
    if any(not re.fullmatch(r"official|TWSE|TPEx|regular|regular-session|TAIEX|\d{4,6}|\d{4}-\d{2}-\d{2}", t)
           for t in tokens):
        return dict(result, status="UNVERIFIABLE", reason="RULE_NOT_SUPPORTED_NO_INFERENCE")
    target = re.search(r"\d{4}-\d{2}-\d{2}", fields.get("期間", ""))
    if not target:
        return dict(result, status="UNVERIFIABLE", reason="NO_EXPLICIT_TARGET_DATE")
    day = target.group()
    result["target_date"] = day
    if any(re.fullmatch(r"\d{4}-\d{2}-\d{2}", t) and t != day for t in tokens):
        return dict(result, status="UNVERIFIABLE", reason="RULE_TARGET_DATE_MISMATCH")
    try:
        session_end = datetime.combine(datetime.fromisoformat(day).date(), time(14), TZ)
    except ValueError:
        return dict(result, status="UNVERIFIABLE", reason="INVALID_TARGET_DATE")
    # Never settle an unfinished session using data accidentally present in a fixture/ref.
    if as_of < session_end:
        return dict(result, status="PENDING", reason="TARGET_SESSION_NOT_COMPLETED")
    stock = re.search(r"-(\d{4,6})-", pid)
    if stock:
        code = stock.group(1)
    elif "-MKT-" in pid:
        code = "TAIEX"
    else:
        return dict(result, status="UNVERIFIABLE", reason="UNKNOWN_INSTRUMENT")
    instruments = [t for t in tokens if t == "TAIEX" or re.fullmatch(r"\d{4,6}", t)]
    if instruments != [code]:
        return dict(result, status="UNVERIFIABLE", reason="RULE_INSTRUMENT_MISMATCH")
    path = f"reports/{day}/evening.json"
    raw = load(path)
    if raw is None:
        return dict(result, status="UNVERIFIABLE", reason="OUTCOME_REPORT_MISSING")
    try:
        report = json.loads(raw)
    except (TypeError, ValueError):
        return dict(result, status="UNVERIFIABLE", reason="INVALID_OUTCOME_JSON")
    if not isinstance(report, dict):
        return dict(result, status="UNVERIFIABLE", reason="INVALID_OUTCOME_SHAPE")
    try:
        generated = datetime.fromisoformat(report["generated_at_taipei"])
        if generated.tzinfo is None or generated > as_of:
            return dict(result, status="UNVERIFIABLE", reason="FUTURE_OR_UNZONED_OUTCOME")
    except (ValueError, KeyError, TypeError):
        return dict(result, status="UNVERIFIABLE", reason="OUTCOME_GENERATION_TIME_MISSING")
    if code == "TAIEX":
        section = mapping(mapping(report.get("market_context")).get("TAIEX"))
        actual = finite(section.get("close"))
        field = "$.market_context.TAIEX.close"
        source = section.get("source")
    else:
        stock_data = mapping(mapping(report.get("stocks")).get(code))
        section = mapping(stock_data.get("daily_ohlcv"))
        row = mapping(section.get("data"))
        actual = finite(row.get("close"))
        field = f"$.stocks['{code}'].daily_ohlcv.data.close"
        source = mapping(stock_data.get("metrics")).get("source")
        if row.get("date") != day or str(row.get("stock_id")) != code:
            return dict(result, status="UNVERIFIABLE", reason="OUTCOME_IDENTITY_OR_DATE_MISMATCH")
    if section.get("status") != "PASS" or section.get("source_date") != day or actual is None or actual <= 0:
        return dict(result, status="UNVERIFIABLE", reason="OUTCOME_SECTION_NOT_CURRENT_PASS")
    if not source:
        return dict(result, status="UNVERIFIABLE", reason="OUTCOME_SOURCE_UNSPECIFIED")
    op, value = rule.group(2), float(rule.group(3).replace(",", ""))
    hit = {"<": actual < value, "<=": actual <= value,
           ">": actual > value, ">=": actual >= value}[op]
    return dict(result, status="PROVIDER_MATCHED", outcome="HIT" if hit else "MISS",
                actual=actual, operator=op, threshold=value,
                evidence={"path": path, "field": field, "source": source,
                          "source_date": day, "sha256": digest(raw),
                          "report_generated_at": report.get("generated_at_taipei")},
                reason="OUTCOME_ONLY_NOT_TIMELY_FORECAST_CERTIFICATION")


def audit(ledgers, load, as_of, revision):
    results, errors = [], []
    for path, text in sorted(ledgers.items()):
        for prediction in predictions(text):
            result = settle(prediction, load, as_of)
            result.update(original_path=path, original_sha256=digest(text))
            results.append(result)
        if path == "predictions/2026-11-04/evening.md" and "TWD 11148.21 billion" in text:
            errors.append({"id": "ERR-20261104-PM-TURNOVER-UNIT", "original_path": path,
                           "original_sha256": digest(text),
                           "original": "TWD 11148.21 billion",
                           "conditional_conversion": "11,148.21 億元 = TWD 1114.821 billion",
                           "basis": "11,148.21 億元 * 100,000,000 / 1,000,000,000",
                           "status": "SUSPECTED_UNIT_ERROR_NEEDS_SOURCE_RECONCILIATION",
                           "unit_conversion_factor": 10,
                           "scope_note": "Unit conversion only; do not substitute differently scoped totals."})
    return {"schema_version": "ledger-review-v1", "as_of_taipei": as_of.isoformat(),
            "data_revision": revision, "results": results, "errata": errors,
            "counts": dict(Counter(x["status"] for x in results)),
            "outcome_counts": dict(Counter(x["outcome"] for x in results if "outcome" in x)),
            "warning": "Provider outcome verification only. No aggregate accuracy/alpha claim; "
                       "publication, original timing, dependent samples and full report grades remain separate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-ref", default="origin/data/snapshots")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    # Resolve a commit once; no shell interpretation or moving-ref reads afterwards.
    revision = subprocess.check_output(
        ["git", "rev-parse", "--verify", "--end-of-options", args.data_ref + "^{commit}"], text=True).strip()
    names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", revision], text=True).splitlines()
    available, cache = set(names), {}

    def load(path):
        if path not in available:
            return None
        if path not in cache:
            cache[path] = subprocess.check_output(["git", "show", f"{revision}:{path}"], text=True)
        return cache[path]

    ledgers = {path: load(path) for path in names
               if re.fullmatch(r"predictions/\d{4}-\d{2}-\d{2}/(?:morning|evening)\.md", path)}
    result = audit(ledgers, load, datetime.now(TZ), revision)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    # New result artifact only; never overwrite originals or prior evaluations.
    with output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"path": str(output), "ledgers": len(ledgers), "counts": result["counts"],
                      "outcome_counts": result["outcome_counts"], "errata": len(result["errata"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
