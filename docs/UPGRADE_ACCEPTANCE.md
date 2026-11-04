# Upgrade acceptance — 2026-11-04

## Implemented

- [PR #32](https://github.com/champion5566/tw-stock-agent/pull/32), merged as `4ff42de76711c80be8b396291dbec835da26373f`: aligned 08:38/08:40 morning timing, lightweight report profile, native request-file push preparation, completed-night reuse, late-retry protection, pinned ECC workflow adoption and operations/handoff rules.
- [PR #33](https://github.com/champion5566/tw-stock-agent/pull/33), merged as `e30c6105e6c5b8fa42a0f042020400b6ce8faff2`: live-preview diagnostic regression; after-cutoff evening observations are distinguished from future provider clocks.
- Existing morning/night/weekly ChatGPT tasks updated and read back. Morning remains 08:40, night 23:00, weekly Sunday 19:00. Active weekday preparation tasks are 08:20 and 22:50 starting 2026-11-05, with native cron backups retained.
- Platform limit is five active tasks. Subsequent target-time acceptance is integrated into preparation tasks (submit first, then audit prior report) and the existing weekly report, rather than adding another task. No new account, paid service, credentials or runtime plugin is required.

## Executed checks

| Check | Result | Evidence |
|---|---|---|
| Baseline offline suite | PASS, 52 tests | Before changes, 2026-11-04 |
| Upgrade offline suite | PASS, 61 tests | Full suite, compilation, shell syntax, whitespace checks |
| PR #32 CI | PASS | [41853260573](https://github.com/champion5566/tw-stock-agent/actions/runs/41853260573) |
| PR #33 CI | PASS | [41854043373](https://github.com/champion5566/tw-stock-agent/actions/runs/41854043373) |
| Merged-code live source/publish preview | PASS for executed steps | [41853406444](https://github.com/champion5566/tw-stock-agent/actions/runs/41853406444) |
| Request commit and exact readback | PASS | [68d6843](https://github.com/champion5566/tw-stock-agent/commit/68d6843addf3a2b16705146a8110a7ecf017b5ae) |
| Request-triggered live source/publish | PASS for executed steps | [41853621340](https://github.com/champion5566/tw-stock-agent/actions/runs/41853621340) |
| Request-run bundle exact-revision readback | PASS | [published bundle](https://github.com/champion5566/tw-stock-agent/blob/28a722993848a05070d0dc8344c97c4795293a62/reports/2026-11-04/evening.json) |

The request was created at 23:02:28 Taipei, workflow resolved preparation at 23:03:43,
and generated the bundle at 23:05:21. It was deliberately a current-time acceptance
check after cutoff, **not** the scheduled 22:50 preparation or an on-time 23:00 report.
The data-report ID references run 41853621340 and the exact request commit.

Six required stock datasets passed the source/field checks in the live preview. US
observations were retrieved. The whole report correctly remained DATA_PARTIAL: market
context was not collected, and after-cutoff observations/generation cannot qualify the
intended report. A successful quote step is not evidence of valid target-time freshness.

## Independent acceptance and remaining work

- Code/CI: verified as above.
- Actual request -> collection -> publication -> exact readback: verified as above.
- Full required data coverage: PARTIAL. Actual TOPIX, market context and provider
  completed-session gaps retain their original requirements and explicit statuses.
- First future 08:20/22:50 preparation and 08:40/23:00 report punctuality: NOT YET VERIFIED.
- Prediction-ledger correctness and persistence: independently audited by reporting tasks;
  this upgrade does not rewrite historical ledgers or create replacement predictions.
- User notification receipt: UNKNOWN without an independent platform acknowledgment.

Data-package `publication_status=PENDING_PUSH_AND_READBACK` is the saved pre-push state;
the independent exact remote readback above establishes publication for that specific
revision. It is not a notification acknowledgment or proof of timely publication.
