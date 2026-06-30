# Product Loop Benchmark

Promote stable evidence from `product-loop-run-log.md` after each iteration.

## Known-Good Flows

### Flow Name

- Surface/URL:
- Playwright steps:
- Expected visible states:
- Assertions:
- Screenshot/trace evidence:
- Last verified:

## Regression Checks

- Check:
- Source run-log entry:
- Why it matters:

- Check: For visible UX/UI optimization, Playwright runtime evidence is not sufficient by itself; run `design-taste-frontend` when applicable and `design-slop-ban` for visible UI linting.
- Source run-log entry:
- Why it matters: future loops should not repeat visual regressions, generic UI patterns, inaccessible controls, text overflow, or broken responsive states after they have already been found.

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

- Metric:
- Baseline window:
- Baseline value:
- Source:

## Do Not Regress

- Rule:
- Evidence:

- Rule: Do not claim UX/UI visual-quality PASS without Playwright evidence when the surface can be opened, taste/slop score `>=8/10` when visual quality matters, and no critical slop violation.
- Evidence:
