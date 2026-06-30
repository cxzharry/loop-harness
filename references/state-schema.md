# State Schema

Use these artifacts for persistent product optimization loops.

## PRODUCT_LOOP.md

Purpose:
- Product surface and optimization goal.
- Detected intent and any user-confirmed metric/target/risk decisions.
- Pattern id from `product-loop-patterns.json` when using a reusable loop.
- Profiles enabled.
- Cadence and rollout level.
- Execution mode and run-until-done limits when applicable.
- Human gates and denylist.
- Verification commands and data sources.
- Playwright command/route expectations when app verification is required.
- Execution strategy: single-agent, sequential-agents, or parallel-agents.
- Agent handoff and worktree-map pointers when actioning work may be split.
- Run-until-done target, target minimum, safety budget, plateau patience, and stop conditions.
- Budget and kill switch pointer.

## PRODUCT_LOOP_STATE.md

Required sections:
- Last run.
- Active opportunity.
- Execution mode, current iteration, target, latest verdict, and stop condition.
- Primary metric, baseline window, and user confirmations when metric-based.
- Candidate backlog.
- Watch list.
- Failed attempts and do-not-retry notes.
- Active benchmark regressions that currently block forward optimization.
- Execution orchestration: parallel domains, agent task ids, worktree strategy, integration owner, conflict review, integrated verification.
- Human decisions.
- User confirmations.
- Data gaps and instrumentation needs.
- Next scheduled action.

## product-loop-run-log.md

Append-only. Each entry includes:
- Timestamp.
- Profile.
- Discovery signals.
- Selected intervention.
- Verification evidence.
- Playwright URL, viewport, flow steps, assertions, screenshots/traces when app verification was needed.
- Verdict.
- Files changed or no-change reason.
- Next scheduling decision.
- Iteration state for run-until-done loops.
- Promotion notes: what moved into state and benchmark.
- Agent task ids, worktree map, conflict review, and integration verification when parallel agents are used.

## PRODUCT_LOOP_BENCHMARK.md

Promoted from stable run-log evidence. It should include:
- Known-good product flows and Playwright steps.
- Recurring smoke assertions.
- Baseline metrics or accepted proxy evidence.
- Do-not-regress rules.
- Historical failures that should become regression checks.
- Last promoted run-log entry.
- Regression cases with source run-log entry, error class, trigger, matching rule, owner profile, last failed, last passed, and active/retired status.

## product-loop-budget.md

Required fields:
- Max runs per day/week.
- Optional max iterations per opportunity when the user requests a hard cap.
- Default plateau patience.
- Max actioning changes per run.
- Max subagent/tool-heavy checks per run.
- Token or time budget.
- Kill switch.
- Escalation owner or inbox.

## AGENT_HANDOFF.md

Required when a loop dispatches multiple agents or needs durable handoff across agents:
- Run id and loop iteration.
- Execution strategy.
- Integration owner.
- Shared constraints and denylist.
- Benchmark cases that must pass before acceptance.
- One task entry per agent with domain, scope, goal, allowed files/surfaces, forbidden files/surfaces, required context, verification command, expected output, worktree, and status.
- Agent results: summary, root cause or hypothesis, files changed, verification evidence, risks, follow-up.
- Integration record: conflict review, integrated files, integration verification, benchmark verdict, final decision.

## worktree-map.md

Required when a loop creates or reuses isolated worktrees:
- Repo root.
- Existing linked-worktree detection.
- Submodule check.
- Native worktree tool or git fallback used.
- Project-local worktree ignore verification.
- Task id to branch/path/agent/status/verification/integration decision mapping.
- Cleanup decision for merged, removed, retained, or blocked worktrees.
