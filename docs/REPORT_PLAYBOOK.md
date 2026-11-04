# Shared morning/evening research workflow

This is the canonical content playbook for both report tasks and the background teacher.
It supersedes earlier instructions to print A–L sections, repeat full ledger blocks in
the message, or generate a separate daily review report. Data coverage, cutoff checks,
original forecast IDs, scoring definitions and immutable ledgers remain unchanged.
The user's existing opening prediction/recap remains the first visible block.

## Division of work

- Existing collectors provide observations, clocks, provenance and readiness. Reuse their
  outputs; perform bounded targeted lookups only for important missing/conflicting inputs.
- Deterministic code handles calculations, unit conversions and supported outcome checks.
  Read evaluations/ledger-review-*.json before recomputing results with prose. No new agent,
  scheduler, database or paid data service is needed for the simplified flow.
- One research workflow runs at morning and evening, passing versioned state in the existing
  immutable prediction ledger. The model handles new evidence, economic transmission,
  competing explanations, expectations gaps and falsification.
- The teacher reviews in the background, batches corrections and checks adoption. Internal
  scores are diagnostics; neither score increases nor agent count establish trading value.
  User attention is reserved for material changes, completed useful fixes or a real decision.

## Compact visible report

Aim for 300–500 Chinese characters of analysis, plus at most six rows of instrument
summary and a concise source/exception footer. Important events can justify more.
1. Morning: retain opening center/delta/percent/range/confidence (or one compact N/A row
   with the specific reason). Evening: retain the original morning prediction and the
   actual result/error or a compact unscoreable statement. Don't repeat N/A across tables.
2. State at most three material changes since the previous report: evidence -> transmission
   -> affected exposures -> what would disprove it. Differentiate sourced fact, inference
   and hypothesis. If nothing material changed, say so rather than fill a template.
3. Prioritize one or two decision situations. A justified conditional action specifies a
   measurable trigger, timeframe, invalidation and implication. Do not invent arbitrary
   volume/time thresholds to populate a form. Evidence-supported waiting is acceptable.
4. Show concise six-instrument status; mention flow/ranking/catalysts/US holdings only where
   they change a decision. Required full OHLCV, metrics, institutional/credit fields and
   cross-market details remain available in the verified data package/appendix. Missing
   required data stays marked missing, not removed from coverage or claimed complete.
5. Provide parent/current ledger links, data revision and brief material exceptions. Full
   audit states and unchanged numbers appear once in the appendix or linked artifact,
   not repeatedly in the body. Never claim receipt without independent acknowledgment.

## Shared research state without another database

Append one [RESEARCH_STATE] JSON block to each *new* prediction ledger alongside the
required [PREDICTION_LEDGER] and [ROLLING_ERROR_LOG]. The previous opposite-slot ledger
is the parent; morning normally follows the latest completed evening, evening follows
today's morning. On closures, explicitly identify the last valid session and do not
create a fake open forecast.

State schema:
- version: research-state-v1; report_id; parent_report_id; updated_at_taipei.
- candidates: at most three entries with stable idea_id, claim, evidence (source + observed_at),
  status (WATCH / ACCEPT / REJECT), next_check, falsifier and change_reason.
- pending_checks: original prediction/action IDs still awaiting outcomes.
- corrections_applied: correction IDs and concrete adoption evidence.

Read the parent state first, update only for actual new evidence and preserve stable IDs.
If an old ledger lacks state, initialize from currently verified information and say
state_initialised_now; never fabricate historical continuity. Omit private holdings/costs.
This is one logical shared record with immutable per-report versions, not two independent
research lists or an additional mutable state file.

## Evidence and outcomes

Follow REPORT_CONTRACT.md and PROVIDER_POLICY.md: pin the data revision, distinguish
actual publication from collection time, respect 08:38/22:58 cutoffs and 08:40/23:00
targets. Supplemental late data must not qualify an original forecast. Missing inputs
cannot be invented. An experimental opening estimate needs an explicit reproducible
method and valid inputs; uncalibrated confidence is marked accordingly. The opening
experiment must not consume the entire research workflow.

Keep original ledgers create-only, exact-readback verified. Store complete prediction and
action rules with unique IDs and their ex-ante timing. Settling an individual valid item
does not require every unrelated dataset. PROVIDER_MATCHED is not OFFICIAL_DIRECT or
formal forecast eligibility. Unsupported/conditional rules remain for manual review,
not partial-rule parsing. No inferred precision, made-up costs, sample counts or causal
attribution. Original prediction scoring and report-quality scoring remain separate.

## Simplification acceptance

Replay the same historical inputs, retaining original N/A and source limitations; label
the compact rewrite retrospective, never a new scored historical forecast. Compare
decision-relevant coverage, unsupported claims, repeated content and reading cost.
A shorter rewrite proves only presentation changes. Judge research utility over subsequent
comparable reports and settled decisions. Maintained full-stack tools such as
ZhuLinsen/daily_stock_analysis are candidates for a controlled comparison, not installed
or assumed to satisfy Taiwan market coverage, live data or alpha requirements.
