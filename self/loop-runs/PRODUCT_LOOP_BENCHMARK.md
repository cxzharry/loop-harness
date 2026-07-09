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
  - `product_loop_audit.py self/loop-runs --strict` exits 0.
  - `product_loop_audit.py assets/templates --min-level L2` exits 0 with no WARN/MISS.
  - `product_loop_audit.py assets/templates --strict` exits non-zero because templates are not scheduled/unattended run artifacts, not because of placeholder WARN noise.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T08:01:27Z

### Progressive Disclosure Entrypoint

- Surface/URL: `SKILL.md`, `references/operation.md`, `references/*.md`
- Playwright steps: not applicable
- Expected visible states: not applicable
- Assertions:
  - `SKILL.md` stays a concise entrypoint under 200 lines.
  - Detailed loop contract lives in one-level reference files linked directly from `SKILL.md`.
  - `references/operation.md` preserves intent, start run, execution modes, five phases, run-until-done, orchestration, benchmark promotion, and output report details.
  - `quick_validate.py`, self-loop audit, template audit, and pressure eval smoke still pass after the split.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T07:54:23Z

### Pressure Transcript Scoring

- Surface/URL: `benchmark/`
- Playwright steps: not applicable
- Expected visible states: not applicable
- Assertions:
  - `benchmark/run_pressure_eval.py` reads `benchmark/manifest.json`.
  - Missing transcripts fail rather than pass silently.
  - Committed pass fixtures under `benchmark/fixtures/pass` score 10/10 for every critical case.
  - Critical cases require score `>=8/10`.
  - Skipped or not-run required checks do not count as positive evidence.
  - Failed-iteration promotion transcripts must include filled Raw Run Result, Finding, and Benchmark Promotion sections.
- Screenshot/trace evidence: not applicable
- Last verified: 2026-06-30T08:01:27Z

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

- Check: `SKILL.md` must stay concise and route detailed behavior through direct one-level references.
- Source run-log entry: 2026-06-30T07:54:23Z
- Why it matters: loading the skill should preserve behavior without spending context on every detailed phase contract unless needed.

- Check: template audits should distinguish placeholder templates from real run artifacts.
- Source run-log entry: 2026-06-30T08:01:27Z
- Why it matters: `assets/templates` should validate cleanly as reusable scaffolding without pretending to have real state activity or run-log entries.

- Check: pressure eval smoke must use committed pass fixtures rather than untracked temporary transcripts.
- Source run-log entry: 2026-06-30T08:01:27Z
- Why it matters: benchmark validation must be reproducible across future runs and installed skill syncs.

- Check: target-repo loop artifacts must live under `.loop-harness/` and audit must auto-detect that folder from repo root.
- Source run-log entry: 2026-06-30T08:50:55Z
- Why it matters: product repos should not be polluted with loose loop artifact files, and users should not need to remember the artifact subfolder path for audit.

- Check: reusable cross-repo knowledge must be selected from `~/.codex/loop-harness/knowledge/` as a subset and promoted through a gate.
- Source run-log entry: 2026-06-30T10:02:11Z
- Why it matters: loop-harness should learn across local repos without bloating the skill package or promoting noisy repo-specific failures globally.

- Check: public release hygiene must be repeatable before GitHub publish.
- Source run-log entry: 2026-07-09T05:04:30Z
- Why it matters: a public skill repo needs README/LICENSE, generic installation docs, no personal absolute paths, no secret literals, and local cache/runtime ignores before push.

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

## Regression Case: skill-md-progressive-disclosure

