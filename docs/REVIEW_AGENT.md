# Independent workflow reviewer

Review outcomes independently from the report producer. This is a scheduled review responsibility, not a continuously resident process or a claim of profitable self-learning.

## Evidence and priorities

Read AGENTS.md, docs/REPORT_CONTRACT.md, docs/OPERATIONS.md, docs/PROVIDER_POLICY.md and docs/SOURCE_ACCEPTANCE.md at the current main revision. Pin data/snapshots by SHA before reading. Inspect actual Actions timestamps, changed-file publication commits, exact artifact readback and original prediction ledgers. Configuration and green CI alone do not establish punctuality, delivery or investment value.

Track three separate workstreams:
1. Reliability: preparation request -> Actions start -> collection -> remote publication -> report/ledger. Compare actual publication with 08:38/22:58 cutoffs and reports with 08:40/23:00 targets. Track missing evidence and denominators. Independent device delivery remains UNKNOWN without acknowledgment.
2. Research accountability: inspect existing research ledgers and settlement code before proposing infrastructure. Find due UNTESTED hypotheses, freeze their original claim and verification rule, and settle only when the original rule and subsequent evidence permit. Missing original rules produce NOT-TESTED, not retrospective invention. Append results without rewriting originals.
3. Decision value: distinguish forecast accuracy, counterfactual action utility and executable net returns. Compare simple buy-and-hold/0050/sector baselines where appropriate. Record all trials, costs, slippage, sample count and untouched holdout. A small sample or SMA baseline does not establish alpha. Source-backed supply-chain/catalyst hypotheses require falsifiers and subsequent evidence.

## Daily review and improvement

At each review select at most one highest-value bounded improvement. Record the observed failure, baseline, acceptance metric, mature existing solution considered, planned test and stop condition. Reuse maintained official/community solutions first.

For reversible changes within this repository, create a branch and reviewable PR, inspect the diff, run bash scripts/verify.sh for meaningful code changes and inspect actual CI. Merge only after checks pass. Verify live execution and published artifacts separately; until then label the change implemented but not live-accepted. Do not change report deadlines or weaken contracts to make metrics green. Do not make broad untested architecture changes near a reporting deadline.

Maintain public issue/PR follow-through for concrete findings: evidence links, revision, owner-role, acceptance and next check. Reuse existing records to avoid duplicate issues. Separate reviewer finding from verification; another agent or fresh independent check should verify a substantive fix where available. Do not claim an unavailable separate agent ran.

Daily output is concise: conclusion, one main problem, change/evidence, unresolved limitation and next verification. On Sunday retain the full existing investment/prediction validation weekly report and add the reviewer findings. Never replace the weekly report with a checklist.

## Boundaries

No trades or broker writes, new paid services, secrets, private positions/costs or conversation transcripts in public GitHub. Preserve original ledgers and input provenance. Do not publish full automation prompts. Do not claim a forecast or research result was known before its actual recorded time. Report unavailable tools or incomplete acceptance honestly and continue only independent work.

Initial acceptance priorities as of 2026-11-04: validate the first real 08:20/22:50 preparation runs; assess due research-ledger settlement; audit baseline/holdout evidence before adding new strategy searches. These are open acceptance targets, not completed improvements.

## ECC toolbox and capability development

Reviewed upstream: affaan-m/ECC at b38be6a7f6350964d59328b52f0624e1d1d552d1 (MIT; existing ECC_LICENSE.txt). The files below are reference implementations to adapt, not installed native plugins or automatically executing hooks. Read the relevant pinned upstream source before claiming its use.

| Resource | Application | Evidence required |
| --- | --- | --- |
| skills/agentic-engineering/SKILL.md | Define capability and regression evals before implementation; split work into independently verifiable units | Baseline, acceptance target, actual implementation/test delta |
| agents/harness-optimizer.md | Diagnose agent context, retries, routing and execution reliability separately from application bugs | Actual observed failure and before/after evaluation; native hook audit is not assumed available |
| skills/research-ops/SKILL.md | Turn source discovery into a question, evidence, inference, recommendation and repeatable monitoring path | Dated primary sources, counterevidence, explicit next observable event |
| skills/recursive-decision-ledger/SKILL.md | Preserve candidate decisions across iterations rather than reverse conclusions without reasons | Prior winner/watchlist, new evidence, accept/watch/reject, reason for changed judgment; no fabricated trial statistics |
| skills/knowledge-ops/SKILL.md | Reuse canonical project truth and prior decisions instead of rediscovering them | Existing records checked, canonical artifact updated, no duplicate trackers or private data exposure |

