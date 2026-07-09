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

Use a human-confirmed evaluation contract before first actioning in a repo or
before any material change to Metrics, Criteria, or Benchmark. The agent may
recommend candidate defaults, but the saved review selection plus CLI
confirmation is the source of truth.

Existing locked contract fast path: when `.loop-harness/criteria/current.md`
is already `Contract status: locked`, `.loop-harness/review/evaluation-contract-confirmed.json`
exists, and Metrics, Criteria, and Benchmark are unchanged, skip the A-lite review page
and continue from stored state. Reopen the selection gate only when the existing contract is missing, stale, or materially incomplete.

Use `AskUserQuestion` or the review page for decisions that need human choice:
- Primary product surface or user flow.
- Primary metric when `METRIC_OPTIMIZE` or `run-until-done` depends on it.
- Criteria that define pass/fail quality.
- Benchmark seeds that should gate the loop.
- Target threshold.
- Human gate: pricing, payment, auth, permissions, secrets, destructive migration, legal/compliance, brand-sensitive copy, or major product direction.
- Scheduled/actioning loop approval when cost or risk is material.

Safe defaults can be recommendations, not silent actioning choices. Mark recommended
Metrics, Criteria, and Benchmark candidates as `(Recommended)` in the review page,
then wait for saved selection and CLI confirmation before locking the contract.

## Start Of Run

1. Identify intent and product surface in one line.
2. Use `.loop-harness/` as the default artifact root in target repos unless the user explicitly chooses another folder.
3. Load existing artifacts if present: `.loop-harness/PRODUCT_LOOP.md`, `.loop-harness/PRODUCT_LOOP_STATE.md`, `.loop-harness/criteria/current.md`, `.loop-harness/product-loop-run-log.md`, `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`, and `.loop-harness/product-loop-budget.md`.
4. Scaffold missing ongoing-loop artifacts into `.loop-harness/` from `assets/templates/`.
5. Select profiles using `references/profiles.md`.
6. Select a pattern using `references/patterns.md` and `assets/templates/product-loop-patterns.json` when cadence or recurring scope matters.
7. Select local global criteria/seeds only when the contract is missing criteria/seeds, this is a first run, or the user asks for reusable/global guidance.
8. If the existing locked contract fast path applies, skip the A-lite review page and continue to benchmark selection and batch planning.
9. Otherwise, brainstorm the candidate Metrics, Criteria, and Benchmark options with the user. Use an installed brainstorming workflow when available; otherwise ask concise equivalent questions.
10. Serve the A-lite review page with `scripts/review_contract.py serve --repo <repo> --candidates <candidates.json>`. The page must group choices as `Metrics`, `Criteria`, and `Benchmark`, with independent No/Yes controls for every candidate.
11. Read `.loop-harness/review/evaluation-contract-selection.json`, summarize the selected Metrics, Criteria, and Benchmark in CLI, and ask for explicit confirmation.
12. Lock the human-confirmed evaluation contract in `.loop-harness/criteria/current.md` using `scripts/review_contract.py confirm --repo <repo> --yes`.
13. Ask only unresolved target, evidence-source, risk, or schedule decisions after the selection gate.
14. Plan the first iteration as an execution batch with lane decomposition before actioning.
15. Run `scripts/product_loop_audit.py <repo-root-or-.loop-harness> --min-level L2` after scaffolding, material artifact schema changes, or before scheduled/unattended operation. For ordinary iterations that only append run evidence, validate the latest run-log entry instead.
16. Run `scripts/product_loop_cost.py --pattern <pattern-id> --level L1|L2|L3 --cadence <interval>` before scheduling recurring loops.

## Execution Modes

- `report-only`: discover, verify signals, persist state, and stop without source changes.
- `run-until-done`: repeat full five-phase iterations until a stop condition fires.
- `scheduled`: run on cadence; each tick starts a fresh process and continues from `.loop-harness/*` state within budget.

There is no `action-once` mode. Any loop that changes files, product behavior, docs, metrics, or release state must use `run-until-done`, even when it stops after one successful iteration.

`run-until-done` requires `criteria/current.md` with `Contract status: locked`, a measurable target or locked rubric, safety budget or kill switch, `target_min`, stop conditions, plateau patience, and human gates written to state before actioning. The locked file must come from the human-confirmed evaluation contract when this is the first run or when Metrics, Criteria, or Benchmark changed materially. For metric targets, confirm primary metric, baseline window, target threshold, and sample/window or proxy evidence.

