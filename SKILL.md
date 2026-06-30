---
name: loop-harness
description: Autonomous product optimization loop harness for improving live products, prototypes, docs, and engineering quality over repeated runs. Use when Codex should discover product improvement opportunities, prioritize them, form hypotheses, hand off bounded interventions, verify evidence, persist learnings, and decide whether to schedule the next loop across UX, growth metrics, engineering quality, content/docs, or release readiness.
---

# Loop Harness

Use this skill to run controlled product optimization loops. A loop must improve a product with evidence, not generate generic recommendations.

## Core Rule

Every run follows exactly five phases:

1. Discovery
2. Handoff
3. Verification
4. Persistence
5. Scheduling

Do not skip a phase. If a phase lacks evidence, record the gap and route the run to instrumentation, human handoff, or report-only mode.

## Intent Detection And User Confirmation

State intent before choosing profiles or execution mode:

- `UX_OPTIMIZE`: improve a screen, flow, copy, accessibility, or product comprehension.
- `METRIC_OPTIMIZE`: improve activation, conversion, retention, completion, revenue, or funnel movement.
- `ENGINEERING_QUALITY`: fix bugs, performance, CI, reliability, or product-affecting technical quality.
- `RELEASE_READY`: prepare a changed product surface for deployment or release.
- `INSTRUMENT`: add or repair analytics/observability before claiming product improvement.
- `POST_LAUNCH_LEARN`: learn from shipped behavior, support, feedback, metrics, and errors.

Default intent:
- If the user asks to "improve/optimize product" without a metric, use `UX_OPTIMIZE + ENGINEERING_QUALITY` in `run-until-done` when a target can be inferred; otherwise use `report-only` discovery to define the target.
- If the user names conversion, activation, retention, funnel, revenue, experiment, or metric, use `METRIC_OPTIMIZE`; require a metric decision before `run-until-done`.
- If metrics are desired but unavailable or untrusted, switch to `INSTRUMENT`.

Use `AskUserQuestion` only for real decisions that cannot be safely inferred:
- Which primary product surface or user flow to optimize.
- Which primary metric to optimize when `METRIC_OPTIMIZE` or `run-until-done` depends on a metric.
- Which target threshold defines done.
- Whether to cross a human gate: pricing, payment, auth, permissions, secrets, destructive migration, legal/compliance, brand-sensitive copy, or major product direction.
- Whether to enable scheduled/actioning loops when cost or risk is material.

Do not ask when a safe default exists. Instead, record the assumption in `PRODUCT_LOOP_STATE.md` and continue. Prefer 2-3 concrete choices when asking.

## Start Of Run

1. Identify intent and state it in one line.
2. Identify the product surface: app, route, prototype, docs, repo, release, or metric area.
3. Load existing loop artifacts if present:
   - `PRODUCT_LOOP.md`
   - `PRODUCT_LOOP_STATE.md`
   - `product-loop-run-log.md`
   - `PRODUCT_LOOP_BENCHMARK.md`
   - `product-loop-budget.md`
4. If artifacts are missing and the user wants an ongoing loop, scaffold from `assets/templates/`.
5. Select one or more optimization profiles. See `references/profiles.md`.
6. Select a product loop pattern when cadence or recurring scope matters. See `references/patterns.md` and `assets/templates/product-loop-patterns.json`.
7. Ask only for unresolved metric/target/risk/schedule decisions listed above.
8. Run `scripts/product_loop_audit.py <repo-or-folder>` when artifacts exist or after scaffolding.
9. Run `scripts/product_loop_cost.py --pattern <pattern-id> --level L1|L2|L3 --cadence <interval>` before scheduling recurring loops.

## Skill Package Layout

Keep runtime skill resources separate from skill self-evaluation artifacts:

- `references/`: operational guidance loaded as needed while using the skill.
- `scripts/`: deterministic helpers for auditing product-loop artifacts and cost.
- `assets/templates/`: files copied or adapted into the target repo when scaffolding a loop.
- `benchmark/`: evals, rubrics, criteria, and transcript scoring for validating `loop-harness` behavior itself.
- `self/loop-runs/`: durable logs/state from using `loop-harness` to improve `loop-harness`.