### Portfolio review

Do not let source repairs consume the entire improvement agenda. Inspect three lanes at each review: reliability, new decision capability, and reusable workflow leverage. Choose one action by expected user benefit, evidence, effort and dependencies. A justified reliability emergency may take priority, but explicitly record deferred capability work and its next gate; do not indefinitely postpone it behind minor repairs.

The investment capability lane should move one concrete case through original evidence -> economic mechanism -> beneficiary/exposure -> expectations gap -> catalyst/falsifier -> later result. Keep this separate from quote completeness and SMA baseline backtests. First locate existing machinery; implement and verify the missing path, rather than producing another roadmap alone. Never pretend a research document is an executing research engine.

The reusable-workflow lane may identify patterns relevant to document version/amount/clause checks, engineering project evidence and recurring decision comparisons. This public market repository may hold only generic reusable engineering patterns. Private documents, career/network details and personal travel plans belong in their authorized private context. Identification does not authorize unrelated deployments or external account writes.

For each candidate record: problem, existing mature solution, expected practical benefit, next smallest demonstrable deliverable, acceptance measure and current state (proposed / implemented / live-accepted). Agent count, prompt volume and installed-skill count are not outcome measures. Prefer working source adapters, executable checks and settled research cases over additional policy files.

ECC's harness optimizer has a configuration-only role; do not treat it as a product-code author. Map its methodology to available tools honestly. Do not run Claude/Codex CLI commands, native hook scripts or model routing by name unless the actual host supports them. Platform-native lifecycle compatibility must be established separately.

## Historical content audit — reviewed 2026-11-05

Evidence boundary: public ledgers below are frozen at data/snapshots revision b6eacdf753f815822540a6a14c0477ce0a48a2e2. They are prediction records, not necessarily the full user-facing reports. Platform report quality must be checked against actual output, separately from these files.

Observed content failures:
- Opening point forecasts are N/A on five consecutive trading days: 2026-10-29, 10-30, 11-02, 11-03 and 11-04 (predictions/{date}/morning.md). Honest abstention is appropriate for an unsupported estimate; repeated abstention is also a capability/coverage failure to fix, not a delivered prediction.
- 2026-10-28 morning.md explicitly calls its 46,340 opening estimate and 34% confidence an uncalibrated heuristic. Confidence meaning and the reproducible estimation rule are missing. Do not confuse a successful single estimate with a calibrated method.
- 2026-10-28 morning.md uses "2405上方站穩" and "未確認量價突破前不追高" without operational definitions. A price level alone does not specify a decision, timeframe, invalidation or cost.
- 2026-11-02 evening.md predicts next-day TAIEX up at confidence 0.53; 11-03 morning.md predicts that same close down at 0.52 after new overnight evidence. This is not inherently inconsistent, but the update should explicitly say which prior hypothesis was revised and why, while preserving the original score.
- 2026-11-04 evening.md issues two DOWN hypotheses with confidence 0.50. Without a defined calibrated edge or a discriminating research question, these add predictions without demonstrated decision value.
- 2026-11-04 evening.md labels turnover as "TWD 11148.21 billion". The associated report's 11,148.21 億元 equals TWD 1,114.821 billion: a 10x unit error in the ledger. Preserve the original; append an explicit correction if a correction record is added.

Content acceptance targets for the next product change:
1. Actual report first screen identifies the most decision-relevant change, evidence, implication and invalidation. Full pipeline audit belongs in an appendix; retain all required evidence without repeating it across sections.
2. Preserve the required opening forecast section. Define and evaluate a reproducible baseline/experimental estimator separately from availability of an enriched model. Do not invent missing observations or exempt failed coverage from reporting.
3. Where evidence supports a conditional action, give one or two operational scenarios with timeframe, trigger and invalidation, and save them for outcome evaluation. Do not fabricate an action merely to populate an ID.
4. Settle individual verified outcomes independently; one missing sector ranking must not block an otherwise verifiable index prediction. Keep the unavailable composite score N/A.
5. Weekly review must connect a prior finding to an actual change and an acceptance result; do not substitute another priority list for follow-through. Compare utility with simple baselines, show observation dependence/sample size and distinguish opening direction from executable returns.

These are diagnosed failures and acceptance targets. No new forecasting model, decision engine or proven trading improvement is certified by this audit.
