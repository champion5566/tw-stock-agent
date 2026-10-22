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