Do not treat files in `benchmark/` or `self/loop-runs/` as target-repo loop artifacts. Target-repo artifacts live in the product repo being optimized, usually scaffolded from `assets/templates/`.

## Execution Modes

Choose one mode at the start of each run:

- `report-only`: Discover, verify signals, persist state, and stop without source changes.
- `run-until-done`: Repeat full five-phase iterations until a stop condition fires.
- `scheduled`: Run on cadence; each tick may be report-only or run-until-done within budget.

There is no `action-once` mode. Any loop that changes files, product behavior, docs, metrics, or release state must use `run-until-done`, even when it stops after the first successful iteration.

`run-until-done` requires:
- A measurable target or acceptance rubric.
- Explicit token/wall-clock budget, kill switch, or other safety budget.
- `target_min` or minimum acceptable verification bar.
- Stop conditions, plateau patience, and human gates written to state before actioning.

If these are missing, ask for the missing decision or infer a conservative default. If the missing decision cannot be resolved safely, downgrade to `report-only`; do not action work without a run-until-done target and stop conditions.

For metric-based run-until-done, confirm:
- Primary metric.
- Baseline window.
- Target threshold.
- Minimum sample/window or proxy evidence allowed before final judgment.

## Execution Orchestration

For `run-until-done` or actioning `scheduled` runs, decide whether work is sequential or parallel before editing files.

Use a single agent when findings are related, share state, require one mental model, or may conflict on the same files. Use parallel agents only when there are 2+ independent interventions, failures, surfaces, test files, or investigation domains that can be completed without shared mutable state.

When dispatching parallel agents:
1. Group work by independent domain.
2. Create one focused task per domain with scope, goal, constraints, expected output, verification command, and files/surfaces allowed.
3. Give each agent only the task-local context it needs; do not rely on conversation history.
4. Record dispatched tasks in `AGENT_HANDOFF.md` or `agent-tasks/<task-id>.md`.
5. Require each agent to return root cause or hypothesis, files changed, verification evidence, unresolved risks, and next handoff.
6. Review every agent result for conflicts before integration.
7. Run matching benchmark cases and the full relevant verification suite after integration.

For file-changing parallel agents, use isolated workspaces:
- Detect whether the current checkout is already a linked worktree before creating another one.
- Treat git submodules as normal repos, not as worktrees.
- Prefer native worktree tools when the environment provides them.
- Fall back to `git worktree` only when no native tool exists.
- Verify project-local `.worktrees/` or `worktrees/` is ignored before creating a worktree.
- Write task-to-worktree mapping to `worktree-map.md`.
- If worktree creation is blocked, record the blocker and run sequentially or in report-only mode.

Parallel execution cannot mark the loop `PASS` until integration evidence exists:
- agent summaries reviewed;
- changed files conflict check completed;
- matching active benchmark cases pass;
- relevant tests/build/Playwright checks pass or a non-pass verdict is persisted;
- state, run log, benchmark, handoff, and worktree map are updated.

## Run-Until-Done Controller

In `run-until-done`, each iteration must execute all five phases. Do not loop only the implementation step.

Default limits:
- Default execution is `until-done`: continue until success or a stop condition fires.
- `target=PASS` for binary verification, or `target_score=8/10` for rubric-based verification.
- Default plateau patience is 3 consecutive iterations with no meaningful evidence improvement.
- Stop early on human gate, budget cap, environment blocker, regression, or plateau.

Iteration loop:

```text
while stop condition has not fired:
  Discovery: refresh state, benchmark cases, previous failures, and current product signals.
  Handoff: choose or refine one bounded intervention and hypothesis; decide single-agent vs parallel execution and worktree isolation.
  Verification: run matching benchmark cases, then profile-specific evidence checks after action.
  Persistence: record verdict, evidence, scores, failed attempts, benchmark promotions, agent handoffs, worktree mappings, and what not to retry.
  Scheduling: decide SUCCESS, NEXT_ITERATION, REPLAN, PAUSE, ESCALATE, or STOP.
```

