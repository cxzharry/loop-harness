# State Schema

Use these artifacts for persistent product optimization loops.

## Artifact Root

In target repos, put loop artifacts in `.loop-harness/` by default:

```text
.loop-harness/
  PRODUCT_LOOP.md
  PRODUCT_LOOP_STATE.md
  criteria/
    current.md
  product-loop-run-log.md
  PRODUCT_LOOP_BENCHMARK.md
  benchmarks/
    active/
    archive/
  runs/
    archive/
  schedules/
  product-loop-budget.md
  AGENT_HANDOFF.md
  worktree-map.md
  agent-tasks/
```

Use another folder only when the user explicitly requests it or the repo already has an established loop artifact root. The loop-harness skill's own self-development artifacts may use ignored local `self/loop-runs/` as an internal exception, but that folder is not part of the public skill package.

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
- Evaluation contract pointer: `criteria/current.md`.
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
- Evaluation contract pointer and status.
- Candidate backlog.
- Watch list.
- Failed attempts and do-not-retry notes.
- Active benchmark regressions that currently block forward optimization.
- Execution orchestration: parallel domains, agent task ids, worktree strategy, integration owner, conflict review, integrated verification.
- Planned execution batch: batch type, lane ids, lane dependencies, parallelization rationale, integration plan, and deferred-lane rationale if any.
- Human decisions.
- User confirmations.
- Data gaps and instrumentation needs.
- Selected global/local criteria and benchmark seeds, when `select_knowledge.py` is used.
- Watchdog scheduler status, schedule id, last tick, lock owner, and log path when scheduled.
- Next scheduled action.

## criteria/current.md

Runtime criteria are repo-local, not skill-package benchmark criteria. This file is the locked evaluation contract for the current loop:
- Product surface, user flow, intent, and profiles.
- Primary metric or acceptance rubric.
- Baseline window, target, target minimum, direction, source, and sample/window caveat.
- Acceptance criteria, evidence required, pass thresholds, and non-applicability rules.
- Benchmark seeds with matching rule, expected result, verification command, and activation rule.
- Playwright route/URL, viewports, flow steps, assertions, and screenshot/trace expectation when app verification is relevant.
- User confirmations, human gates, non-goals, and last reviewed timestamp.

If this file is missing, incomplete, or not `Contract status: locked`, the next loop should run report-only/evaluation-contract bootstrap before actioning.

## product-loop-run-log.md

Append-only for recent entries. This is the only current file for raw run errors and findings; do not create separate error-log or findings files. When it grows large, keep recent entries and archive pointers here, then move detailed historical entries under `runs/archive/YYYY-MM.md` or `runs/archive/<timestamp>.md`.

Each entry includes:
- Timestamp.
- Raw Run Result: profile, discovery signals, selected intervention, verification evidence, Playwright URL/viewport/flow/assertions/screenshots/traces, error output, failed assertions, verdict, files changed or no-change reason, next scheduling decision, and iteration state.
- Finding: finding id, error class, symptom, evidence, root cause/hypothesis, reproduction steps, severity, confidence, and status.
- Benchmark Promotion: promotion decision, benchmark case id, matching rule, expected result, verification command, status, and what moved into state/benchmark.
- Agent task ids, worktree map, conflict review, and integration verification when parallel agents are used.
- Batch type, lane ids, parallelization rationale, and deferred-lane rationale when more than one lane is known.

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

Keep `PRODUCT_LOOP_BENCHMARK.md` as a compact active index when benchmark volume grows. Put large active cases in `benchmarks/active/<case-id>.md` and retired or old cases in `benchmarks/archive/<case-id>.md`. Selectors must read both the compact index and active split files.

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

## schedules/

Required for watchdog scheduler runs:
- Status file with schedule id, cadence, command, repo root, mode, pause state, last tick, next tick, and last verdict.
- Tick logs under `.loop-harness/schedules/` for scheduler stdout/stderr and loop report pointers.
- Lock file that records owner, pid, started timestamp, and current command to prevent overlapping ticks.
- Pause marker used by `watchdog.py pause` and cleared by `watchdog.py resume`.

Watchdog commands are `setup`, `status`, `pause`, `resume`, `tail`, `uninstall`, and `tick`. Scheduled ticks start as fresh processes and continue from `.loop-harness/*` state plus `criteria/current.md`.

## AGENT_HANDOFF.md

Required when a loop dispatches multiple agents or needs durable handoff across agents:
- Run id and loop iteration.
- Execution strategy.
- Integration owner.
- Shared constraints and denylist.
- Benchmark cases that must pass before acceptance.
- One task entry per agent with domain, scope, goal, allowed files/surfaces, forbidden files/surfaces, required context, verification command, expected output, worktree, and status.
- For multi-lane batches, one task entry per lane even if executed by the same local controller.
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
