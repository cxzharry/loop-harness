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
  - `product_loop_audit.py self/loop-runs --min-level L3` exits 0.
  - `product_loop_audit.py assets/templates --min-level L2` exits 0.
  - `product_loop_audit.py assets/templates --strict` exits non-zero while template artifacts have warnings.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T07:45:29Z

### Pressure Transcript Scoring

- Surface/URL: `benchmark/`
- Playwright steps: not applicable
- Expected visible states: not applicable
- Assertions:
  - `benchmark/run_pressure_eval.py` reads `benchmark/manifest.json`.
  - Missing transcripts fail rather than pass silently.
  - Critical cases require score `>=8/10`.
  - Skipped or not-run required checks do not count as positive evidence.
  - Failed-iteration promotion transcripts must include filled Raw Run Result, Finding, and Benchmark Promotion sections.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T07:17:26Z

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

- Check: Each loop context has one active `product-loop-run-log.md`; raw errors, findings, and benchmark promotion decisions are recorded inside the same run-log entry.
- Source run-log entry: 2026-06-30T07:04:04Z
- Why it matters: separate error-log or findings files make promotion provenance harder to audit and can split the evidence chain.

- Check: Benchmark and artifact audit scoring must reject skipped/not-run checks, negated evidence, and unfilled structured fields.
- Source run-log entry: 2026-06-30T07:17:26Z
- Why it matters: loop-harness can only prevent regressions if its benchmarks distinguish real verification from superficial text mentions.

- Check: Product-loop audit hard misses must return non-zero exit codes, not only lower readiness levels in stdout.
- Source run-log entry: 2026-06-30T07:45:29Z
- Why it matters: automated gates and CI rely on exit codes; a hard miss with exit 0 lets regressions pass silently.

## Regression Cases

## Regression Case: ux-skipped-taste-slop-must-fail

- Source run-log entry: 2026-06-30T07:17:26Z
- Error class: scope_regression
- Surface/URL: `benchmark/run_pressure_eval.py`, `benchmark/manifest.json`
- Trigger condition: transcript for UX/UI visual-quality work says `design-taste-frontend` or `design-slop-ban` was skipped, not run, omitted, bypassed, or not applied.
- Playwright steps: not applicable
- Expected result: `ux_requires_taste_slop_benchmark` fails and reports forbidden skipped/not-run evidence.
- Failure evidence: pre-fix scoring could count a skipped taste/slop mention as satisfying required patterns.
- Matching rule: any change to UX/UI benchmark manifest patterns or pressure scoring evidence matching.
- Owner profile: engineering-quality, ux-product
- Last failed: 2026-06-30T07:17:26Z pre-fix review
- Last passed: 2026-06-30T07:17:26Z
- Status: active

## Regression Case: negated-artifact-evidence-caps-readiness

- Source run-log entry: 2026-06-30T07:17:26Z
- Error class: scope_regression
- Surface/URL: `scripts/product_loop_audit.py`
- Trigger condition: target artifacts include claims such as `No human gate`, `Playwright not run`, `No finding`, `Benchmark Promotion not filled`, or `Integration verification not executed`.
- Playwright steps: not applicable
- Expected result: audit reports `MISS negated evidence claims present` and caps readiness below passing level.
- Failure evidence: pre-fix audit could treat negated text as positive field coverage.
- Matching rule: any change to product-loop audit field matching, scoring caps, or evidence parsing.
- Owner profile: engineering-quality
- Last failed: 2026-06-30T07:17:26Z pre-fix review
- Last passed: 2026-06-30T07:17:26Z
- Status: active

## Regression Case: failed-iteration-promotion-requires-filled-sections

- Source run-log entry: 2026-06-30T07:17:26Z
- Error class: scope_regression
- Surface/URL: `benchmark/manifest.json`, `benchmark/run_pressure_eval.py`
- Trigger condition: failed-iteration promotion transcript mentions finding or promotion words but lacks filled `Raw Run Result`, `Finding`, or `Benchmark Promotion` fields.
- Playwright steps: not applicable
- Expected result: `failed_iteration_promotes_benchmark` fails with missing section or field messages.
- Failure evidence: pre-fix benchmark could pass from word presence without durable field completion.
- Matching rule: any change to failed-iteration promotion benchmark case, manifest schema, or pressure scorer section parsing.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-06-30T07:17:26Z pre-fix review
- Last passed: 2026-06-30T07:17:26Z
- Status: active

## Regression Case: audit-hard-miss-exit-gate

- Source run-log entry: 2026-06-30T07:45:29Z
- Error class: scope_regression
- Surface/URL: `scripts/product_loop_audit.py`
- Trigger condition: audit output contains hard misses such as `MISS negated evidence claims present` or failed iterations without active promoted regression cases.
- Playwright steps: not applicable
- Expected result: audit returns non-zero exit code; `--min-level` fails below the requested level; `--strict` fails on any warning or miss; `non-zero` does not count as a `no ... finding` negated-evidence claim.
- Failure evidence: pre-fix negated evidence fixture returned `Product Loop Readiness: 59/100 L1` with `MISS negated evidence claims present: 1` and exit code 0.
- Matching rule: any change to product-loop audit exit-code logic, readiness thresholding, strict mode, hard-miss detection, or validation commands.
- Owner profile: engineering-quality
- Last failed: 2026-06-30T07:45:29Z pre-fix review
- Last passed: 2026-06-30T07:45:29Z
- Status: active

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

- Rule: Do not create separate `error-log.md`, `findings.md`, or `run-log-error.md`; keep Raw Run Result, Finding, and Benchmark Promotion in `product-loop-run-log.md`.
- Evidence: `SKILL.md`, `references/state-schema.md`, `assets/templates/product-loop-run-log.template.md`

- Rule: Do not let `product_loop_audit.py` return exit code 0 for hard misses such as negated evidence or missing promoted active regression cases.
- Evidence: `scripts/product_loop_audit.py`, `self/loop-runs/product-loop-run-log.md`

- Rule: Do not match `no` inside longer words such as `non-zero` when detecting negated evidence.
- Evidence: `scripts/product_loop_audit.py`, `self/loop-runs/product-loop-run-log.md`