Stop conditions:
- `SUCCESS`: verification verdict is `PASS`, or every locked rubric criterion meets target.
- `EXHAUSTED`: explicit user-provided iteration cap, token budget, wall-clock budget, or change budget reached.
- `PLATEAU`: plateau patience is exhausted after repeated iterations show no meaningful evidence improvement.
- `REGRESSION`: product quality, tests, or target metric worsens materially.
- `BUDGET`: token/time/change cap exceeded.
- `HUMAN_GATE`: approval is required.
- `ENV`: same environment blocker repeats twice.
- `UNKNOWN`: required data is unavailable; route to instrumentation.

Failure routing:
- `discovery_gap` -> instrument, collect data, or switch to report-only.
- `handoff_scope` -> re-scope smaller or escalate.
- `verification_fail` -> next iteration targets the failed criterion.
- `persistence_gap` -> halt and repair state/run-log before continuing.
- `scheduling_risk` -> pause or reduce cadence.

## Error-To-Benchmark Promotion

Every failed iteration must become future regression protection.

When verdict is `FAIL`, `REGRESSION`, `PARTIAL` with a defect, `ENV`, or `UNKNOWN`:
1. Classify the error.
2. Append raw run evidence and a structured `Finding` block to `product-loop-run-log.md`.
3. Decide whether the finding should be promoted.
4. Promote durable facts to `PRODUCT_LOOP_STATE.md`.
5. Create or update a regression case in `PRODUCT_LOOP_BENCHMARK.md` only from a promoted finding.
6. In the next iteration, run matching active benchmark cases before any new optimization.

Do not create a separate error log or findings file. The single run-log entry must contain all three layers:

```markdown
#### Raw Run Result
- Verdict:
- Verification evidence:
- Error output:
- Failed assertions:

#### Finding
- Finding id:
- Error class:
- Symptom:
- Evidence:
- Root cause/hypothesis:
- Reproduction steps:
- Severity:
- Confidence:
- Status: open | promoted | dismissed | resolved | not_applicable

#### Benchmark Promotion
- Promotion decision: promoted | not_promoted
- Benchmark case id:
- Matching rule:
- Expected result:
- Verification command:
- Status: active | retired | not_applicable
```

Error classes:
- `ui_regression`: broken visible state, layout, responsive behavior, accessibility, or user flow.
- `runtime_error`: console error, server error, crash, failing route, or broken interaction.
- `metric_regression`: target metric, event, funnel, or data quality worsens.
- `content_drift`: docs/copy/spec no longer matches product behavior or source of truth.
- `env_blocker`: local server, dependency, auth/session, data, or tool issue blocks verification.
- `scope_regression`: intervention touched unrelated files, widened scope, or crossed a denylist.

Regression case schema:

```markdown
## Regression Case: <stable-id>

- Source run-log entry:
- Error class:
- Surface/URL:
- Trigger condition:
- Playwright steps:
- Expected result:
- Failure evidence:
- Matching rule:
- Owner profile:
- Last failed:
- Last passed:
- Status: active | retired
```

Benchmark gate:
- During Discovery, load `PRODUCT_LOOP_BENCHMARK.md` and select active cases whose matching rule touches the current surface/profile/files/metric.
- During Verification, run matching benchmark cases before accepting any new intervention.
- If an active benchmark case fails, classify the iteration as `REGRESSION`, persist the failure, and fix that case before optimizing forward.
- Retire a benchmark case only when the product surface or requirement is intentionally removed and that decision is recorded in state.

## Phase 1: Discovery

Find real signals before proposing work.

Allowed signal sources:
- UX/browser inspection, screenshots, user flows, accessibility checks.
- Product metrics, funnel data, analytics, event logs, user feedback.
- Bugs, CI failures, errors, performance traces, release smoke results.
- Docs, onboarding, support requests, PRD/prototype mismatches.
- Existing `PRODUCT_LOOP_STATE.md` watchlist, failed attempts, and human decisions.

Rules:
- Prefer real data. If data is missing, propose instrumentation or a report-only discovery pass.
- Separate signal from interpretation.
- Record noise and ignored items so the next run does not rediscover them.

Output:
```markdown
### Discovery
- Signals inspected:
- New findings:
- Existing state changes:
- Noise ignored:
- Data gaps:
```

