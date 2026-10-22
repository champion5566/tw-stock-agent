#!/usr/bin/env bash
# Optimistic Git transaction: each retry overlays this run's files on latest HEAD.
set -euo pipefail
workspace=${GITHUB_WORKSPACE:?GITHUB_WORKSPACE required}
test -d "$workspace/out" || { echo 'No output directory'; exit 1; }
temporary=$(mktemp -d)
cleanup() { git -C "$workspace" worktree remove --force "$temporary/tree" >/dev/null 2>&1 || true; rm -rf "$temporary"; }
trap cleanup EXIT
for attempt in 1 2 3 4 5; do
  git -C "$workspace" fetch origin refs/heads/data/snapshots
  base_sha=$(git -C "$workspace" rev-parse FETCH_HEAD)
  if [ -d "$temporary/tree" ]; then
    git -C "$temporary/tree" reset --hard "$base_sha"
  else
    git -C "$workspace" worktree add --detach "$temporary/tree" "$base_sha"
  fi
  cp -R "$workspace/out/." "$temporary/tree/"
  git -C "$temporary/tree" add -- '*.json'
  if git -C "$temporary/tree" diff --cached --quiet; then
    echo 'No snapshot changes'; exit 0
  fi
  git -C "$temporary/tree" -c user.name='github-actions[bot]' \
    -c user.email='41898282+github-actions[bot]@users.noreply.github.com' \
    commit -m "Market data ${REPORT_SLOT:-manual} $(date -u +%Y-%m-%dT%H:%MZ)"
  if git -C "$temporary/tree" push origin HEAD:refs/heads/data/snapshots; then exit 0; fi
  echo "Concurrent update; retry $attempt/5"
done
echo 'Snapshot publish failed after 5 attempts' >&2
exit 1
