# State Schema

Use these artifacts for persistent product optimization loops.

## Artifact Root

In target repos, put loop artifacts in `.loop-harness/` by default:

```text
.loop-harness/
  PRODUCT_LOOP.md
  PRODUCT_LOOP_STATE.md
  product-loop-run-log.md
  PRODUCT_LOOP_BENCHMARK.md
  product-loop-budget.md
  AGENT_HANDOFF.md
  worktree-map.md
  agent-tasks/
```

Use another folder only when the user explicitly requests it or the repo already has an established loop artifact root. The loop-harness skill's own self-development artifacts use `self/loop-runs/` as an internal exception.

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
- Selected global/local criteria and benchmark seeds, when `select_knowledge.py` is used.
- Next scheduled action.

## product-loop-run-log.md

Append-only. This is the only file for raw run errors and findings; do not create separate error-log or findings files.

Each entry includes:
- Timestamp.
- Raw Run Result: profile, discovery signals, selected intervention, verification evidence, Playwright URL/viewport/flow/assertions/screenshots/traces, error output, failed assertions, verdict, files changed or no-change reason, next scheduling decision, and iteration state.
- Finding: finding id, error class, symptom, evidence, root cause/hypothesis, reproduction steps, severity, confidence, and status.
- Benchmark Promotion: promotion decision, benchmark case id, matching rule, expected result, verification command, status, and what moved into state/benchmark.
- Agent task ids, worktree map, conflict review, and integration verification when parallel agents are used.

Use `Finding Status: not_applicable` and `Error class: none` for clean passing iterations. Use `Promotion decision: not_promoted` when a failure is noise, one-off, already covered, or not reproducible enough to become a benchmark.

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
