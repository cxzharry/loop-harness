# Product Loop

Product surface:
Optimization goal:
Intent:
Pattern: daily-product-triage
Profiles: ux-product, engineering-quality
Readiness level: L1 report-only
Execution mode: report-only
Cadence:
Scheduler: watchdog.py
Scheduler state directory: schedules/

## Scope

Watched surfaces:
Non-goals:
Denylist:

## Human Gates

- Pricing, payment, auth, permissions, secrets.
- Destructive migrations or irreversible data changes.
- Legal/compliance/brand-sensitive decisions.
- Major product direction changes.

## Verification

Evaluation contract: criteria/current.md
Primary checks:
Metric/data sources:
Browser routes:
Playwright required for app verification: yes
Playwright smoke flows:
Test commands:

## Execution Orchestration

Execution strategy: single-agent
Batch planning required before actioning: yes
Batch types: single-lane | multi-lane | sequential | discovery-only
Lane decomposition fields: lane id, goal, allowed files/surfaces, dependencies, verification command, owner
Parallelization strategy:
Parallel agents allowed when domains are independent: yes
Agent handoff file: AGENT_HANDOFF.md
Agent task directory: agent-tasks/
Worktree isolation for file-changing parallel agents: yes
Worktree map: worktree-map.md
Integration verification:
Conflict policy:

## Five Phase Contract

- Discovery: inspect real product signals before proposing work.
- Handoff: choose one execution batch with one or more bounded lanes, hypotheses, scopes, risks, owner boundaries, execution strategy, and worktree plan.
- Verification: accept only evidence-backed checks, including integrated verification after parallel agents.
- Persistence: update state, append the run log, and update handoff/worktree files.
- Scheduling: stop, run again, schedule, pause, or escalate.

## Watchdog Scheduler

Commands: `watchdog.py setup`, `watchdog.py status`, `watchdog.py pause`, `watchdog.py resume`, `watchdog.py tail`, `watchdog.py uninstall`, `watchdog.py tick`
Status/logs: schedules/
Process model: each scheduled tick starts fresh and continues from persisted loop state.
Overlap lock: schedules/ lock file prevents concurrent ticks.
Scheduled run-until-done requirement: criteria/current.md has `Contract status: locked`.

## Budget

See `product-loop-budget.md`.

## Run-Until-Done

Primary metric:
Baseline window:
Target:
Target minimum:
Acceptance criteria: criteria/current.md
Benchmark seeds: criteria/current.md
Iteration budget: until-done
Plateau patience: 3 iterations without meaningful improvement
Stop conditions: SUCCESS, EXHAUSTED, PLATEAU, REGRESSION, BUDGET, HUMAN_GATE, ENV, UNKNOWN

## Kill Switch

Pause when budget is exceeded, repeated failures occur, or human gate is triggered.
