# Architecture audit — 2026-10-22

Scope: main branch source tree, workflow definitions, available run outcomes, recent PRs #20–#22, and the agreed user requirements. This is an incremental cleanup, **not** a claim of complete integration validation.

## Product contract
1. **Collect** verifiable observations with original source, exchange/session date, trade timestamp, fetched timestamp, units, and status.
2. **Validate** missing price, prior session, future clock, stale and delayed data separately. No `pz` as last trade; no prior close masquerading as live.
3. **Store** machine-readable snapshots on `data/snapshots`; distinguish source date from collection date.
4. **Analyze** independently using deterministic features; label hypotheses untested until validated out of sample.
5. **Report** morning/night with coverage and explicit unavailable fields. Collection success does not mean report delivery success.
6. **Never trade**; Shioaji is quote-only, no CA activation or order submission.

## Confirmed architecture debt

| Priority | Finding | Impact | Action |
|---|---|---|---|
| P0 | Three writers used three different concurrency groups while pushing the **same** `data/snapshots` branch | Concurrent non-fast-forward push failures / missed updates | **Fixed**: common `data-snapshots-writer` group and one publisher script |
| P0 | Intraday `MIS z='-'` was classified as `STALE_OR_NO_TRADE` even when source time was current | False stale diagnoses | **Fixed**: `NO_LAST_TRADE`, `STALE`, `PRIOR_SESSION`, `FUTURE_TIMESTAMP` separate |
| P0 | Shioaji snapshot timestamp required provider-specific decoding, +8h bug | Fresh quotes rejected | **Regression tests added**, provider-aware decoder retained |
| P1 | Three copies of Git worktree / copy / commit / push shell | Patch drift and divergent failure behavior | **Fixed**: `scripts/publish_snapshots.sh` |
| P1 | `intraday.json` overwrites each query on the same date | Cannot audit multiple intraday observations from branch history without git commit lookup | **Open**: append time-indexed snapshots + latest pointer with retention policy |
| P1 | `market-data.yml` invokes research and backtesting every morning/evening | Expensive repeated historical downloads and backtests; daily data unavailable at 08:25 | **Open**: separate ingestion from nightly research job; incremental history cache |
| P1 | `collect_cross_market.py` requests 1-year US history for many symbols on every cross-market run | FinMind quotas, latency, large JSON and Git churn | **Open**: cache daily bars, refresh at most once per completed market session |
| P1 | `collect_shioaji_night.py` and `collect_intraday.py` duplicate SDK login / TX tick callback | Provider-specific fixes can diverge | **Open**: extract one read-only Shioaji adapter with context-managed session |
| P1 | `collect_market.py` uses external TWSE MCP, but fails whole run if both quote sources fail, including morning when FinMind daily is prior-session | Scheduled report data gaps | **Open**: policy by session; publish partial status and alert, not invented numbers |
| P1 | No automated link from successful snapshot collection to a guaranteed user-visible 08:20/23:00 report | Successful Actions ≠ notification/report delivery | **Open**: explicit delivery job with acknowledgment and missing-report alert |
| P2 | `stock-test.yml` / `fetch_quotes.py` hard-code 3 experimental symbols, separate MIS/Yahoo logic | Redundant diagnostic path; drift from production | **Open**: archive or refactor into provider contract tests after proving parity |
| P2 | Multiple `ieobserve-*`, Fugle and MCP smoke workflows remain in production tree | Test clutter, unrelated CI failures and navigation noise | **Open**: move experimental probes under `experiments/` or disable only after review |
| P2 | `README.md` had two lines | No operational contract / runbook | **Fixed**: architecture and manual operation instructions |
| P2 | `ASSETS.us.user_holdings` contains an unverified `SPCX` symbol | Risk of false holding inference | **Open**: user-approved watchlist in config, holdings separate |
| P2 | 08:25 GitHub Actions cron ≠ user-requested 08:20 delivery; cron can start late | Timing mismatch | **Open**: split ingestion and delivery, enforce SLO / alert |

## Target architecture (do not implement prematurely)

`providers/{shioaji,twse,taifex,finmind,yahoo}.py` -> `models/quote.py` -> `quality/validators.py` -> `storage/snapshot.py` -> `research/{features,backtest}.py` -> `reports/{morning,night}.py`.

Avoid speculative package proliferation now. First stabilize contracts, tests, and scheduler; migrate one module at a time with golden-fixture parity tests.

## Operating / safety constraints
- Free-first: GitHub Actions, official TWSE/TPEx/TAIFEX, Shioaji already configured, FinMind free tier where adequate.
- No broker CA, no order endpoint, no printing secrets, no arbitrary high-frequency snapshot polling.
- Use Shioaji tick subscription for continuous intraday; snapshots for one-shot checks.
- Daily OHLCV, session-final futures, delayed 5-minute Yahoo bars and live ticks **must never** be conflated.
- Morning historical data from previous completed session is expected, not necessarily an error.
- GitHub cron times are UTC and **best effort**; independent delivery acknowledgment needed.

## Verification gate
- Offline Python compilation, unit tests for quote status and timezone, shell syntax.
- Live one-shot workflow to verify provider credentials, data age and symbols (not covered by offline tests).
- Nightclose session and daylight/timezone rollover integration tests before changing schedules.
- Retain original code/probes until a replacement has matching output and passing tests.