- Source run-log entry: 2026-06-30T07:54:23Z
- Error class: scope_regression
- Surface/URL: `SKILL.md`, `references/operation.md`
- Trigger condition: changes inline detailed phase, orchestration, verification, persistence, or output contracts back into `SKILL.md` instead of routing through references.
- Playwright steps: not applicable
- Expected result: `SKILL.md` remains under 200 lines, references are linked directly, and source plus installed validation gates pass.
- Failure evidence: pre-optimization `SKILL.md` had 446 lines and duplicated details already suitable for progressive-disclosure references.
- Matching rule: any change to `SKILL.md`, `references/operation.md`, or reference routing.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-06-30T07:54:23Z pre-fix review
- Last passed: 2026-06-30T07:54:23Z
- Status: active

## Regression Case: template-placeholder-audit-no-warning

- Source run-log entry: 2026-06-30T08:01:27Z
- Error class: scope_regression
- Surface/URL: `scripts/product_loop_audit.py`, `assets/templates/`
- Trigger condition: auditing `assets/templates` reports placeholder-only state or run-log absence as `WARN`.
- Playwright steps: not applicable
- Expected result: `python3 scripts/product_loop_audit.py assets/templates --min-level L2` exits 0, scores 100/100 L2, and emits no WARN/MISS.
- Failure evidence: pre-fix template audit emitted `WARN no proven state activity` and `WARN no real run-log entries` for reusable scaffolding.
- Matching rule: any change to audit state/run-log activity checks or template artifact layout.
- Owner profile: engineering-quality
- Last failed: 2026-06-30T08:01:27Z pre-fix review
- Last passed: 2026-06-30T08:01:27Z
- Status: active

## Regression Case: committed-pressure-pass-fixtures

- Source run-log entry: 2026-06-30T08:01:27Z
- Error class: scope_regression
- Surface/URL: `benchmark/fixtures/pass`, `benchmark/run_pressure_eval.py`, `benchmark/manifest.json`
- Trigger condition: pressure eval smoke relies on missing, untracked, or temporary transcripts.
- Playwright steps: not applicable
- Expected result: `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass` exits 0 and scores 10/10 across all critical cases.
- Failure evidence: pre-fix validation used temporary synthetic transcripts, while the repository had no committed pass fixture directory.
- Matching rule: any change to pressure benchmark manifest, scorer, transcript fixture paths, or validation commands.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-06-30T08:01:27Z pre-fix review
- Last passed: 2026-06-30T08:01:27Z
- Status: active

## Regression Case: default-loop-artifact-root

- Source run-log entry: 2026-06-30T08:50:55Z
- Error class: scope_regression
- Surface/URL: `SKILL.md`, `references/operation.md`, `references/state-schema.md`, `references/verification.md`, `scripts/product_loop_audit.py`, `benchmark/manifest.json`
- Trigger condition: target-repo loop artifacts are documented, scaffolded, audited, or pressure-tested as loose root files instead of `.loop-harness/` files.
- Playwright steps: not applicable
- Expected result: target repos use `.loop-harness/` by default; `python3 scripts/product_loop_audit.py <repo-root> --min-level L2` auto-detects `<repo-root>/.loop-harness`; pressure fixtures require `.loop-harness/` persistence, handoff, agent-task, and worktree-map paths.
- Failure evidence: pre-fix repo-root audit returned `0/100 L0` for a temp repo with valid `.loop-harness/` artifacts; pressure fixtures mentioned artifact filenames without the `.loop-harness/` root.
- Matching rule: any change to artifact path conventions, scaffold instructions, audit root resolution, pressure persistence cases, handoff paths, or worktree-map paths.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-06-30T08:50:55Z pre-fix review
- Last passed: 2026-06-30T08:50:55Z
- Status: active

## Regression Case: global-local-knowledge-store

