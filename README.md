# tw-stock-agent — 台股研究 Agent

Read-only market data pipeline; **not** an execution or trading bot.

## Production entrypoints

| Workflow | Purpose | Trigger | Output |
|---|---|---|---|
| Market Data Snapshots | TW historical daily OHLCV, institutional, margin, research baseline | 08:25 / 20:40 Taipei (GitHub best effort), manual | `out/YYYY-MM-DD/{morning,evening}.json`, research/backtest |
| Cross Market Source Verification | US/JP/KR quotes and TAIFEX data | 05:35 / 08:30 / 22:45 Taipei, manual | `out/YYYY-MM-DD/cross-{slot}.json` |
| Intraday Read-only Quote On Demand | TWSE MIS indices + Shioaji stock and TX quotes | **Manual only** | `out/YYYY-MM-DD/intraday.json` |

The latest dated snapshots are committed to the `data/snapshots` branch. A successful workflow **does not** certify every symbol is current or that a ChatGPT report was delivered. Inspect per-symbol `status` and `trade_time`.

## Data policy
- Shioaji: read-only quote credentials via Actions secrets `SHIOAJI_API_KEY` and `SHIOAJI_SECRET_KEY`; no CA / orders.
- TWSE MIS: `z='-'` means missing last-trade price; never substitute `pz` or previous close.
- FinMind: historical data; daily bars are not a substitute for live ticks.
- Explicit freshness and source timestamps; `quote_quality.py` holds shared checks.
- Snapshot writers use one retrying publisher script; independent workflow concurrency avoids dropped cross-workflow queues.

## Verify
```bash
python -m compileall -q .
python -m unittest discover -s tests -p 'test_quote_quality.py' -v
bash -n scripts/publish_snapshots.sh
```

See [architecture audit](docs/ARCHITECTURE_AUDIT.md) for known issues, migration stages and operational risks.

## Scope note
The older `stock-test`, `mcp-smoke`, `ieobserve-*` and Fugle workflows are experimental probes, **not** report delivery. Do not treat their red CI state as proof of core quote-feed failure.

## Integrated pipeline

The public CLI entry points remain unchanged. Shared modules have one responsibility:

| Module | Responsibility |
|---|---|
| `market_sources.py` | Existing TWSE MCP / FinMind HTTP clients and source failures |
| `shioaji_quotes.py` | One read-only SDK session, stock snapshots, TX ticks and cleanup |
| `quote_quality.py` | Positive finite prices, provider clocks, daily versus live quality, complete-source selection |
| `snapshot_io.py` | Latest JSON at existing paths and immutable observations |
| `collect_*.py` | Orchestration and existing output envelopes |
| `research_ledger.py`, `backtest_baseline.py` | Offline analysis of an explicitly selected collected snapshot |

`Market Data Snapshots` publishes collection **before** the separate `research` job.
Research consumes the same run's artifact, including across midnight; it never blocks
collection publishing and publishes only its own research/backtest files. Morning
and evening research outputs remain available. All existing cron times are retained.

Publishing uses a bounded fetch/overlay/push retry with no force push. Independent
workflows no longer share GitHub's single pending concurrency slot (which could cancel
queued runs). Each publisher has a temporary worktree and removes it on success or failure.

Snapshots keep the existing `YYYY-MM-DD/{slot}.json`, `cross-{slot}.json` and
`intraday.json` paths. Additional immutable observations live under
`YYYY-MM-DD/observations/{name}/{run}-{attempt}-{uuid}.json`. `latest` means latest
published observation, not a promise of a live trade. No automatic historical deletion
is enabled; repository growth/retention remains an operational follow-up.

## Quality contract

| Value | Meaning |
|---|---|
| `PASS` on a quote with `is_live: true` | Positive finite trade with source timestamp within freshness tolerance |
| `PASS` on `data_kind: daily` | Source date is the requested calendar date; never a live quote |
| `PRIOR_SESSION` | Previous date within daily tolerance, or an older-date quote outside live tolerance |
| `NO_LAST_TRADE`, `NO_TIMESTAMP` | Price or source clock absent; collection time never fills either gap |
| `FUTURE_TIMESTAMP`, `STALE` | Source clock is future or outside freshness tolerance |
| `HISTORICAL_BAR` | Yahoo observation outside the collector's bar-age tolerance |
| `MISSING`, `FAIL`, `ERROR`, `NOT_CONFIGURED`, `NO_TICKS_IN_WINDOW` | Inspect source diagnostics; never infer zero or prior close |

