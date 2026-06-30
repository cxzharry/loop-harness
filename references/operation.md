# Operation Contract

Use this file for the full loop execution contract after `SKILL.md` triggers.

## Intent Detection And User Confirmation

State intent before choosing profiles or execution mode:

- `UX_OPTIMIZE`: improve a screen, flow, copy, accessibility, or product comprehension.
- `METRIC_OPTIMIZE`: improve activation, conversion, retention, completion, revenue, or funnel movement.
- `ENGINEERING_QUALITY`: fix bugs, performance, CI, reliability, or product-affecting technical quality.
- `RELEASE_READY`: prepare a changed product surface for deployment or release.
- `INSTRUMENT`: add or repair analytics/observability before claiming product improvement.
- `POST_LAUNCH_LEARN`: learn from shipped behavior, support, feedback, metrics, and errors.

Defaults:
- If the user asks to improve or optimize a product without a metric, use `UX_OPTIMIZE + ENGINEERING_QUALITY` in `run-until-done` when a target can be inferred; otherwise use `report-only` discovery to define the target.
- If the user names conversion, activation, retention, funnel, revenue, experiment, or metric, use `METRIC_OPTIMIZE`; require a metric decision before `run-until-done`.
- If metrics are desired but unavailable or untrusted, switch to `INSTRUMENT`.

Use `AskUserQuestion` only for decisions that cannot be safely inferred:
- Primary product surface or user flow.
- Primary metric when `METRIC_OPTIMIZE` or `run-until-done` depends on it.
- Target threshold.
- Human gate: pricing, payment, auth, permissions, secrets, destructive migration, legal/compliance, brand-sensitive copy, or major product direction.
- Scheduled/actioning loop approval when cost or risk is material.

Do not ask when a safe default exists. Record the assumption in `PRODUCT_LOOP_STATE.md` and continue.

## Start Of Run

1. Identify intent and product surface in one line.
2. Load existing artifacts if present: `PRODUCT_LOOP.md`, `PRODUCT_LOOP_STATE.md`, `product-loop-run-log.md`, `PRODUCT_LOOP_BENCHMARK.md`, and `product-loop-budget.md`.
3. Scaffold missing ongoing-loop artifacts from `assets/templates/`.
4. Select profiles using `references/profiles.md`.
5. Select a pattern using `references/patterns.md` and `assets/templates/product-loop-patterns.json` when cadence or recurring scope matters.
6. Ask only unresolved metric, target, risk, or schedule decisions.
7. Run `scripts/product_loop_audit.py <repo-or-folder> --min-level L2` after scaffolding or artifact changes.
8. Run `scripts/product_loop_cost.py --pattern <pattern-id> --level L1|L2|L3 --cadence <interval>` before scheduling recurring loops.

## Execution Modes

- `report-only`: discover, verify signals, persist state, and stop without source changes.
- `run-until-done`: repeat full five-phase iterations until a stop condition fires.
- `scheduled`: run on cadence; each tick may be report-only or run-until-done within budget.

There is no `action-once` mode. Any loop that changes files, product behavior, docs, metrics, or release state must use `run-until-done`, even when it stops after one successful iteration.

`run-until-done` requires a measurable target or locked rubric, safety budget or kill switch, `target_min`, stop conditions, plateau patience, and human gates written to state before actioning. For metric targets, confirm primary metric, baseline window, target threshold, and sample/window or proxy evidence.

## Five Phases

Every iteration must execute all five phases:

1. Discovery: refresh state, benchmark cases, previous failures, and current product signals.
2. Handoff: choose one bounded intervention and hypothesis; decide single-agent, sequential-agent, or parallel-agent execution and worktree isolation.
3. Verification: run matching benchmark cases first, then profile-specific checks after action.
4. Persistence: record verdict, evidence, scores, failed attempts, benchmark promotions, agent handoffs, worktree mappings, and what not to retry.
5. Scheduling: decide `SUCCESS`, `NEXT_ITERATION`, `REPLAN`, `PAUSE`, `ESCALATE`, or `STOP`.

Find real signals before proposing work. Convert findings into one bounded intervention with impact, confidence, effort, risk, hypothesis, success evidence, rollback or escalation condition, owner boundary, allowed files/surfaces, and denylist.

## Run-Until-Done Controller

Default execution is until success or stop condition. Use `target=PASS` for binary verification or `target_score=8/10` for rubric verification. Default plateau patience is 3 consecutive iterations without meaningful evidence improvement.

