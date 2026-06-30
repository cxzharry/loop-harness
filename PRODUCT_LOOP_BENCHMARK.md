# Product Loop Benchmark

Promote stable evidence from `product-loop-run-log.md` after each iteration.

## Known-Good Flows

### Static Skill Validation

- Surface/URL: loop-harness skill package
- Playwright steps: not applicable
- Expected visible states: not applicable
- Assertions:
  - `quick_validate.py` passes for source and installed skill.
  - `product_loop_audit.py` compiles.
  - `product_loop_cost.py` compiles.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T04:53:51Z

### Pressure Transcript Scoring

- Surface/URL: `evals/`
- Playwright steps: not applicable
- Expected visible states: not applicable
- Assertions:
  - `evals/run_pressure_eval.py` reads `evals/manifest.json`.
  - Missing transcripts fail rather than pass silently.
  - Critical cases require score `>=8/10`.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T04:53:51Z

## Regression Checks

- Check: pressure eval cases exist for metric gate, Playwright gate, fail-to-benchmark promotion, active benchmark blocking, parallel agents, and worktree isolation.
- Source run-log entry: 2026-06-30T04:53:51Z
- Why it matters: these are the critical behavior failures that make loop-harness unsafe for autonomous optimization.

## Regression Cases

## Regression Case: sample-case-id

- Source run-log entry:
- Error class: ui_regression | runtime_error | metric_regression | content_drift | env_blocker | scope_regression
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

## Metric Baselines

- Metric: pressure benchmark case score
- Baseline window: before `evals/` scaffold
- Baseline value: no behavior benchmark suite
- Source: repository inspection

## Do Not Regress

- Rule: Do not remove or weaken critical pressure benchmark cases without replacing them with equivalent behavior coverage.
- Evidence: `evals/manifest.json`
