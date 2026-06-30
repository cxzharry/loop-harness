# State Schema

Use these artifacts for persistent product optimization loops.

## PRODUCT_LOOP.md

Purpose:
- Product surface and optimization goal.
- Pattern id from `product-loop-patterns.json` when using a reusable loop.
- Profiles enabled.
- Cadence and rollout level.
- Human gates and denylist.
- Verification commands and data sources.
- Budget and kill switch pointer.

## PRODUCT_LOOP_STATE.md

Required sections:
- Last run.
- Active opportunity.
- Candidate backlog.
- Watch list.
- Failed attempts and do-not-retry notes.
- Human decisions.
- Data gaps and instrumentation needs.
- Next scheduled action.

## product-loop-run-log.md

Append-only. Each entry includes:
- Timestamp.
- Profile.
- Discovery signals.
- Selected intervention.
- Verification evidence.
- Verdict.
- Files changed or no-change reason.
- Next scheduling decision.

## product-loop-budget.md

Required fields:
- Max runs per day/week.
- Max actioning changes per run.
- Max subagent/tool-heavy checks per run.
- Token or time budget.
- Kill switch.
- Escalation owner or inbox.
