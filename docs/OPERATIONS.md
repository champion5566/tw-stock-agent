# Operations and handoff

## Prepare via the connected GitHub file tool

The connector currently supports creating files but exposes no workflow-dispatch tool.
Use GitHub's native push event rather than a new hosting or credential dependency.
Read `main` first, then create this **new** file on `main`:

`preparation/requests/YYYY-MM-DD/morning.json` (or `evening.json`)

```json
{"schema_version":"preparation-request-v1","slot":"morning","requested_at_taipei":"<actual timezone-aware current Taipei timestamp>"}
```

Requests contain only these public operational fields. Never include holdings or account
information. The path/date/slot/schema and timestamp are validated; stale, future and
multiple requests in one push are rejected. One file per date/slot gives idempotency:
if already present, inspect its matching run rather than overwriting or repeatedly triggering.
This is an explicitly authorized preparation request, separate from prediction-ledger writes.

Check the `Cross Market Source Verification` run for that exact request commit. Its
resolved slot must match; check source steps, artifact, publication and exact readback.
A create-file response proves the request commit, not successful collection. If late,
still diagnose the run and preserve evidence; never backdate the request or forecast.

Morning request 08:20 weekdays; evening request 22:50 weekdays. At invocation confirm the
current slot/window. If already past cutoff, do not trigger collection just to backfill an
on-time forecast. Report the late trigger and retain native backup diagnostics.
Native 08:30/08:35 and 22:52 schedules remain available; all cross-market runs serialize
broker sessions through their existing concurrency group. GitHub permits only one pending
run per group, so pending backups can be replaced; do not claim all requests executed.

## Verify and merge

1. Inspect live branch and existing implementation before edits; research maintained
   solutions before adding infrastructure. Work on a feature branch.
2. Run `bash scripts/verify.sh`; inspect diff and targeted regression cases.
3. Open a PR; verify its actual Quality Gate before merging the exact tested head.
4. Inspect the post-merge source run, actual version, input/output clocks and report
   readback. Record partial datasets separately from code/transport failures.
5. Observe actual morning/night scheduled occurrences before certifying punctuality.

## Report consumer

Pin `data/snapshots` to a concrete commit. Prefer `reports/YYYY-MM-DD/{slot}.json`;
read the file-changing commit time and check it against cutoff. If it is missing or late,
state that at the start of the report and perform only targeted source checks. Supplemental
current data must not retroactively qualify a pre-open sample. Read original parent ledger,
create the new public-only ledger without overwriting, and verify exact text by readback.

Separate workflow success, DATA_READY/PARTIAL, publication, ledger and report output.
Keep DELIVERY_ACK=UNKNOWN unless an independent acknowledgment exists. Preserve the
current A–L requirements and opening prediction/verification blocks.

## Diagnose

- Request exists, no run: check Actions push trigger and actual request commit.
- Run created late: scheduler/queue delay; source code tests cannot certify recovery.
- Slow run: inspect provider timings; report profile excludes annual US downloads.
- Ready stocks but partial report: inspect each failed section; never relax coverage.
- After-cutoff retry: inspect publication-observations; timely package should remain selected.
- Missing night data: check nightclose source clock; never substitute a day quote.
- Source unavailability: retain partial output and explain exact missing fields.

## Rollback

Revert the upgrade merge using a new PR, restore previous automation prompts from the
private task history, and pause the two preparation tasks. Keep original ledgers and
immutable data evidence. Do not force-push main or delete historical observations.

## Handoff record

Record source revision/PR, checks executed, CI/run links, published file revision,
remaining gaps, next target-time observation and whether user action is actually needed.
This durable project record replaces relying on conversational recollection; no automatic
session observer or self-learning hook is enabled.
