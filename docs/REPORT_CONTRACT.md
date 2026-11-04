# Report contract v2

Executable authority: `report_contract.py`. All times are Asia/Taipei.

| Scenario | Collection window | Data cutoff | Report target |
|---|---|---|---|
| Morning | Never before 08:20 | 08:38 | 08:40 |
| Evening | Request at 22:50; native backup 22:52 | 22:58 | 23:00 |

Morning preparation requests are independent of GitHub cron; both are best effort.
Nightclose (05:35 Tue–Sat) stores historical night observations, not live morning ticks.
Native Taiwan background refresh remains 08:25/22:15. Weekly reporting stays Sunday 19:00.

## Required public data

- Six instruments: 0050, 006208, 00631L, 2330, 3707, 5483. Watch-only: 2313, 2367, 3491.
- Target completed XTAI session OHLCV, turnover TWD, previous close, amplitude,
  prior-5/prior-20-session volume ratios, institutional components/5-session flow,
  credit balances/daily and 5-session changes. Share and native-lot units are distinct.
- Market context: TAIEX/TPEX, breadth, aggregate institutions/margin, futures positioning.
- Morning: nine completed US regular-session daily bars, eight JP/KR observations
  including actual TOPIX (regional portal sources), and completed-night TX observation near actual 05:00 end.
- Evening: nine US observations (>15m DELAYED, >30m STALE) and TX Tick within 10m
  of the 23:00 target. Age must also be reassessed at actual completion.
- ETF proxies cannot satisfy actual indices. Daily bars, snapshots and ticks remain
  distinct. A valid previous completed session is expected historical morning data.

`scenario-report-v2` remains the outer schema; `readiness.version=report-contract-v2`
adds the corrected times and stricter cutoff/collection-window checks. Legacy v1
packages remain readable historical evidence, not silently revalidated current packages.
`stock_data_status=COMPLETE` describes only stock data. `DATA_READY` requires every
required section; unavailable sections stay visible as DATA_PARTIAL.

Asia sections accept calendar-confirmed MARKET_CLOSED as a non-trading-day state; carried prices are not fresh quotes. Provider timestamp/date inference must be explicitly recorded. Market context exposes source scope and separate TWSE/TPEx components. See PROVIDER_POLICY.md for active routes.

## Point-in-time and publication

Collection completion is distinct from collection start. Input completion, generation
and every morning Asia observation must be before the cutoff. Missing completion in
legacy inputs falls back to the recorded fetch time, but does not establish publication.
A source bar after cutoff is OBSERVATION_AFTER_CUTOFF, distinct from a provider clock
being ahead of actual wall time. Morning source collection before 08:20 is rejected.

Bundles contain fingerprints, original clocks, run/commit identity and independent states.
The publisher archives every candidate, records a pre-push check, and preserves a timely
report against late/weaker retries. Preview output never outranks a timely formal package.
Actual publication requires inspecting the GitHub file-changing commit and exact-revision
readback. A pre-push timestamp alone is insufficient. A successful push is not user delivery.

Reporting tasks must pin a data-branch revision before reading a report and verify its
file-changing commit is no later than cutoff. Original prediction text must exist before
09:00 to count as a morning prediction. Late/backfilled/unverifiable samples are excluded
from formal accuracy metrics. Missing evidence produces UNKNOWN/UNVERIFIABLE, never a
reconstructed result. Data packages keep `formal_sample_eligible=false` because they
cannot certify a separately created model prediction or ledger.

## Independent acceptance states

| State | Evidence required |
|---|---|
| Code | Offline verification and actual CI |
| Source execution | Run/commit, step outcomes and source clocks |
| Data | Per-section checks and exact input fingerprints |
| Publication | Successful push, file-changing commit before cutoff, exact readback |
| Ledger | New non-personal original text, successful create and exact readback |
| Report output | Platform scheduled/start/completion/result for the correct occurrence |
| Notification receipt | Independent platform acknowledgment; otherwise UNKNOWN |

No position size, cost, account or profit information belongs in public artifacts.
Historical ledgers are create-only, never rewritten or reconstructed. Existing report
sections, scoring weights and original prediction identifiers are preserved.

## Verification and open coverage

Run `bash scripts/verify.sh`, then inspect an actual live preparation run and published
bundle. A current-time preview does not certify future 08:40/23:00 execution. Regional actual TOPIX, market context and completed-session fallback routes are now connected; actual availability remains independently checked for each run. Exchange calendars do not certify unannounced closures.

Primary provider references remain exchange_calendars, yfinance regular-session history,
FinMind Taiwan chip datasets and the official Shioaji SDK documentation.