- Source run-log entry: 2026-06-30T10:02:11Z
- Error class: scope_regression
- Surface/URL: `SKILL.md`, `references/global-knowledge.md`, `references/operation.md`, `references/state-schema.md`, `scripts/select_knowledge.py`, `scripts/promote_global_knowledge.py`, `benchmark/manifest.json`
- Trigger condition: changes touch global knowledge selection, criteria packs, benchmark seeds, promotion gate, pressure cases, or persistence docs.
- Playwright steps: not applicable
- Expected result: `select_knowledge.py` returns only matching criteria/seeds by profile, intent, and surface; global seeds remain inactive without repo-local evidence; `promote_global_knowledge.py` writes candidates to inbox by default and requires gate plus explicit `--promote` before promoted knowledge.
- Failure evidence: pre-fix pressure eval failed `global_knowledge_selects_subset` and `global_promotion_requires_gate` at 0/10; no selector or promotion gate script existed.
- Matching rule: any change to global knowledge store paths, selector output, promotion gate, registry schema, pressure cases, or persistence instructions.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-06-30T10:02:11Z pre-fix pressure eval
- Last passed: 2026-06-30T10:02:11Z
- Status: active

## Regression Case: latest-run-log-validator-hard-gate

- Source run-log entry: 2026-07-09T03:27:48Z
- Error class: scope_regression
- Surface/URL: `scripts/product_loop_audit.py`, `scripts/validate_run_log_entry.py`, `self/loop-runs/product-loop-run-log.md`
- Trigger condition: a loop instance has an earlier structured run-log entry but the latest timestamped entry lacks `Raw Run Result`, `Finding`, or `Benchmark Promotion` sections.
- Playwright steps: not applicable
- Expected result: `product_loop_audit.py <loop-root> --min-level L3` exits non-zero and reports `MISS latest run-log entry invalid`.
- Failure evidence: pre-fix self-loop audit reported `100/100 L3` while `validate_run_log_entry.py self/loop-runs/product-loop-run-log.md` failed on the latest entry.
- Matching rule: any change to product-loop audit logic, run-log validation, self-development validation commands, or run-log schema.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-07-09T03:27:48Z pre-fix RED test
- Last passed: 2026-07-09T03:27:48Z
- Status: active

## Regression Case: skill-frontmatter-trigger-only

- Source run-log entry: 2026-07-09T03:27:48Z
- Error class: scope_regression
- Surface/URL: `SKILL.md`
- Trigger condition: skill frontmatter description starts with a what-it-does summary or includes workflow phrases such as prioritizing candidates, forming hypotheses, verifying evidence, persisting learnings, or scheduling the next loop.
- Playwright steps: not applicable
- Expected result: `SKILL.md` description starts with `Use when` and describes trigger contexts only.
- Failure evidence: pre-fix frontmatter began with `Autonomous product optimization loop harness...` and summarized workflow steps, which can cause agents to shortcut the skill body.
- Matching rule: any change to skill frontmatter, `agents/openai.yaml`, or trigger/discovery metadata.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-07-09T03:27:48Z pre-fix RED test
- Last passed: 2026-07-09T03:27:48Z
- Status: active

## Regression Case: canonical-scheduling-next-actions

- Source run-log entry: 2026-07-09T03:27:48Z
- Error class: scope_regression
- Surface/URL: `SKILL.md`, `references/operation.md`, `scripts/run_loop_controller.py`, `scripts/validate_run_log_entry.py`
- Trigger condition: scheduling output docs mix legacy values such as `NEXT_ITERATION` or `REPLAN` with runtime next-action values.
- Playwright steps: not applicable
- Expected result: scheduling docs use exactly one next action from `stop_success`, `run_again_now`, `schedule`, `pause`, or `escalate`; stop conditions remain separate from next actions.
- Failure evidence: pre-fix `references/operation.md` told agents to decide `SUCCESS`, `NEXT_ITERATION`, `REPLAN`, `PAUSE`, `ESCALATE`, or `STOP`, while scripts validated `stop_success` and `run_again_now`.
- Matching rule: any change to scheduling docs, run-until-done controller stop values, run-log validator, state schema, or output report shape.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-07-09T03:27:48Z pre-fix RED test
- Last passed: 2026-07-09T03:27:48Z
- Status: active

## Regression Case: skill-package-self-benchmark-selection

