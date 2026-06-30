# Product Loop

Product surface:
Optimization goal:
Pattern: daily-product-triage
Profiles: ux-product, engineering-quality
Readiness level: L1 report-only
Execution mode: report-only
Cadence:

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

Primary checks:
Metric/data sources:
Browser routes:
Test commands:

## Five Phase Contract

- Discovery: inspect real product signals before proposing work.
- Handoff: choose one bounded intervention with hypothesis, scope, risk, and owner boundary.
- Verification: accept only evidence-backed checks.
- Persistence: update state and append the run log.
- Scheduling: stop, run again, schedule, pause, or escalate.

## Budget

See `product-loop-budget.md`.

## Run-Until-Done

Target:
Target minimum:
Max iterations:
Stop conditions: SUCCESS, EXHAUSTED, PLATEAU, REGRESSION, BUDGET, HUMAN_GATE, ENV, UNKNOWN

## Kill Switch

Pause when budget is exceeded, repeated failures occur, or human gate is triggered.