Stop conditions:
- `SUCCESS`: verification verdict is `PASS`, or every locked rubric criterion meets target.
- `EXHAUSTED`: explicit user cap, token budget, wall-clock budget, or change budget reached.
- `PLATEAU`: plateau patience exhausted.
- `REGRESSION`: product quality, tests, or target metric worsens materially.
- `BUDGET`: token/time/change cap exceeded.
- `HUMAN_GATE`: approval required.
- `ENV`: same environment blocker repeats twice.
- `UNKNOWN`: required data unavailable; route to instrumentation.

Failure routing:
- `discovery_gap` -> instrument, collect data, or switch to report-only.
- `handoff_scope` -> re-scope smaller or escalate.
- `verification_fail` -> next iteration targets the failed criterion.
- `persistence_gap` -> halt and repair state/run-log before continuing.
- `scheduling_risk` -> pause or reduce cadence.

## Execution Orchestration

Use one agent when findings share state, require one mental model, or may conflict on the same files. Use parallel agents only for independent interventions, failures, surfaces, test files, or investigation domains.

For parallel agents:
- Create one task per domain with scope, goal, constraints, expected output, verification command, and allowed files/surfaces.
- Record tasks in `AGENT_HANDOFF.md` or `agent-tasks/<task-id>.md`.
- Require each agent to return root cause/hypothesis, changed files, verification evidence, risks, and next handoff.
- Review conflicts before integration.
- Run matching benchmark cases and the relevant full verification suite after integration.

For file-changing parallel agents, use isolated workspaces. Detect existing linked worktrees, treat submodules as repos, prefer native worktree tools when available, fall back to `git worktree`, verify `.worktrees/` or `worktrees/` is ignored, and write `worktree-map.md`. If blocked, record the blocker and run sequentially or report-only.

Parallel execution cannot pass until agent results are reviewed, changed files are conflict-checked, matching benchmarks pass, relevant tests/build/Playwright checks pass or a non-pass verdict is persisted, and state/run-log/benchmark/handoff/worktree map are updated.

## Error-To-Benchmark Promotion

Every failed iteration must become future regression protection.

When verdict is `FAIL`, `REGRESSION`, `PARTIAL` with a defect, `ENV`, or `UNKNOWN`:
1. Classify the error.
2. Append raw run evidence and a structured `Finding` block to `product-loop-run-log.md`.
3. Decide whether to promote.
4. Promote durable facts to `PRODUCT_LOOP_STATE.md`.
5. Create or update a regression case in `PRODUCT_LOOP_BENCHMARK.md` only from a promoted finding.
6. In the next iteration, run matching active benchmark cases before new optimization.

Do not create separate error or finding files. The single run-log entry contains `Raw Run Result`, `Finding`, and `Benchmark Promotion` blocks. Use `references/state-schema.md` for exact fields.

Error classes: `ui_regression`, `runtime_error`, `metric_regression`, `content_drift`, `env_blocker`, `scope_regression`.

Benchmark gate:
- During Discovery, load `PRODUCT_LOOP_BENCHMARK.md` and select active cases matching current surface, profile, files, or metric.
- During Verification, run matching active cases before accepting new intervention.
- If an active case fails, classify as `REGRESSION`, persist it, and fix that case before optimizing forward.
- Retire a benchmark only when the product surface or requirement is intentionally removed and recorded in state.

## Output Report

End each run with:

- Intent: detected intent, assumptions, and user confirmations.
- Profile: profiles used.
- Discovery: signals, findings, state changes, noise ignored, data gaps.
- Handoff: chosen intervention, hypothesis, scope, risk gate, execution strategy, agent task ids, independence rationale, worktree strategy, integration owner.
- Verification: commands/checks/data sources, verdict, Playwright evidence when app verification was needed, UX/UI taste/slop score when visual quality matters, parallel-agent conflict review when used.
- Persistence: run-log append, state promotions, benchmark promotions, raw run result, finding id/status, benchmark promotion decision.
- Scheduling: next action and rationale.
- Iteration State: iteration number, stop condition, target, score/verdict, next targeted criterion.

Required after each iteration:
- Run-log entry id/timestamp.
- State fields promoted.
- Error classification.
- Benchmark cases matched before verification.
- Benchmark verdict.
- Benchmark regression case id created or updated.
- Agent handoff files updated.
- Worktree map updated.
- Evidence retained for future regression checks.