## Phase 2: Handoff

Convert findings into one bounded intervention.

For each candidate, score:
- Impact: expected product/user/business value.
- Confidence: evidence strength.
- Effort: implementation and verification cost.
- Risk: potential harm, ambiguity, reversibility.

Choose at most one primary intervention per loop unless the user explicitly asks for batch work. Write a hypothesis:

```markdown
If we change <surface/intervention>, then <target user/product outcome> should improve because <evidence>.
Success evidence: <metric/check/rubric>.
Rollback/escalation: <condition>.
```

Handoff must define owner boundary, files/surfaces, denylisted areas, acceptance evidence, and whether the loop is report-only, assisted, or actioning.

Human approval is required for pricing, payments, auth, permissions, secrets, destructive migrations, irreversible data changes, legal/compliance, brand-sensitive copy, or major product direction.

For actioning runs, handoff must also define:
- Execution strategy: `single-agent`, `parallel-agents`, or `sequential-agents`.
- Independence rationale when using parallel agents.
- Agent task ids and owner domains.
- Worktree strategy and task-to-worktree map when edits may conflict.
- Integration owner and integration verification commands.
- Conflict policy for agents editing the same file or surface.

## Phase 3: Verification

Verify the intervention independently from the implementation story.

Use profile-specific verification from `references/verification.md`. Typical checks:
- Browser smoke, screenshots, visual comparison, accessibility.
- Tests, lint, typecheck, build, CI, performance.
- Metric query, event validation, funnel sanity check.
- Content clarity review, link validation, PRD/prototype alignment.

If verification requires launching or inspecting an app, use Playwright for real browser evaluation:
- Discover the dev server command and target URL from the repo.
- Start or reuse the local server and record the URL.
- Use Playwright to navigate the actual route, exercise the primary flow, and inspect visible states.
- Capture evidence: viewport, steps, assertions, errors, console/network failures when relevant, and screenshots or traces when useful.
- If Playwright or the app server cannot run, verdict is `UNKNOWN` or `ENV`; do not mark `PASS` from static inspection alone.

For UX/UI visual-quality work, Playwright is required but not sufficient when the surface can be opened. Combine it with:
- `design-taste-frontend` for landing pages, portfolios, redesigns, onboarding, conversion-focused web surfaces, brief fit, hierarchy, composition, and taste scoring.
- `design-slop-ban` for visible UI linting across websites, web apps, mobile UI, design systems, copy, heroes, motion, accessibility, responsive states, and generic AI-design failure modes.

UX/UI visual-quality `PASS` requires taste/slop score `>=8/10` and no critical slop violation. If the full `design-taste-frontend` rubric does not fit the surface, record why and still apply `design-slop-ban` plus relevant hierarchy, copy, responsive, accessibility, and product-specificity checks.

Rules:
- The implementer cannot mark its own work done without evidence.
- If verification cannot run, mark `ESCALATE_HUMAN` or `NEEDS_INSTRUMENTATION`.
- Do not accept screenshots, test claims, or metric claims without source details.
- For parallel-agent runs, do not accept agent summaries alone; verify integrated work in the coordinator workspace after reviewing conflicts.

Verdicts:
- `PASS`: evidence supports the hypothesis or the bounded acceptance criteria.
- `PARTIAL`: improvement exists but follow-up is needed.
- `FAIL`: evidence rejects the change or risk is too high.
- `UNKNOWN`: required evidence is missing.

## Phase 4: Persistence

Write durable state outside the conversation.

Update:
- `PRODUCT_LOOP_STATE.md`: current opportunities, selected intervention, status, failed attempts, human decisions, next action.
- `product-loop-run-log.md`: append-only run summary with raw run result, structured finding, benchmark promotion decision, timestamp, profile, signals, action, verification, verdict, and next schedule decision.
- `PRODUCT_LOOP_BENCHMARK.md`: promoted checks, known-good evidence, recurring smoke flows, and do-not-regress rules derived from run logs.
- `AGENT_HANDOFF.md` or `agent-tasks/`: task scopes, assigned agents, constraints, outputs, integration decisions.
- `worktree-map.md`: worktree paths, branches, task ids, status, verification, and cleanup/integration decision.