## Evaluation Contract Bootstrap

Before any actioning iteration, `.loop-harness/criteria/current.md` must contain the locked evaluation contract with `Contract status: locked`:
- Product surface and user flow.
- Primary metric or acceptance rubric.
- Baseline window, data source, target, target minimum, and direction.
- Acceptance criteria and pass thresholds.
- Benchmark seeds and activation rule.
- Playwright URL/route, viewports, flow steps, assertions, and screenshot/trace expectation when app verification is relevant.
- User confirmations, human gates, and non-goals.

If this contract is missing, materially incomplete, or not `Contract status: locked`, use `report-only` discovery or an `evaluation-contract` bootstrap batch. Do not action product changes until Metrics, Criteria, and Benchmark are selected through the review page and confirmed in CLI. Record selected global/local criteria and benchmark seeds in `PRODUCT_LOOP_STATE.md`; seeds are not active benchmarks until repo-local evidence promotes them.

## Five Phases

Every iteration must execute all five phases. An iteration is one planned execution batch, not necessarily one tiny fix.

1. Discovery: refresh state, benchmark cases, previous failures, and current product signals.
2. Handoff: choose one execution batch containing one or more bounded lanes, each with hypothesis, scope, risk, owner boundary, allowed files/surfaces, verification command, dependencies, and worktree plan.
3. Verification: run matching benchmark cases first, then profile-specific checks after action.
4. Persistence: record verdict, evidence, scores, failed attempts, benchmark promotions, agent handoffs, worktree mappings, and what not to retry.
5. Scheduling: choose exactly one next action: `stop_success`, `run_again_now`, `schedule`, `pause`, or `escalate`.

Find real signals before proposing work. Convert findings into a bounded execution batch. If multiple findings are independent, decompose them into lanes and execute them within the same iteration; do not create separate iterations just because there is more than one known lane.

## Iteration Batch Planning

Before implementation, classify the current batch:

- `single-lane`: one concern, one owner boundary, one verification path.
- `multi-lane`: independent lanes can run in parallel or be executed sequentially inside the same iteration.
- `sequential`: lanes are known but have true dependencies; document the dependency and finish the sequence inside the same iteration when budget allows.
- `discovery-only`: no safe actioning target exists yet.

Each lane must define:
- Lane id.
- Goal and hypothesis.
- Allowed files/surfaces and forbidden shared state.
- Dependencies and conflict risk.
- Owner or agent.
- Verification command/evidence.
- Expected output.

Parallelization strategy:
- Use parallel agents/worktrees when lanes have independent ownership and low integration risk.
- Use one local controller for tightly coupled files, high context-transfer cost, or one-command fixes.
- Use sequential execution inside the same iteration when lanes are independent enough to plan together but too small to justify agent dispatch.

Next iteration rule:
- Start a new iteration only after the planned batch has run integrated verification and the result is not `PASS`.
- Do not defer known independent lanes to later iterations unless budget, human gate, conflict risk, or environment blockers are recorded.
- If the batch fails, the next iteration targets the failed lane or failed integrated criterion, not untouched work that should have been in the original batch.

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

Use one agent when findings share state, require one mental model, or may conflict on the same files. Use parallel agents only for independent lanes, interventions, failures, surfaces, test files, or investigation domains.

For parallel agents:
- Create one task per lane/domain with scope, goal, constraints, expected output, verification command, and allowed files/surfaces.
- Record tasks in `.loop-harness/AGENT_HANDOFF.md` or `.loop-harness/agent-tasks/<task-id>.md`.
- Require each agent to return root cause/hypothesis, changed files, verification evidence, risks, and next handoff.
- Review conflicts before integration.
- Run matching benchmark cases and the relevant full verification suite after integration.

For file-changing parallel agents, use isolated workspaces. Detect existing linked worktrees, treat submodules as repos, prefer native worktree tools when available, fall back to `git worktree`, verify `.worktrees/` or `worktrees/` is ignored, and write `.loop-harness/worktree-map.md`. If blocked, record the blocker and run sequentially or report-only.