## Next staged changes
1. Add immutable intraday run-id/time snapshot files and a latest pointer, plus retention.
2. Extract Shioaji read-only adapter; mock SDK, test quote source timestamps.
3. Split costly historical/backtest refresh from morning collection; add quota-aware caching.
4. Make scheduled report delivery observable with acknowledgment and error notifications.
5. Archive old probes only after usage check; avoid deleting evidence.


## Integration update — 2026-10-22, Issue #24 continuation

PR #23 was already merged before the handoff issue was filed; its branch is not an
unmerged one-file draft. Current work builds from main `9d7fb43`.

Completed integration:
- Shared public clients extracted from the Taiwan collector; cross-market no longer
  imports the Taiwan CLI to access transport.
- Shared read-only Shioaji adapter and cleanup for intraday and TX enrichment.
- One price/clock policy; future dates and fresh cross-midnight ticks are distinct.
- MCP actual `last` and clock checked; observed same-day `last: "-"` no longer PASS.
- Complete-source fallback; no mixed MIS/Shioaji or Yahoo/IEX top-level observations.
- Existing latest snapshot paths retained; immutable observation records added.
- Publisher uses fresh-head retries and isolated worktree cleanup. Replaces global
  concurrency because GitHub concurrency permits only one pending run per group.
- Ingestion publishes independently of research; original research outputs retained,
  exact artifact input survives midnight, derived publishing excludes source files.
- Full offline CI, actual community backtest engine and concurrent Git integration test.

Remaining product/operational work (not claimed complete):
- Guaranteed 08:20/23:00 user report delivery and acknowledgment are outside this
  repository's existing implementation. No report scheduler was changed here.
- Exchange holiday calendar / canonical futures trading-date attribution, direct
  TOPIX index source, SPCX identity validation, daily history caching, data retention.
- Experimental workflows remain available. File moves would break existing probe
  entry points without adding runtime value, so they were not moved in this pass.
- Live source market coverage and quote age must still be read from each snapshot;
  all-source unavailable snapshots remain artifacts and fail publishing as before.


### Acceptance evidence for PR #25

- Local full suite: 24 passing tests; Python compile, shell syntax and whitespace checks pass.
- Actions Quality Gate: `39718421416` (runtime commit `0a575824`).
- Actual Taiwan collection and isolated research: `39718275207`; all seven daily
  datasets retained as PRIOR_SESSION and all seven backtests execute as EXPLORATORY_ONLY.
- Actual read-only intraday SDK/MIS: `39718416834`; 2330/0050 snapshot clocks and TX tick
  freshness pass, missing MIS last trades remain diagnostics rather than live prices.
- Cross-market live collection: `39718416779`; inspect source-specific coverage/age.
- These provider checks ran around 11:42–11:45 Taipei, not during the futures night
  session. Night-session availability is not newly certified by this daytime run.
- Temporary branch-only smoke triggers removed after execution; intraday returns
  to manual-only. The final docs/trigger cleanup does not change runtime code.


## Shioaji-first follow-up and report experiments

Stock quote source order is now Shioaji Tick, single Shioaji snapshot, then MIS.
All seven tracked stocks use one shared session; TX remains a Shioaji Tick.
Simulated auction ticks are excluded, fresh request snapshots remain non-live,
and source selection diagnostics are retained. Daily bars and flows stay separate.

A deterministic report builder and manual three-scenario acceptance workflow produce
morning, evening and current-quote reports with source evidence. Daytime previews
are explicitly labeled and do not certify timed delivery. 08:20/23:00 fixture
regressions verify date selection and withholding incomplete/current-day bars.

### Three-scenario real-source acceptance (PR #26)

Runtime commit `961e412515f4e4634edd67cef6d075a7c384c4e1`, Actions run
[39719869433](https://github.com/champion5566/tw-stock-agent/actions/runs/39719869433).
All three sequential jobs completed successfully:

| Scenario | Actual generation time (Taipei) | Data result |
|---|---|---|
| Morning preview | 2026-10-22 12:01:27 | COMPLETE: seven OHLCV, institutional and margin datasets for 2026-10-21 |
| Evening preview | 2026-10-22 12:03:01 | PARTIAL as expected before close: current-session daily values withheld; TX fresh |
| Immediate query | 2026-10-22 12:03:57 | Seven fresh stock observations, all Shioaji; six stock Ticks, one snapshot; TX fresh |

The 08:20/23:00 policies also pass offline fixtures. These are current-time previews,
not proof of timed execution or night-session availability. Full source JSON and
rendered JSON/Markdown are retained in the run artifacts. Permanent rendered copies:
- [Morning](experiments/2026-10-22-morning.md)
- [Evening](experiments/2026-10-22-evening.md)
- [Immediate](experiments/2026-10-22-intraday.md)

Final cleanup extracts the unchanged watchlist to `instruments.py` so independent
collectors/report rendering do not import another collector just for configuration.
The temporary branch-push experiment trigger is removed; the reusable experiment is
manual-only. No provider, selection or subscription behavior changes in this cleanup.
