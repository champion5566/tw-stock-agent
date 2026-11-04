# Source repair acceptance — 2026-11-04

## Implemented source repairs

Regional primary/fallback selection is in `regional_quotes.py`; market-wide official and
existing-provider adapters are in `market_context.py`. The active decisions, references
and boundaries are in `PROVIDER_POLICY.md`. Both scheduled collection workflows enrich
the same existing snapshots; the small report bundle includes actual normalized values
and source/time provenance, not only missing-item flags.

## Executed local target probes

| Need | Executed evidence | Result |
|---|---|---|
| Korean indexes | Naver domestic batch KOSPI/KOSDAQ/KPI200 | Values, explicit localTradedAt and market state retrieved |
| Samsung/SK Hynix | Naver domestic stock batch | Both observations and original provider times retrieved |
| Actual TOPIX/Nikkei | Naver world `.TOPX`/`.N225` + Yahoo Japan | Actual indices retrieved; date-only JP displays are not given invented clocks |
| Japanese semiconductor stocks | Yahoo Japan nested stock boards + Naver 6857.T/8035.T | Real provider schemas inspected; independent timestamped fallback retrieved |
| TAIEX OHLCV | TWSE current-month endpoint was behind; FinMind TAIEX target-date row | Exact 2026-11-04 row retrieved |
| TPEX OHLCV | TPEx index and daily trading totals | Same source date and expected fields verified |
| Breadth | TWSE stock-only table; TPEx four-digit stock table | TWSE 438 advances/544 declines; TPEx 397/416 with 12 not-comparable changes |
| Institutional totals | TWSE BFI82U + TPEx summary | Both 2026-11-04, official component sums checked, combined scope exposed |
| Credit | TWSE totals + separate TPEx row aggregation | Native units preserved; TPEx current margin balance 2250593/change -18713 |
| Foreign TX position | Latest API was 2026-11-03; dated official POST CSV | Exact 2026-11-04 foreign net OI -93647 contracts retrieved |
| Independent TX backup | FinMind TaiwanFuturesInstitutionalInvestors | Actual schema uses futures_id; exact date and long/short balances retrieved |
| US completed daily close | Yahoo completed-session reader; independent FinMind USStockPrice | 2026-11-03 NVDA close 206.69 retrieved; uppercase Close supported |
| Current ticker identity | SEC company_tickers.json | Current SPCX issuer record retrieved; historical-position mapping remains unverified |

An initial official dated-CSV request timed out; the bounded read timeout/retry was adjusted
and the dated CSV then succeeded. The independent FinMind backup was also actually queried.
This is an example of the required search -> real request -> diagnose -> alternate source
process, not a policy that treats the first timeout as a permanent missing dataset.

These probes ran after the Asian session had closed. Asia observations correctly remain
STALE/NO_TIMESTAMP for live-morning purposes. Retrieval and parser acceptance do not certify
future 08:38 availability. No previous forecast or ledger was changed.

## Verification and rollout

Baseline before these changes: 61 tests. The new suite exercises source identity, Naver
explicit clocks, Japan's distinct index/equity boards, HTTP-Date inference, date-only
rejection, holiday calendars, whole-source fallback, exact US symbol/date, official named
columns and units, both futures schemas, two-market totals and derived-scope counts.

Run `bash scripts/verify.sh`. PR CI, post-merge source execution, exact published readback
and scheduled-time observations are independent acceptance stages. Actual rollout evidence
is appended after those executions; no green CI result substitutes for source availability.

## Deployed acceptance

- Merged [PR #34](https://github.com/champion5566/tw-stock-agent/pull/34), code revision `8e276d3072335246430f9416d193fa46f660eba3`.
- Full offline suite: **81 tests PASS**, compilation, shell syntax and diff checks pass.
- PR CI: [41859557223](https://github.com/champion5566/tw-stock-agent/actions/runs/41859557223), PASS; merged-code Quality Gate also passed.
- Actual merged-code source/generation/publication run: [41859790574](https://github.com/champion5566/tw-stock-agent/actions/runs/41859790574), PASS.
- Exact remote [report readback](https://github.com/champion5566/tw-stock-agent/blob/f3338d6e88716382b9eb5584247488eb2aea7b64/2026-11-04/report-evening.json), data-report ID `DATA-2026-11-04-evening-41859790574`, generation 23:40:32 Taipei.
- Six required stocks: PASS. All six required market-context items (TAIEX, TPEX, breadth, combined institutional totals, margin totals, foreign TX positioning): **PASS**, each actual source date 2026-11-04.
- Nine regional observations, including actual TOPIX, were present with provider timestamps. Closed-market observations correctly remained STALE for live purposes.
- Overall DATA_PARTIAL/CURRENT_TIME_PREVIEW is expected after the 22:58 cutoff; this is not a retroactive 23:00 report or proof of tomorrow's morning freshness.
- All five active reporting/preparation task prompts were updated and independently read back with the provider-selection policy. Existing delivery times remain unchanged.

The remaining platform-receipt, actual future timing, historical-position mapping and
forecast-calibration boundaries are recorded in PROVIDER_POLICY.md. They are not silently
reclassified as resolved quote-source gaps.
