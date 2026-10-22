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
- The three snapshot writers use a **shared concurrency group** and publisher script to prevent collisions.

## Verify
```bash
python -m compileall -q .
python -m unittest discover -s tests -p 'test_quote_quality.py' -v
bash -n scripts/publish_snapshots.sh
```

See [architecture audit](docs/ARCHITECTURE_AUDIT.md) for known issues, migration stages and operational risks.

## Scope note
The older `stock-test`, `mcp-smoke`, `ieobserve-*` and Fugle workflows are experimental probes, **not** report delivery. Do not treat their red CI state as proof of core quote-feed failure.
