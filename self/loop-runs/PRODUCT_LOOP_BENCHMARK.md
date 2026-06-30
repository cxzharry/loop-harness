# Product Loop Benchmark

Promote stable evidence from `self/loop-runs/product-loop-run-log.md` after each iteration.

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

- Surface/URL: `benchmark/`
- Playwright steps: not applicable
- Expected visible states: not applicable
- Assertions:
  - `benchmark/run_pressure_eval.py` reads `benchmark/manifest.json`.
  - Missing transcripts fail rather than pass silently.
  - Critical cases require score `>=8/10`.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T04:53:51Z

## Regression Checks

- Check: pressure eval cases exist for metric gate, Playwright gate, fail-to-benchmark promotion, active benchmark blocking, parallel agents, and worktree isolation.
- Source run-log entry: 2026-06-30T04:53:51Z
- Why it matters: these are the critical behavior failures that make loop-harness unsafe for autonomous optimization.

- Check: UX/UI visual optimization must combine Playwright runtime evidence with `design-taste-frontend` and `design-slop-ban`; passing requires taste/slop score `>=8/10` and no critical slop violation.
- Source run-log entry: 2026-06-30T05:20:25Z
- Why it matters: browser smoke alone can miss generic, inaccessible, or visually regressed UI; the loop must block those regressions before optimizing forward.

- Check: Skill self-eval criteria live under `benchmark/`, and self-run loop artifacts live under `self/loop-runs/`; package root stays limited to runtime skill resources.
- Source run-log entry: 2026-06-30T05:29:01Z
- Why it matters: keeping benchmarks and logs separate prevents agents from confusing loop-harness self-development artifacts with target-repo loop artifacts.

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
- Baseline window: before `benchmark/` scaffold
- Baseline value: no behavior benchmark suite
- Source: repository inspection

## Do Not Regress

- Rule: Do not remove or weaken critical pressure benchmark cases without replacing them with equivalent behavior coverage.
- Evidence: `benchmark/manifest.json`

- Rule: Do not claim UX/UI visual-quality PASS from Playwright alone when visual quality matters; run the combined taste/slop benchmark or record a justified non-applicability reason with equivalent checks.
- Evidence: `references/verification.md`, `benchmark/manifest.json`, `benchmark/cases/ux_requires_taste_slop_benchmark.md`

- Rule: Do not place `PRODUCT_LOOP*.md`, `product-loop-*.md`, `AGENT_HANDOFF.md`, or `worktree-map.md` at the skill package root for self-development runs.
- Evidence: `self/loop-runs/`, `benchmark/`, `SKILL.md`