After every iteration, persist before deciding the next loop action:
1. Append the raw iteration result to `product-loop-run-log.md`.
2. Add a structured `Finding` block in the same run-log entry. Use `Status: not_applicable` and `Error class: none` when the iteration passed cleanly.
3. Add a `Benchmark Promotion` block in the same run-log entry.
4. Promote durable facts from the log into `PRODUCT_LOOP_STATE.md`: active status, next target, failed attempts, and what not to retry.
5. Promote reusable verification into `PRODUCT_LOOP_BENCHMARK.md`: Playwright flows, commands, expected states, accepted baselines, regression checks.
6. Keep transient noise only in the run log unless it recurs.
7. For every failed or regressed iteration, add or update a regression case with error class, matching rule, expected result, last failed, and status when the finding is promoted.
8. For parallel runs, update handoff and worktree map with agent result, conflict review, integration verdict, and cleanup decision.

Persist failed hypotheses and what not to retry. Preserve useful learnings even when no code/docs change was made.

## Phase 5: Scheduling

Decide the next loop action:
- `stop_success`: goal met or no valuable next action.
- `run_again_now`: cheap high-confidence follow-up exists.
- `schedule`: cadence is useful and budget allows it.
- `pause`: missing data, budget, reviewer, or unsafe context.
- `escalate`: human decision required.

Use `product-loop-budget.md` for max runs, max changes, max subagents, daily token cap, and kill switch. High-frequency loops need early exit when no actionable signal exists.

## Output Format

End each run with:

```markdown
## Loop Harness Report

### Intent
<detected intent, assumptions, and user confirmations>

### Profile
<profiles used>

### Discovery
<signals and findings>

### Handoff
<chosen intervention, hypothesis, scope, risk gate>
<execution strategy, agent task ids, independence rationale, worktree strategy, integration owner>

### Verification
<commands/checks/data sources, verdict>
<Playwright URL, flow steps, assertions, screenshots/traces when app verification was needed>
<UX/UI taste/slop benchmark score and critical slop verdict when visual quality matters>
<parallel-agent conflict review and integrated verification when parallel execution was used>

### Persistence
<run-log append, state promotions, benchmark promotions, or reason not updated>
<raw run result, finding id/status, benchmark promotion decision>

Required after each iteration:
- Run-log entry id/timestamp:
- State fields promoted:
- Error classification: `<none | ui_regression | runtime_error | metric_regression | content_drift | env_blocker | scope_regression>`
- Benchmark cases matched before verification:
- Benchmark verdict: `<PASS | FAIL | REGRESSION | UNKNOWN | not applicable>`
- Benchmark regression case id created/updated:
- Agent handoff files updated:
- Worktree map updated:
- Evidence retained for future regression checks:

### Scheduling
<next action and rationale>

### Iteration State
<iteration number, stop condition, target, score/verdict, next targeted criterion>
```

## References

- Read `references/profiles.md` when selecting optimization profiles.
- Read `references/patterns.md` when choosing a reusable product loop pattern.
- Read `references/scoring.md` when ranking candidates or judging readiness.
- Read `references/verification.md` before accepting an intervention.
- Read `references/state-schema.md` before creating or updating loop artifacts.
- Read `references/failure-modes.md` when a loop stalls, repeats, or becomes unsafe.

## Validation

After creating or changing loop artifacts, run:

```bash
python3 <skill-dir>/scripts/product_loop_audit.py <product-repo-or-folder> --min-level L2
python3 <skill-dir>/scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d
```

Use `--min-level L3` for scheduled or unattended loops. Use `--strict` when the audit is a CI/release gate; strict mode requires L3 and fails on any warning or miss. Hard misses such as negated evidence or failed iterations without promoted active regression cases must exit non-zero even when the numeric score is otherwise high enough for L1.

When validating loop-harness behavior against real pressure-test transcripts, run:

```bash
python3 <skill-dir>/benchmark/run_pressure_eval.py --transcripts <transcript-dir>
```

For skill package validation, run:

```bash
python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```