Daily tolerance is a documented calendar-day heuristic, **not** an exchange holiday
calendar. A fresh tick just before midnight can remain live after midnight. Source
exchange trading dates are kept independently; no weekend/holiday trading date is invented.
MCP uses the actual `last` field and source `date` + `time`; a same-day `last: "-"`
is `NO_LAST_TRADE`. Selecting Shioaji or IEX keeps that source's fields and timestamps;
MIS/Yahoo OHLC is available only in the nested diagnostic, never silently combined.
The legacy `fetch_quotes.py` CLI now also requires a fresh quote after market close.

Full verification:

```bash
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
python -m compileall -q .
bash -n scripts/publish_snapshots.sh
```

The suite includes provider cleanup/failure isolation, missing-price regression,
midnight handling, collector/storage integration, real `backtesting.py` execution,
workflow schedule contracts and simultaneous Git publishers. Test fixtures do not
substitute for live-provider availability checks. Experimental probes retain their
original entry points and workflows; they do not control production publishing.

Existing GitHub ingestion starts at **08:25**, while requested report delivery is
08:20/23:00 in ChatGPT. This repository does not yet contain a report delivery or
acknowledgment service. Neither the current refactor nor a green Actions run certifies
those reports were delivered. Schedule changes require a separate delivery design.

## Shioaji-first quote policy and three-scenario experiment

Taiwan stock queries now use **Shioaji stock Tick -> one Shioaji snapshot -> MIS**.
TX continues to use the Shioaji futures Tick feed. All seven configured stocks are
covered. The shared SDK session subscribes once, waits a bounded window, unsubscribes
all successful subscriptions and logs out. It does not poll snapshots or place orders.
Indicative `simtrade` ticks are excluded. A fresh snapshot is a request observation
(`is_live: false`), distinct from an actually received fresh Tick (`is_live: true`).

MIS observations, primary/fallback statuses and the selected source remain in
`source_observations` / `quote_selection`. Shioaji Tick OHLC and volume come from the
same event; other providers' fields are not merged into it. Snapshot OHLC comes from
the same Shioaji snapshot. Daily FinMind bars, institutional data and margin are not
replaced by intraday observations.

`Morning Night Intraday Acceptance Experiment` can be run manually. It sequentially
runs three scenarios to avoid unnecessary concurrent broker sessions:

- `morning`: prior available trading-date OHLCV / institutional / margin report;
- `evening`: current-date completed daily data, with missing/previous-date data
  explicitly withheld from current-session values;
- `intraday`: Shioaji-first selected stock observations and TX Tick, timestamp
  freshness and source diagnostics.

Each scenario collects actual current data and uploads raw observations plus
`report-{scenario}.json` and `report-{scenario}.md` as an artifact. Run locally after
collecting the corresponding inputs:

```bash
REPORT_SLOT=morning python collect_market.py
REPORT_SLOT=morning python collect_cross_market.py
python collect_intraday.py
python report_scenarios.py --scenario morning --experiment
```

The experiment is a **current-time preview**, not proof of execution at 08:20/23:00,
not a point-in-time historical replay and not a delivery acknowledgment. Offline
08:20 and 23:00 regression fixtures separately verify date selection. During a
daytime evening preview, `SESSION_NOT_CLOSED` and a partial report are expected.
Actual missing data must not be replaced by yesterday's prices or institutional flows.
This report builder provides auditable data tables; news/forecast commentary and
scheduled message delivery remain separate work.

Official SDK behavior references:
- https://sinotrade.github.io/tutor/market_data/streaming/stocks/
- https://sinotrade.github.io/tutor/market_data/snapshot/
- https://sinotrade.github.io/tutor/limit/

Actual three-scenario outputs from the 2026-10-22 daytime acceptance run:
[morning preview](docs/experiments/2026-10-22-morning.md),
[evening preview](docs/experiments/2026-10-22-evening.md),
[immediate query](docs/experiments/2026-10-22-intraday.md).
The shared Taiwan watchlist lives in `instruments.py`.

## Current report contract (supersedes older timing/coverage notes above)

The enabled morning task is **08:50**, evening **23:00 Taipei**. Six report instruments
are mandatory (0050/006208/00631L/2330/3707/5483); three optional observations remain.
A stock subset being complete no longer marks a complete report. Missing market context,
actual TOPIX, stale quotes, wrong sessions or cutoff violations remain explicit blockers.

Production preparation publishes `reports/YYYY-MM-DD/{morning,evening}.json` with small,
public-data-only facts, input SHA-256 fingerprints and section-level `DATA_READY` /
`DATA_PARTIAL`. Ledger persistence, task execution and user delivery remain independent.
See [report contract](docs/REPORT_CONTRACT.md) for the definitive requirements, preparation
crons, deadlines, source semantics and validation procedure.
