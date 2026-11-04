# Project operating rules

This repository collects public market observations. Broker access is quote-only.

1. Read `docs/REPORT_CONTRACT.md` and `docs/OPERATIONS.md` before changes. `report_contract.py` owns executable timing and data checks: Taipei 08:38 cutoff/08:40 morning; 22:58 cutoff/23:00 evening. Morning collection never starts before 08:20.
2. Follow `docs/PROVIDER_POLICY.md` for every unresolved source/operational gap. Search existing modules, maintained packages, community implementations and official APIs before writing new infrastructure. Try and verify suitable independent alternatives; record failures, chosen source, fallback and target acceptance instead of leaving a primary-source failure as a permanent MISSING item. Record the selected solution and evidence in the PR. Keep required datasets and original prediction text intact.
3. Distinguish configuration, task start, collection, data validation, publication/readback, prediction-ledger persistence and user delivery. A green workflow establishes only executed steps. Local checks do not certify live providers or future schedules.
4. Never replace missing values with previous prices, use an ETF as the actual TOPIX index, mix source clocks/OHLC, or use after-cutoff observations as original pre-open inputs. Delayed reports remain visible and unscored as appropriate.
5. Public GitHub files contain public observations and non-personal predictions only. No position sizes, costs, account data, secrets or conversation transcripts. `preparation/requests` contains only schema, slot and timestamp.
6. Preserve existing prediction ledgers. Never reconstruct missing historical originals or bypass a blocked write. Reporting tasks create new ledgers only and verify exact text by readback.
7. Run `bash scripts/verify.sh` for meaningful code changes. Add regression cases for the actual failure. Before merging inspect the diff and actual CI result; after merging inspect actual source execution and reread published artifacts.
8. For work handoff record revision, checks run, actual run/artifact links, unresolved failures and next action. Keep scheduled acceptance separate from current-time preview. Platform delivery acknowledgment remains UNKNOWN without independent evidence.

Workflow references and upstream revision: `docs/ECC_ADOPTION.md`. No runtime plugin or self-learning hook installation is implied by these project rules.
