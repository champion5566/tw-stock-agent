"""Shared entrypoint: run from repo root with python -m scripts.repair_session."""
import argparse
import json
from pathlib import Path
from execution_supervisor import stop_gate

def session(queue, attempts, mode):
    result = stop_gate(queue, attempts)
    return {"mode": mode, **result}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["interactive", "scheduled"], required=True)
    p.add_argument("--queue", default="docs/repair_queue.json")
    p.add_argument("--attempts")
    a = p.parse_args()
    queue = json.loads(Path(a.queue).read_text(encoding="utf-8"))
    attempts = json.loads(Path(a.attempts).read_text(encoding="utf-8")) if a.attempts else []
    result = session(queue, attempts, a.mode)
    print(json.dumps(result, indent=2))
    return 0 if result["stop_allowed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
