# Repair state — public engineering evidence only

This is a small, resumable issue register for the existing 19:00 teacher. Read it before starting new critique. No private report, portfolio, prompt, account, or conversation content. Never overwrite immutable prediction ledgers. A CI success is not production verification.

| ID | State | Verified evidence | Remaining acceptance / next action |
|---|---|---|---|
| ETF-1105 | WAITING_NEXT_REPORT | PR36 fixed detection; historical 006208 229.20 vs 228.55 and 00631L 31.23 vs 30.85 preserved as errata | Compare a fresh complete producer report's six displayed closes to same-session daily source; do not rewrite historical originals. |
| NIKKEI-FRESHNESS | OPEN | 08:12 observation is stale by 08:40; source is correctly labeled STALE | Diagnose regional provider selection and independent fallback; test fresh source during real morning window; never loosen freshness gate. |
| US-REGULAR-CLOSE | VERIFIED_FOR_TABLE_ADOPTION | PR38 deterministic dated previous/current US closes and returns; 11/12 morning report included table | Continue ordinary regression; do not reopen without contrary evidence. |
| DRAFT-CHECK | OPEN | PR39 checker handles 昨收 and fails on no table; producer reports still state NOT_EXECUTED | Determine whether private draft can be passed to checker in the execution environment. If not, do not claim automation; enforce deterministic bundle table and manual comparison. |
| EVENING-PUBLICATION-1116 | WAITING_NEXT_REPORT | 2026-11-16 evening.json absent in data/snapshots; PR40 merged as 45affb04396bedcbfdacdbfdad8cfb541724ff96; PR Quality Gate 44098878299 passed. Added prepublish existence and postpublish readback. | Identify root cause using actual Cross Market Source Verification job logs and artifacts; inspect next evening production run and data-branch file. This detection change alone is NOT a source fix. |

## Work protocol

Prioritize existing unresolved production faults over new editorial grading. For each issue retain: failure stage, exact reproducible evidence, source or maintained implementation considered, minimal patch, negative test, existing verify.sh result, PR and CI, merged SHA, post-merge published artifact and next comparable producer adoption. Advance OPEN -> APPLIED -> WAITING_NEXT_REPORT -> VERIFIED only on evidence; reopen on recurrence. Prefer a single high-impact fix per execution. Never backfill pre-cutoff qualification or replace original predictions. If a test cannot run, write the exact blocker and next executable step, not 'monitor'.

The GitHub workflows may automatically validate public artifacts; private model-written report drafts are not implicitly available to GitHub. Never equate pipeline green, publication, consumer adoption, and message delivery. The teacher keeps the existing 19:00 cadence; no extra scheduler or agent is implied.
