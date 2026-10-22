#!/usr/bin/env bash
# All snapshot-writing workflows share the same GitHub Actions concurrency group.
set -euo pipefail
test -d "$GITHUB_WORKSPACE/out" || { echo "No output directory"; exit 1; }
git fetch origin data/snapshots
git worktree add --detach /tmp/stock-snapshots origin/data/snapshots
cd /tmp/stock-snapshots
git checkout -B data/snapshots origin/data/snapshots
cp -R "$GITHUB_WORKSPACE/out/." .
git add -- '*.json'
if git diff --cached --quiet; then
  echo 'No snapshot changes'
  exit 0
fi
git -c user.name='github-actions[bot]' -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
  commit -m "Market data ${REPORT_SLOT:-manual} $(date -u +%Y-%m-%dT%H:%MZ)"
git push origin HEAD:data/snapshots
