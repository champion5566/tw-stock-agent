#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
python -m compileall -q .
python -m unittest discover -s tests -v
bash -n scripts/publish_snapshots.sh
git diff --check
