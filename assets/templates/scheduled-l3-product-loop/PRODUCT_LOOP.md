# Product Loop

Product surface:
Optimization goal:
Pattern: daily-product-triage
Profiles: ux-product, metrics-growth, engineering-quality
Readiness level: L3 scheduled/unattended-capable
Cadence:

## Scope

Watched surfaces:
Allowed automated actions:
Denylist:

## Five Phase Contract

- Discovery: early-exit when no actionable signal exists.
- Handoff: one bounded intervention per actioning run.
- Verification: independent evidence required before acceptance.
- Persistence: state and run log are mandatory every run.
- Scheduling: obey budget, kill switch, and human gates.

## Human Gates

- Pricing, payment, auth, permissions, secrets.
- Destructive migrations or irreversible data changes.
- Legal/compliance/brand-sensitive decisions.
- Major product direction changes.

## Budget

See `product-loop-budget.md`. Scheduled loops must pause when cap is exceeded.
