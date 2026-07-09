# Product Loop

Product surface: loop-harness skill package
Optimization goal: keep loop-harness self-evaluable through strict artifact, metadata, benchmark, and pressure-test behavior gates
Intent: ENGINEERING_QUALITY
Pattern: daily-product-triage
Profiles: engineering-quality, content-docs
Readiness level: L2 assisted optimization
Execution mode: run-until-done
Cadence: manual

## Scope

Watched surfaces:
- `SKILL.md`
- `references/`
- `scripts/`
- `assets/templates/`
- `assets/templates/criteria/`
- `assets/templates/PRODUCT_LOOP.md`
- `assets/templates/PRODUCT_LOOP_STATE.md`
- `assets/templates/product-loop-budget.md`
- `benchmark/`
- `benchmark/fixtures/pass/`

Non-goals:
- Run live subagents from the eval runner.
- Change the runtime orchestration contract beyond benchmark support.

Denylist:
- Secrets, credentials, global Codex config outside installed skill sync.

## Human Gates

- Pricing, payment, auth, permissions, secrets.
- Destructive migrations or irreversible data changes.
- Legal/compliance/brand-sensitive decisions.
- Major product direction changes.

## Verification

Evaluation contract: self/loop-runs/criteria/current.md

Primary checks:
- `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py`
- `python3 scripts/product_loop_audit.py self/loop-runs --min-level L3`
- `python3 scripts/validate_run_log_entry.py self/loop-runs/product-loop-run-log.md`
- `python3 scripts/product_loop_audit.py assets/templates --min-level L2`
- `python3 scripts/select_benchmarks.py --repo <skill-dir> --profile engineering-quality --intent ENGINEERING_QUALITY --surface skill-package --include-skill --require`
- `python3 benchmark/test_tooling_regressions.py`
- `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass`
- `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-dir>`

Metric/data sources:
- Pressure transcript score target: `>=8/10` per critical case.

Browser routes:
- None for this skill-package intervention.

Playwright required for app verification: no
Playwright smoke flows:
Test commands:
- See primary checks.

## Execution Orchestration

Execution strategy: single-agent
Batch planning required before actioning: yes
Batch types: single-lane | multi-lane | sequential | discovery-only
Lane decomposition fields: lane id, goal, allowed files/surfaces, dependencies, verification command, owner
Parallelization strategy: use one execution batch per iteration; include independent lanes in the same iteration when safe
Parallel agents allowed when domains are independent: yes
Agent handoff file: self/loop-runs/AGENT_HANDOFF.md
Agent task directory: agent-tasks/
Worktree isolation for file-changing parallel agents: yes
Worktree map: self/loop-runs/worktree-map.md
Integration verification: source validation, installed skill validation, audit script smoke, pressure eval script smoke
Conflict policy: reject or replan if generated eval files overlap with runtime scripts in incompatible ways

## Five Phase Contract

- Discovery: inspect real product signals before proposing work.
- Handoff: choose one execution batch with one or more bounded lanes, hypotheses, scopes, risks, owner boundaries, execution strategy, and worktree plan.
- Verification: accept only evidence-backed checks, including integrated verification after parallel agents.
- Persistence: update state, append the run log, update benchmark, and update handoff/worktree files.
- Scheduling: choose one next action: `stop_success`, `run_again_now`, `schedule`, `pause`, or `escalate`.

## Watchdog Scheduler

Commands: `watchdog.py setup`, `watchdog.py status`, `watchdog.py pause`, `watchdog.py resume`, `watchdog.py tail`, `watchdog.py uninstall`, `watchdog.py tick`
Status/logs: `.loop-harness/schedules/`
Process model: scheduled ticks are fresh processes that continue through `.loop-harness/*` state.
Overlap lock: schedule lock permits one active tick.
Scheduled run-until-done requirement: locked self criteria before actioning.

## Budget

See `self/loop-runs/product-loop-budget.md`.

## Run-Until-Done

Primary metric: pressure benchmark case score
Baseline window: current repository state before benchmark scaffold
Target: all critical pressure cases score `>=8/10`; latest run-log validator passes; engineering-quality skill-package benchmark selection is non-empty; target-repo criteria/current scaffold, split active benchmark storage, and watchdog scheduler semantics pass
Target minimum: 8/10
Iteration budget: until-done
Plateau patience: 3 iterations without meaningful improvement
Stop conditions: SUCCESS, EXHAUSTED, PLATEAU, REGRESSION, BUDGET, HUMAN_GATE, ENV, UNKNOWN

## Kill Switch

Pause when validation fails twice for the same root cause, scope expands beyond benchmark support, or installed skill sync diverges from source.