- Source run-log entry: 2026-07-09T03:27:48Z
- Error class: scope_regression
- Surface/URL: `benchmark/manifest.json`, `scripts/select_benchmarks.py`
- Trigger condition: selecting benchmarks for `--profile engineering-quality --intent ENGINEERING_QUALITY --surface skill-package --include-skill --require` returns zero cases.
- Playwright steps: not applicable
- Expected result: benchmark selection returns at least `strict_run_log_validator` for loop-harness self-development work.
- Failure evidence: pre-fix benchmark selection printed `Selected 0 benchmark case(s)` and returned exit code 1 for engineering-quality skill-package self-development.
- Matching rule: any change to skill-pressure manifest descriptions, benchmark selection tokenization, self-development surfaces, or validation commands.
- Owner profile: engineering-quality
- Last failed: 2026-07-09T03:27:48Z pre-fix RED test
- Last passed: 2026-07-09T03:27:48Z
- Status: active

## Regression Case: runtime-evaluation-contract-scaffold

- Source run-log entry: 2026-07-09T04:17:58Z
- Error class: scope_regression
- Surface/URL: `scripts/init_loop.py`, `assets/templates/criteria/current.md`, `SKILL.md`, `references/operation.md`, `references/state-schema.md`
- Trigger condition: target-repo scaffolding omits `.loop-harness/criteria/current.md` or actioning guidance does not require `Contract status: locked` before product changes.
- Playwright steps: not applicable
- Expected result: scaffold creates `.loop-harness/criteria/current.md`; docs require locked metric/rubric, acceptance criteria, benchmark seeds, target, evidence source, and Playwright flow when applicable before actioning.
- Failure evidence: pre-fix scaffold created no repo-local runtime criteria contract, so criteria could be mistaken for package-level templates only.
- Matching rule: any change to scaffold files, criteria templates, start checklist, operation contract, state schema, or pre-action loop requirements.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-07-09T04:17:58Z pre-fix RED test
- Last passed: 2026-07-09T04:17:58Z
- Status: active

## Regression Case: split-active-benchmark-files

- Source run-log entry: 2026-07-09T04:17:58Z
- Error class: scope_regression
- Surface/URL: `scripts/select_benchmarks.py`, `scripts/product_loop_audit.py`, `assets/templates/PRODUCT_LOOP_BENCHMARK.md`
- Trigger condition: repo-local active regression cases are stored in `.loop-harness/benchmarks/active/*.md` but selector or audit only reads `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`.
- Playwright steps: not applicable
- Expected result: selector and audit read compact benchmark index plus active split case files; archive files under `benchmarks/archive/` are ignored for active blocking.
- Failure evidence: pre-fix selector parsed only `PRODUCT_LOOP_BENCHMARK.md`, so a split active case did not block forward optimization.
- Matching rule: any change to benchmark selector, audit active-case parsing, benchmark template, archive retention docs, or runtime artifact layout.
- Owner profile: engineering-quality
- Last failed: 2026-07-09T04:17:58Z pre-fix RED test
- Last passed: 2026-07-09T04:17:58Z
- Status: active

## Regression Case: compact-benchmark-index-controller-promotion

- Source run-log entry: 2026-07-09T04:17:58Z
- Error class: scope_regression
- Surface/URL: `scripts/run_loop_controller.py`, `assets/templates/PRODUCT_LOOP_BENCHMARK.md`
- Trigger condition: command-backed controller promotes a terminal failure by appending the full regression case into `PRODUCT_LOOP_BENCHMARK.md` when `benchmarks/active/` exists.
- Playwright steps: not applicable
- Expected result: controller writes the full active case to `benchmarks/active/<case-id>.md` and appends only compact index metadata to `PRODUCT_LOOP_BENCHMARK.md`.
- Failure evidence: pre-fix controller appended every promoted case directly to `PRODUCT_LOOP_BENCHMARK.md`, making the file grow without a scale boundary.
- Matching rule: any change to controller promotion, benchmark index template, active split directory creation, or run-log benchmark promotion path.
- Owner profile: engineering-quality
- Last failed: 2026-07-09T04:17:58Z pre-fix RED test
- Last passed: 2026-07-09T04:17:58Z
- Status: active

## Regression Case: self-pressure-coverage-scale-contract

- Source run-log entry: 2026-07-09T04:17:58Z
- Error class: scope_regression
- Surface/URL: `benchmark/manifest.json`, `benchmark/fixtures/pass`, `benchmark/cases/`
- Trigger condition: pressure suite lacks cases or committed pass fixtures for evaluation-contract-before-action, split active benchmark files, scaffold runtime criteria dirs, or self skill-package benchmark selection.
- Playwright steps: not applicable
- Expected result: `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass` includes these behaviors and scores 10/10.
- Failure evidence: pre-fix pressure selection for `evaluation_contract_before_action` returned `No cases selected`, and split active benchmark behavior had no committed fixture coverage.
- Matching rule: any change to pressure manifest, pressure fixtures, case docs, or self-development validation commands.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-07-09T04:17:58Z pre-fix RED test
- Last passed: 2026-07-09T04:17:58Z
- Status: active

## Metric Baselines

## Regression Case: watchdog-scheduler-lifecycle-semantics

- Source run-log entry: 2026-07-09T04:45:18Z
- Error class: scope_regression
- Surface/URL: `SKILL.md`, `references/operation.md`, `references/state-schema.md`, `assets/templates/PRODUCT_LOOP.md`, `assets/templates/PRODUCT_LOOP_STATE.md`, `assets/templates/product-loop-budget.md`, `self/loop-runs/`
- Trigger condition: docs/templates describe scheduled loops without the watchdog command lifecycle, persisted-state process model, criteria lock requirement, overlap lock, or `.loop-harness/schedules/` status/log path.
- Playwright steps: outside_scope for skill-package docs
- Expected result: docs/templates list `watchdog.py setup/status/pause/resume/tail/uninstall/tick`; scheduled ticks start fresh and continue through `.loop-harness/*`; `run-until-done` uses locked criteria; the lock serializes ticks; status/logs live under `.loop-harness/schedules/`.
- Failure evidence: watchdog semantics needed user-facing documentation and self-loop persistence coverage.
- Matching rule: any change to scheduling docs, scheduler templates, state schema, budget template, self-loop state/run-log/benchmark artifacts, or watchdog command names.
- Owner profile: engineering-quality, content-docs
- Last failed: 2026-07-09T04:45:18Z pre-documentation gap
- Last passed: 2026-07-09T04:45:18Z
- Status: active

## Regression Case: public-release-hygiene

- Source run-log entry: 2026-07-09T05:04:30Z
- Error class: scope_regression
- Surface/URL: `README.md`, `LICENSE`, `.gitignore`, `SKILL.md`, `benchmark/test_tooling_regressions.py`, `self/loop-runs/`
- Trigger condition: repository is prepared for public GitHub release without README/LICENSE, with personal absolute local paths, with token/API-key literals in text files, with watchdog docs implying automatic OS scheduler installation, or without ignores for local caches/runtime artifacts.
- Playwright steps: not applicable
- Expected result: `test_public_release_hygiene_has_docs_and_no_local_paths` passes; README uses `$loop-harness` examples and says watchdog does not automatically install OS scheduler jobs; public text files contain no absolute local user paths, local username, GitHub token, OpenAI-style secret, API-key assignment, password assignment, or token assignment literals.
- Failure evidence: public readiness review found missing README/LICENSE, no remote, local absolute paths in self artifacts, and local generated cache risk before release cleanup.
- Matching rule: any change to README, LICENSE, `.gitignore`, skill validation docs, self-loop artifacts, public release workflow, or token/path scanning patterns.
- Owner profile: engineering-quality, content-docs, release-readiness
- Last failed: 2026-07-09T05:04:30Z pre-test RED guard did not exist
- Last passed: 2026-07-09T05:04:30Z
- Status: active

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

- Rule: Keep `SKILL.md` as a concise entrypoint and move detailed operational contracts into directly linked reference files.
- Evidence: `SKILL.md`, `references/operation.md`

- Rule: Keep `assets/templates` placeholder audits free of WARN/MISS while preserving L3 only for artifacts with real run activity.
- Evidence: `scripts/product_loop_audit.py`, `assets/templates/`

- Rule: Keep committed pressure pass fixtures aligned with every critical manifest case.
- Evidence: `benchmark/fixtures/pass`, `benchmark/manifest.json`, `benchmark/run_pressure_eval.py`

- Rule: Target repos use `.loop-harness/` as the default loop artifact root; do not scatter loop artifacts at repo root.
- Evidence: `SKILL.md`, `references/state-schema.md`, `references/operation.md`

- Rule: Audit accepts either `.loop-harness/` directly or the repo root containing `.loop-harness/`.
- Evidence: `scripts/product_loop_audit.py`

- Rule: Runtime learning must not be written into the skill package; reusable cross-repo knowledge belongs in `~/.codex/loop-harness/knowledge/` and goes through an inbox/gate.
- Evidence: `references/global-knowledge.md`, `scripts/select_knowledge.py`, `scripts/promote_global_knowledge.py`

- Rule: L3 audit must fail when the latest run-log entry fails `validate_run_log_entry.py`.
- Evidence: `scripts/product_loop_audit.py`, `scripts/validate_run_log_entry.py`, `benchmark/test_tooling_regressions.py`

- Rule: Skill frontmatter descriptions must be trigger-only and start with `Use when`.
- Evidence: `SKILL.md`, `benchmark/test_tooling_regressions.py`

- Rule: Scheduling next actions are `stop_success`, `run_again_now`, `schedule`, `pause`, or `escalate`; do not mix them with stop-condition enum names.
- Evidence: `SKILL.md`, `references/operation.md`, `scripts/run_loop_controller.py`

- Rule: Loop-harness self-development under `engineering-quality` and `skill-package` must select a matching benchmark before actioning.
- Evidence: `benchmark/manifest.json`, `scripts/select_benchmarks.py`, `benchmark/test_tooling_regressions.py`

- Rule: Target-repo actioning must be gated by a locked repo-local evaluation contract at `.loop-harness/criteria/current.md`.
- Evidence: `assets/templates/criteria/current.md`, `scripts/init_loop.py`, `references/operation.md`, `benchmark/manifest.json`

- Rule: Active benchmark cases may scale into `benchmarks/active/*.md`; selectors and audits must ignore archived cases under `benchmarks/archive/`.
- Evidence: `scripts/select_benchmarks.py`, `scripts/product_loop_audit.py`, `benchmark/test_tooling_regressions.py`

- Rule: Keep `PRODUCT_LOOP_BENCHMARK.md` as a compact active index when split active files exist.
- Evidence: `scripts/run_loop_controller.py`, `assets/templates/PRODUCT_LOOP_BENCHMARK.md`, `references/state-schema.md`

- Rule: Watchdog scheduler docs must cover `setup/status/pause/resume/tail/uninstall/tick`, `.loop-harness/schedules/`, persisted-state continuation, locked criteria for `run-until-done`, and the overlap lock.
- Evidence: `SKILL.md`, `references/operation.md`, `references/state-schema.md`, `assets/templates/`

- Rule: Public release hygiene must keep README/LICENSE present, avoid personal absolute paths and secret literals in public text files, and keep local cache/runtime artifacts ignored.
- Evidence: `README.md`, `LICENSE`, `.gitignore`, `benchmark/test_tooling_regressions.py`
