# tw-stock-agent

Read-only public market research pipeline. Shioaji is quote-only; no orders or CA activation.

## Current operating contract

| Item | Asia/Taipei |
|---|---|
| Morning preparation request | 08:20 weekdays; never collect earlier |
| Native morning backup | 08:30 and 08:35 weekdays |
| Morning cutoff / report target | **08:38 / 08:40** |
| Evening Taiwan background refresh | 22:15 weekdays |
| Evening preparation request / native backup | 22:50 / 22:52 weekdays |
| Evening cutoff / report target | **22:58 / 23:00** |
| Night-session historical observation | 05:35 Tue–Sat |
| Weekly reporting | Existing Sunday 19:00 ChatGPT task |

Schedules are best effort. See [report contract](docs/REPORT_CONTRACT.md) and
[operations](docs/OPERATIONS.md) for evidence requirements and failure handling.

## Data flow

GitHub native schedules or validated `preparation/requests/YYYY-MM-DD/{morning,evening}.json`
pushes start `cross-market.yml`. Each report run collects its own Taiwan input, then
cross-market observations and quote-only TX. Morning can reuse the previously collected
nightclose observation only if the original trade timestamp matches the completed night.

The `report` collection profile excludes annual US history and limits Taiwan history to
60 calendar days (still validated for actual 5/20-session features). The default `full`
CLI profile preserves the prior long-history research behavior. `market-data.yml` still
publishes ingestion separately from its existing research/backtesting job.

Source snapshots and small `reports/YYYY-MM-DD/{morning,evening}.json` bundles are
published on `data/snapshots`. Original source clocks, input SHA-256 fingerprints,
run/commit identity, per-section readiness and immutable observations remain available.
Later/weaker report retries cannot replace a timely, stronger report bundle; every
publication candidate is archived under `publication-observations`.

`publication_check_at_taipei` is a **pre-push** check, not proof of publication. Consumers
must verify the file-changing GitHub commit timestamp and reread the exact revision.
`formal_sample_eligible` stays false in data packages: only the reporting/ledger audit
can establish original pre-open predictions and complete qualification evidence.

## Verification

```bash
python -m pip install -r requirements-test.txt
bash scripts/verify.sh
```

Offline tests cover source and clock semantics, calendars/DST, report requirements,
late retries, request validation, completed-night reuse and concurrent Git publishing.
Live data availability, actual scheduled completion and user notification receipt are
separate acceptance checks.

## Scope and remaining gaps

Required instruments: 0050/006208/00631L/2330/3707/5483. Optional observations
2313/2367/3491 never imply ownership. Public artifacts contain no private positions.
FinMind shares and provider-native credit units remain distinct. Actual TOPIX,
market-wide context and unavailable US completed-session bars remain explicit blockers;
this upgrade does not lower requirements to manufacture DATA_READY.

Experimental `ieobserve-*`, Fugle, `stock-test` and MCP probes remain separate from
production report readiness. Historical architecture/experiment notes are retained as
historical evidence; the current contract supersedes their older schedule notes.

[ECC workflow adoption](docs/ECC_ADOPTION.md) describes the reused engineering approach.
No global ECC plugin, background learner, new paid service or replacement quote stack
is required.