Parallel execution cannot pass until agent results are reviewed, changed files are conflict-checked, matching benchmarks pass, relevant tests/build/Playwright checks pass or a non-pass verdict is persisted, and state/run-log/benchmark/handoff/worktree map are updated.

## Error-To-Benchmark Promotion

Every failed iteration must become future regression protection.

When verdict is `FAIL`, `REGRESSION`, `PARTIAL` with a defect, `ENV`, or `UNKNOWN`:
1. Classify the error.
2. Append raw run evidence and a structured `Finding` block to `.loop-harness/product-loop-run-log.md`.
3. Decide whether to promote.
4. Promote durable facts to `.loop-harness/PRODUCT_LOOP_STATE.md`.
5. Create or update a regression case in `.loop-harness/PRODUCT_LOOP_BENCHMARK.md` only from a promoted finding.
6. In the next iteration, run matching active benchmark cases before new optimization.

Do not create separate error or finding files. The single run-log entry contains `Raw Run Result`, `Finding`, and `Benchmark Promotion` blocks. Use `references/state-schema.md` for exact fields.

Error classes: `ui_regression`, `runtime_error`, `metric_regression`, `content_drift`, `env_blocker`, `scope_regression`.

Benchmark gate:
- During Discovery, load `.loop-harness/PRODUCT_LOOP_BENCHMARK.md` and select active cases matching current surface, profile, files, or metric.
- Also load active split case files under `.loop-harness/benchmarks/active/*.md` when present. Keep `.loop-harness/PRODUCT_LOOP_BENCHMARK.md` as a compact active index; archive retired or old cases under `.loop-harness/benchmarks/archive/`.
- During Discovery, optionally select general local criteria/seeds from `~/.codex/loop-harness/knowledge/` through `scripts/select_knowledge.py`; do not load the whole global store into context.
- During Verification, run matching active cases before accepting new intervention.
- If an active case fails, classify as `REGRESSION`, persist it, and fix that case before optimizing forward.
- Retire a benchmark only when the product surface or requirement is intentionally removed and recorded in state.
- When `product-loop-run-log.md` grows large, keep recent entries plus archive pointers there and move detailed historical entries under `.loop-harness/runs/archive/`.

## Global Knowledge Promotion

Repo-local learning comes first. Only consider global promotion after the run-log finding and repo-local benchmark promotion exist.

Use:

```bash
python3 <skill-dir>/scripts/promote_global_knowledge.py --repo <repo>
```

Default behavior writes a gated candidate to `~/.codex/loop-harness/knowledge/inbox/`. Use `--promote` only after explicit approval or review confirms the finding is generally reusable. Keep env blockers, domain-specific failures, and one-off noise repo-local.

## Watchdog Scheduler

Use `scripts/watchdog.py` for local recurring loops:

```bash
python3 <skill-dir>/scripts/watchdog.py setup --repo <repo> --command "<loop command>" --cadence daily
python3 <skill-dir>/scripts/watchdog.py status --repo <repo>
python3 <skill-dir>/scripts/watchdog.py pause --repo <repo>
python3 <skill-dir>/scripts/watchdog.py resume --repo <repo>
python3 <skill-dir>/scripts/watchdog.py tail --repo <repo>
python3 <skill-dir>/scripts/watchdog.py tick --repo <repo>
python3 <skill-dir>/scripts/watchdog.py uninstall --repo <repo>
```

Scheduler status, tick logs, pause markers, and lock files live under `.loop-harness/schedules/`. Each scheduled tick is a new process that reads `.loop-harness/PRODUCT_LOOP_STATE.md`, `.loop-harness/criteria/current.md`, the run log, benchmark index, budget, handoff, and worktree map. It resumes the loop through persisted state; the interactive chat transcript stays outside the scheduler contract.

Before `setup`, run the cost check, confirm the kill switch, and ensure `run-until-done` loops have locked criteria. During `tick`, acquire the schedule lock before running and release it after persistence; an existing lock means the next tick exits with a persisted scheduling decision instead of overlapping work.

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
- Batch type, lane ids, and parallelization rationale.
- Error classification.
- Benchmark cases matched before verification.
- Benchmark verdict.
- Benchmark regression case id created or updated.
- Agent handoff files updated.
- Worktree map updated.
- Evidence retained for future regression checks.
