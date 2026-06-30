# Product Loop Budget

Max runs per day:
Max iterations per opportunity: unset by default; run until done unless a safety budget or stop condition fires
Default plateau patience: 3 iterations without meaningful improvement
Max actioning changes per run:
Max verification-heavy checks per run:
Max tokens or wall time:
Kill switch:
Escalation owner/inbox:

## Rules

- Exit early when no actionable signal exists.
- Do not run actioning changes when a human gate is triggered.
- Stop run-until-done when success, explicit iteration cap, budget, plateau, regression, human gate, or environment blocker fires.
- Pause scheduled loops when budget is exceeded.
