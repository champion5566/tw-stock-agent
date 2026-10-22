# Report data readiness and timing contract

The connected enabled ChatGPT tasks currently target **08:50** and **23:00 Asia/Taipei**.
The old 08:20 task is disabled. Do not infer active delivery settings from older README
text or change delivery times without checking the actual tasks.

## Roles and required data

- Required report instruments: **0050, 006208, 00631L, 2330, 3707, 5483**.
- Optional observations: **2313, 2367, 3491**. An observation is not a claim of ownership.
- No private position size, cost, account or profit information is part of repository artifacts.

`stock_data_status` describes only the historical stock subset. Overall data readiness
is `DATA_READY` only when **all** required sections pass; otherwise `DATA_PARTIAL`.
It never certifies the prediction ledger, analysis quality, message publication or receipt.

| Section | Morning | Evening |
|---|---|---|
| Six stocks | Previous completed XTAI session | Latest completed XTAI session by report target |
| Daily fields | Previous close, OHLC, shares, turnover TWD, amplitude, prior-5/prior-20-session volume ratios | Same |
| Institutional | Foreign investor + foreign dealer-self, trust, dealer components, total and 5-session net shares | Same |
| Credit | Margin/short balance, daily change and 5-session change in provider-native units | Same |
| Market context | TAIEX/TPEX, breadth, aggregate institutions/margin and futures positioning for target session | Same |
| US | Nine completed regular-session daily bars, separately from extended-hours last bars | Nine observations evaluated at 23:00; >15m delayed, >30m stale |
| Japan/Korea | Eight opening observations, evaluated at 08:50; actual TOPIX required | Optional historical context |
| TX | Last broker observation within 10 minutes of the completed night end, explicitly non-live | Actual Tick within 10 minutes of 23:00 |

TOPIX ETF remains an optional proxy. It cannot satisfy the actual TOPIX requirement.
Market context fields not yet collected are explicit blockers. The contract must expose
these gaps rather than lower requirements until current sources happen to pass.

Daily dates use the maintained `exchange_calendars` XTAI/XNYS calendars, including
weekends, holidays and DST. Calendar expectations do not override actual source dates
or certify unannounced closures. Older source rows cannot redefine the expected session.

Completed US daily bars use yfinance `interval=1d`, `prepost=False`, and only the expected
completed XNYS session. They are provider regular-session daily bars, **not** certified
exchange settlement files. Broker TX snapshots are also not exchange settlement files.
TX night-session validation keeps actual Taiwan timestamps; no automatic conversion of
a trading-date label into an invented final trade timestamp is performed.

FinMind institutional column semantics follow its official wide-dataset documentation:
modern listed/OTC Dealer is split into Dealer_self + Dealer_Hedging, with Dealer aggregate
zero in those rows. Components are used once; a nonzero conflicting aggregate is flagged.
Foreign dealer-self is a real separate category and is included once in foreign totals.

## Preparation and delivery

| Stage | Taipei time | UTC cron | Deadline |
|---|---|---|---|
| Taiwan morning snapshot | 08:25 weekdays | `25 0 * * 1-5` | Morning artifact before 08:45 |
| Cross-market morning + data report | 08:38 weekdays | `38 0 * * 1-5` | 08:45 |
| ChatGPT morning | **08:50** daily | Managed by existing task | Record actual completion; no automatic delivery acknowledgment |
| Taiwan evening refresh | 22:15 weekdays | `15 14 * * 1-5` | Evening artifact before 22:58 |
| Cross-market evening + fresh TX + data report | 22:52 weekdays | `52 14 * * 1-5` | 22:58 |
| ChatGPT evening | **23:00** daily | Managed by existing task | Record actual completion; no automatic delivery acknowledgment |
| Post-night observation | 05:35 Tue-Sat | `35 21 * * 1-5` | Stored as historical session observation |

GitHub and ChatGPT schedules are best effort. Late collection/generation is flagged;
it must not silently pass the cutoff check. Quotes are tested for age **at delivery
target**, not just at their earlier capture time. On closed markets or missing feeds,
the user still receives a visible status report rather than silence.

The post-night and morning paths request a single futures snapshot without subscribing
or waiting for a Tick outside the session. The evening path subscribes for a bounded
window. A day-session or pre-open timestamp cannot satisfy the night-last-observation gate.

## Consumer artifact and independent evidence

Cross-market preparation reads the already-published Taiwan input using a pinned
`data/snapshots` checkout and publishes small public-data-only consumer artifacts:

- `reports/YYYY-MM-DD/morning.json`
- `reports/YYYY-MM-DD/evening.json`

Each has the exact input SHA-256 fingerprints, generation time, target session,
cutoff, per-section failures and deterministic features. Raw source histories remain
in the original snapshot paths. The large raw files are not required for routine
report generation when the consumer artifact exists.

The following are independent states:

1. `data_readiness`: `DATA_READY` / `DATA_PARTIAL`.
2. `parent_ledger_status`: `NOT_CHECKED` until the reporting task reads original text.
3. New prediction-ledger persistence: only VERIFIED after actual write + readback.
4. Report task execution: platform scheduled/start/completion and recorded output.
5. User delivery: `NOT_ACKNOWLEDGED` / platform unknown until independent acknowledgment.

A task record with visible content is evidence of generated output; it is not proof
that a push notification reached a device or was opened. Previous blocked ledger writes
are not bypassed or reconstructed as successful. Old original text and IDs remain intact.

## Verification

Run `python -m unittest discover -s tests -v`. Tests cover unchanged existing behavior,
calendar/DST, actual six-instrument requirements, missing/invalid fields, source priority,
5-session calculations, source units, old/future/late inputs, TOPIX proxy rejection,
regular-session vs ongoing/extended-hours bars, night end vs current ticks, broker
cleanup, real backtesting and concurrent Git publishing. Actual provider runs and
future delivery observation remain separate evidence.

Primary references:
- https://github.com/gerrymanoim/exchange_calendars
- https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html
- https://finmind.github.io/tutor/TaiwanMarket/Chip/
