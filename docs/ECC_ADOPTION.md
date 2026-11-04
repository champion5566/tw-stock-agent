# ECC adoption and maintenance decisions

Upstream: https://github.com/affaan-m/ECC
Reviewed revision: `b38be6a7f6350964d59328b52f0624e1d1d552d1`.
License: MIT, copyright 2026 Affaan Mustafa; notice retained in `ECC_LICENSE.txt`.

This project adapts four engineering workflows, rather than installing the entire
runtime/plugin or copying its agent catalog. Upstream instructions are reference
material; project code and acceptance requirements govern actual execution.

| Upstream workflow | Project implementation | Acceptance evidence |
|---|---|---|
| skills/search-first/SKILL.md | AGENTS research-first rule; existing providers/calendars and GitHub push events reused | PR records existing implementation and narrow change |
| skills/automation-audit-ops/SKILL.md | Independent execution/data/publication/ledger/delivery states; operations inventory | Actual task, Actions and artifact inspections |
| skills/verification-loop/SKILL.md | scripts/verify.sh, Quality Gate, live source run and exact readback | Local/CI/target evidence reported separately |
| skills/eval-harness/SKILL.md | Regression fixtures for cutoff leakage, late retries, night reuse, request validation, report profile | Full existing suite plus failure-specific regressions |

## Reuse decisions

- Keep yfinance, FinMind, Shioaji, exchange_calendars and existing Git publisher.
- Use native GitHub push triggers plus connector create-file because this connected
  tool surface lacks workflow-dispatch. No new scheduler hosting or API credentials.
- Extend the existing report contract and publisher rather than add another schema
  framework, agent framework or database for this small deterministic requirement.
- Keep annual research behind the existing full collection profile; report profile
  does only required short history and cross-market observations.
- Defer global plugin installation, self-learning hooks and additional MCP servers:
  their execution/lifecycle support is not established in ChatGPT scheduled tasks.

## Failure-specific evals

Before acceptance, ensure after-cutoff Asia bars cannot qualify; collection completion
cannot be hidden behind an earlier start; morning before 08:20 is rejected; timely
packages survive late retries; pre-push delay disqualifies timing; night source clocks
survive reuse; annual history is absent in report mode; concurrent publishers preserve
all independent files. DATA_PARTIAL from genuinely missing sources is not a test failure
and is never converted into invented completeness.

Baseline: 52 offline tests passed before modification. Upgrade verification and actual
run/readback evidence are recorded in `docs/UPGRADE_ACCEPTANCE.md` after execution.

This integration provides reusable project rules, deterministic controls and handoff
records. It does not claim automatic hook execution, autonomous model learning,
guaranteed scheduler punctuality or improved market prediction accuracy.
