# Product Loop

Product surface: loop-harness skill package
Optimization goal: make loop-harness self-evaluable through pressure-test behavior benchmarks
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
- `benchmark/`

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

Primary checks:
- `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py`
- `python3 scripts/product_loop_audit.py self/loop-runs`
- `python3 scripts/product_loop_audit.py assets/templates`
- `python3 benchmark/run_pressure_eval.py --transcripts <real-transcript-dir>`
- `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`

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
Parallel agents allowed when domains are independent: yes
Agent handoff file: self/loop-runs/AGENT_HANDOFF.md
Agent task directory: agent-tasks/
Worktree isolation for file-changing parallel agents: yes
Worktree map: self/loop-runs/worktree-map.md
Integration verification: source validation, installed skill validation, audit script smoke, pressure eval script smoke
Conflict policy: reject or replan if generated eval files overlap with runtime scripts in incompatible ways

## Five Phase Contract

- Discovery: inspect real product signals before proposing work.
- Handoff: choose one bounded intervention with hypothesis, scope, risk, owner boundary, execution strategy, and worktree plan.
- Verification: accept only evidence-backed checks, including integrated verification after parallel agents.
- Persistence: update state, append the run log, update benchmark, and update handoff/worktree files.
- Scheduling: stop, run again, schedule, pause, or escalate.

## Budget

See `self/loop-runs/product-loop-budget.md`.

## Run-Until-Done

Primary metric: pressure benchmark case score
Baseline window: current repository state before benchmark scaffold
Target: all critical pressure cases score `>=8/10`
Target minimum: 8/10
Iteration budget: until-done
Plateau patience: 3 iterations without meaningful improvement
Stop conditions: SUCCESS, EXHAUSTED, PLATEAU, REGRESSION, BUDGET, HUMAN_GATE, ENV, UNKNOWN

## Kill Switch

Pause when validation fails twice for the same root cause, scope expands beyond benchmark support, or installed skill sync diverges from source.
