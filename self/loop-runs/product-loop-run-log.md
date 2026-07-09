# Product Loop Run Log

Append one entry per loop run.

## Entries

### 2026-06-30T10:02:11Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals:
  - User wanted a local-first mechanism where general reusable findings or benchmarks can be promoted outside repos only when they are truly reusable.
  - Existing loop-harness had repo-local `.loop-harness/` persistence but no reader for `~/.codex/loop-harness/knowledge/`.
  - RED pressure eval failed two new cases: global subset selection and gated global promotion.
- Handoff:
  - Add `scripts/select_knowledge.py` to select matching global/local criteria by profile, intent, and surface without loading the whole store.
  - Add `scripts/promote_global_knowledge.py` to gate repo-local findings before writing candidates to `~/.codex/loop-harness/knowledge/inbox/`.
  - Add `references/global-knowledge.md` as the one-level reference, keeping `SKILL.md` concise.
  - Add pressure cases so future changes cannot promote noise or activate global seeds without repo-local evidence.
- Selected intervention: global local knowledge selector and promotion gate.
- Execution strategy: single-agent
- Agent tasks: global-local-knowledge-store
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source validation complete before installed sync
- Verification evidence:
  - RED: pressure eval failed `global_knowledge_selects_subset` and `global_promotion_requires_gate` at 0/10 before fixtures/contract.
  - GREEN: `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass` passed 9/9 cases at 10/10.
  - `python3 scripts/select_knowledge.py --repo <skill-source> --profile ux-product --intent UX_OPTIMIZE --surface web-route` returned subset matching with built-in fallback criteria and benchmark seeds.
  - `python3 scripts/promote_global_knowledge.py --repo self/loop-runs --dry-run` returned a gated candidate and wrote nothing.
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py scripts/select_knowledge.py scripts/promote_global_knowledge.py benchmark/run_pressure_eval.py` passed.
  - `python3 scripts/product_loop_audit.py self/loop-runs --strict` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates --min-level L2` passed at 100/100 L2.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `git diff --check` passed.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Error output: none after implementation
- Failed assertions: none after implementation
- Verdict: PASS
- Files changed:
  - `SKILL.md`
  - `references/operation.md`
  - `references/state-schema.md`
  - `references/global-knowledge.md`
  - `scripts/select_knowledge.py`
  - `scripts/promote_global_knowledge.py`
  - `benchmark/manifest.json`
  - `benchmark/cases/global_knowledge_selects_subset.md`
  - `benchmark/cases/global_promotion_requires_gate.md`
  - `benchmark/fixtures/pass/global_knowledge_selects_subset.md`
  - `benchmark/fixtures/pass/global_promotion_requires_gate.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
  - `self/loop-runs/product-loop-run-log.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-06-30-global-local-knowledge-store
- Error class: scope_regression
- Symptom: loop-harness had repo-local learning but no controlled path for reusable cross-repo criteria or benchmark seeds.
- Evidence: the package lacked `select_knowledge.py`, `promote_global_knowledge.py`, and `references/global-knowledge.md`; pressure tests for global selection/promotion failed before the change.
- Root cause/hypothesis: previous iterations correctly avoided skill-package bloat but did not add the local global store reader and promotion gate needed to reuse general knowledge safely.
- Reproduction steps: ask loop-harness to reuse `~/.codex/loop-harness/knowledge/` or promote a finding globally; before this change there was no script or contract to do it.
- Severity: medium
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: global-local-knowledge-store
- Matching rule: changes touch global knowledge selection, criteria packs, benchmark seeds, promotion gate, pressure cases, or persistence docs.
- Expected result: global local knowledge is selected as a profile/intent/surface subset; global seeds stay inactive without repo-local evidence; promotion writes candidates to inbox and requires gate plus explicit `--promote` before promoted knowledge.
- Verification command: `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass`, `python3 scripts/select_knowledge.py ...`, and `python3 scripts/promote_global_knowledge.py --repo <repo> --dry-run`
- Status: active
- State promoted: local global knowledge store contract at `~/.codex/loop-harness/knowledge/`.
- Benchmark promoted: active regression case for global subset selection and gated global promotion.

### 2026-06-30T08:50:55Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals:
  - User approved standardizing loop artifacts into a dedicated folder instead of scattering `PRODUCT_LOOP*`, run-log, benchmark, budget, handoff, and worktree files at repo root.
  - RED test: a temp repo containing `.loop-harness/` artifacts failed when auditing the repo root because `product_loop_audit.py` only read direct root artifacts.
  - Existing pressure benchmarks mentioned artifact filenames without enforcing the `.loop-harness/` artifact root.
- Handoff:
  - Use `.loop-harness/` as the default artifact root in target repos.
  - Keep `self/loop-runs/` as the internal exception for loop-harness self-development.
  - Make `product_loop_audit.py <repo-root>` auto-detect `<repo-root>/.loop-harness`.
  - Update pressure benchmarks and pass fixtures so durable persistence paths include `.loop-harness/`.
- Selected intervention: default loop artifact root plus repo-root audit auto-discovery.
- Execution strategy: single-agent
- Agent tasks: default-loop-artifact-root
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source validation complete before installed sync
- Verification evidence:
  - RED: temp repo with `.loop-harness/` artifacts returned `Product Loop Readiness: 0/100 L0` when audited at repo root.
  - GREEN: temp repo with `.loop-harness/` artifacts returned `Product Loop Readiness: 87/100 L2` with no WARN/MISS when audited at repo root.
  - `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass` passed 7/7 cases at 10/10 with `.loop-harness/` path requirements.
  - `python3 scripts/product_loop_audit.py self/loop-runs --strict` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates --min-level L2` passed at 100/100 L2.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Error output: pre-fix audit missed `.loop-harness/` when called with the product repo root.
- Failed assertions: repo-root audit should discover `.loop-harness/`; target-repo persistence should not be scattered at root.
- Verdict: PASS
- Files changed:
  - `SKILL.md`
  - `references/operation.md`
  - `references/state-schema.md`
  - `references/verification.md`
  - `references/scoring.md`
  - `scripts/product_loop_audit.py`
  - `benchmark/manifest.json`
  - `benchmark/cases/active_benchmark_blocks_forward.md`
  - `benchmark/cases/failed_iteration_promotes_benchmark.md`
  - `benchmark/cases/parallel_agents_independent.md`
  - `benchmark/cases/ux_requires_taste_slop_benchmark.md`
  - `benchmark/cases/worktree_isolation.md`
  - `benchmark/fixtures/pass/active_benchmark_blocks_forward.md`
  - `benchmark/fixtures/pass/failed_iteration_promotes_benchmark.md`
  - `benchmark/fixtures/pass/parallel_agents_independent.md`
  - `benchmark/fixtures/pass/worktree_isolation.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
  - `self/loop-runs/product-loop-run-log.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-06-30-default-loop-artifact-root
- Error class: scope_regression
- Symptom: target-repo loop artifacts would be scaffolded/read as loose root files, and repo-root audit did not discover a dedicated `.loop-harness/` artifact directory.
- Evidence: pre-fix temp repo with `.loop-harness/` artifacts audited at repo root returned `0/100 L0`; pressure benchmark fixtures did not require `.loop-harness/` persistence paths.
- Root cause/hypothesis: early artifacts were optimized for quick scaffolding, then self-development moved to `self/loop-runs/` without defining the equivalent target-repo artifact root.
- Reproduction steps: create a temp repo, place valid loop artifacts in `.loop-harness/`, run `python3 scripts/product_loop_audit.py <repo-root> --min-level L2`.
- Severity: medium
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: default-loop-artifact-root
- Matching rule: changes touch artifact path conventions, scaffold instructions, audit root resolution, pressure persistence cases, handoff paths, or worktree map paths.
- Expected result: target repos use `.loop-harness/` by default; repo-root audit auto-detects `.loop-harness/`; pressure fixtures require `.loop-harness/` paths for run-log, state, benchmark, handoff, agent tasks, and worktree map.
- Verification command: temp repo `.loop-harness/` audit smoke plus `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass`
- Status: active
- State promoted: `.loop-harness/` is the default target-repo artifact root.
- Benchmark promoted: active regression case for artifact-root convention and repo-root audit auto-discovery.

### 2026-06-30T08:01:27Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals:
  - User asked `$loop-harness` to fix `$loop-harness` until benchmarks are satisfied and no findings remain.
  - `python3 scripts/product_loop_audit.py self/loop-runs --strict` already passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates --strict` failed because template placeholders emitted warning-level findings for no state activity and no run-log entries.
  - `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass` failed because no committed pass fixture directory existed.
- Handoff:
  - Keep self-run artifact gates strict.
  - Treat `assets/templates` as reusable scaffolding rather than a real loop run.
  - Add committed pass transcripts for every critical pressure case so benchmark smoke is reproducible.
- Selected intervention: template-placeholder audit semantics plus committed pressure pass fixtures.
- Execution strategy: single-agent
- Agent tasks: audit-template-placeholder-no-warning, committed-pressure-pass-fixtures
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source validation complete before installed sync
- Verification evidence:
  - `python3 scripts/product_loop_audit.py self/loop-runs --strict` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates --min-level L2` passed at 100/100 L2 and emitted no WARN/MISS.
  - `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass` passed 7/7 cases at 10/10.
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py` passed.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `git diff --check` passed.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Error output: pre-fix template audit emitted warning findings for expected placeholders; pressure smoke had no committed fixture transcripts.
- Failed assertions: reusable templates should not emit warning findings for placeholder-only state/log; pressure smoke should run from committed fixtures.
- Verdict: PASS
- Files changed:
  - `scripts/product_loop_audit.py`
  - `benchmark/fixtures/pass/active_benchmark_blocks_forward.md`
  - `benchmark/fixtures/pass/failed_iteration_promotes_benchmark.md`
  - `benchmark/fixtures/pass/missing_metric_run_until_done.md`
  - `benchmark/fixtures/pass/parallel_agents_independent.md`
  - `benchmark/fixtures/pass/ui_requires_playwright.md`
  - `benchmark/fixtures/pass/ux_requires_taste_slop_benchmark.md`
  - `benchmark/fixtures/pass/worktree_isolation.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
  - `self/loop-runs/product-loop-run-log.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-06-30-template-and-pressure-fixtures
- Error class: scope_regression
- Symptom: template audit produced warning findings for intentional placeholders, and pressure benchmark smoke depended on untracked temporary transcripts.
- Evidence: pre-fix `assets/templates --strict` failed from placeholder warnings; pre-fix repository had no committed `benchmark/fixtures/pass` transcripts.
- Root cause/hypothesis: audit did not distinguish template artifact roots from real loop-run roots, and earlier pressure smoke validation used generated tmpdir transcripts that were not retained.
- Reproduction steps: run `python3 scripts/product_loop_audit.py assets/templates --min-level L2` and inspect warnings; run `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass` before fixtures exist.
- Severity: medium
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: template-placeholder-audit-no-warning, committed-pressure-pass-fixtures
- Matching rule: changes touch `scripts/product_loop_audit.py`, `assets/templates/`, `benchmark/manifest.json`, `benchmark/run_pressure_eval.py`, or `benchmark/fixtures/pass`.
- Expected result: template audits at L2 emit no WARN/MISS for placeholders; pressure pass fixtures score 10/10 across all critical cases.
- Verification command: `python3 scripts/product_loop_audit.py assets/templates --min-level L2` and `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass`
- Status: active
- State promoted: template-placeholder audit semantics and committed pass fixtures.
- Benchmark promoted: two active regression cases for template warning noise and pressure fixture reproducibility.

### 2026-06-30T07:54:23Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals:
  - User observed `SKILL.md` was long and asked to optimize it with `skill-creator` while preserving full functionality.
  - `wc -l` showed `SKILL.md` at 446 lines.
  - Existing `references/` already held profiles, patterns, scoring, verification, state schema, and failure modes, so progressive disclosure was the right packaging strategy.
- Handoff:
  - Keep `SKILL.md` as a concise trigger-time entrypoint.
  - Move detailed operational contract into a one-level reference file.
  - Preserve all function coverage: intent, start run, execution modes, five phases, run-until-done, orchestration, Playwright/UX verification, persistence, benchmark promotion, scheduling, output report, and validation gates.
- Selected intervention: progressive-disclosure rewrite of `SKILL.md` plus `references/operation.md`.
- Execution strategy: single-agent
- Agent tasks: skill-md-progressive-disclosure
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source validation complete before installed sync
- Verification evidence:
  - `wc -l SKILL.md references/operation.md` returned `126 SKILL.md` and `143 references/operation.md`.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py` passed.
  - `python3 scripts/product_loop_audit.py self/loop-runs --min-level L3` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates --min-level L2` passed at 87/100 L2.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic valid transcripts at 10/10.
  - UX skipped/not-run pressure smoke failed with exit 1 as expected.
  - Negated artifact audit fixture returned exit 1 as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `git diff --check` passed.
  - Installed `quick_validate.py <codex-home>/skills/loop-harness` passed.
  - Installed `product_loop_audit.py self/loop-runs --min-level L3` passed at 100/100 L3.
  - Installed line count returned `126 SKILL.md` and `143 references/operation.md`.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Error output: none
- Failed assertions: none
- Verdict: PASS
- Files changed:
  - `SKILL.md`
  - `references/operation.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
  - `self/loop-runs/product-loop-run-log.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-06-30-skill-md-progressive-disclosure
- Error class: scope_regression
- Symptom: trigger-time `SKILL.md` carried the full operations manual instead of a concise entrypoint.
- Evidence: pre-change `SKILL.md` had 446 lines; post-change `SKILL.md` has 126 lines and routes details to `references/operation.md`.
- Root cause/hypothesis: earlier iterations added operational safeguards directly into `SKILL.md`; once stable, those safeguards belonged in references for progressive disclosure.
- Reproduction steps: run `wc -l SKILL.md references/*.md` and inspect whether `SKILL.md` repeats detailed phase, orchestration, persistence, and output contracts.
- Severity: medium
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: skill-md-progressive-disclosure
- Matching rule: changes touch `SKILL.md`, `references/operation.md`, or reference routing.
- Expected result: `SKILL.md` stays under 200 lines, directly links the required references, and validation gates still pass.
- Verification command: `wc -l SKILL.md references/operation.md` plus source and installed validation gates.
- Status: active
- State promoted: concise entrypoint with detailed operation contract in direct references.
- Benchmark promoted: progressive-disclosure regression case.

### 2026-06-30T07:45:29Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals:
  - Code review found `scripts/product_loop_audit.py` reported `MISS negated evidence claims present` and capped readiness at 59/100 L1, but still returned exit code 0.
  - A readiness level can be informational, but a hard miss must fail automated gates.
  - Validation commands did not expose a minimum readiness level, so CI/smoke usage could accidentally accept L1 when L2/L3 was required.
- Handoff:
  - Add `--min-level` to make expected readiness explicit.
  - Add `--strict` for CI/release gates that must fail on any warning or miss.
  - Return non-zero for hard misses such as negated evidence and failed iterations without promoted active regression cases.
  - Update validation instructions and self-loop checks to use explicit minimum levels.
- Selected intervention: audit exit-code and threshold gate semantics.
- Execution strategy: single-agent
- Agent tasks: audit-hard-miss-exit-gate
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source validation complete before installed sync
- Verification evidence:
  - RED: negated evidence fixture printed `MISS negated evidence claims present: 1` and `AUDIT_EXIT=0`; the regression wrapper failed as expected.
  - GREEN: same negated evidence fixture now prints `AUDIT_EXIT=1`.
  - `python3 scripts/product_loop_audit.py self/loop-runs --min-level L3` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates --min-level L2` passed at 87/100 L2.
  - `python3 scripts/product_loop_audit.py assets/templates --strict` returned exit 1 as expected because templates have warnings.
  - Regex boundary smoke: `non-zero ... finding` in self-run narrative no longer triggers negated-evidence detection.
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py` passed.
  - `python3 scripts/product_loop_audit.py assets/templates --min-level L3` returned exit 1 as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic valid transcripts at 10/10.
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts with exit 1 as expected.
  - UX skipped/not-run pressure smoke failed with exit 1 as expected.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `git diff --check` passed.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ <skill-source>/ <codex-home>/skills/loop-harness/`
  - Installed `quick_validate.py <codex-home>/skills/loop-harness` passed.
  - Installed `product_loop_audit.py self/loop-runs --min-level L3` passed at 100/100 L3.
  - Installed `py_compile` for audit, cost, and pressure eval scripts passed.
  - Installed negated artifact fixture returned exit 1 as expected.
  - Installed pressure eval synthetic suite passed 7/7 at 10/10.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Error output: pre-fix audit returned exit code 0 for a hard miss.
- Failed assertions: hard audit miss should return non-zero.
- Verdict: PASS
- Files changed:
  - `SKILL.md`
  - `scripts/product_loop_audit.py`
  - `self/loop-runs/PRODUCT_LOOP.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
  - `self/loop-runs/product-loop-run-log.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-06-30-audit-hard-miss-exit-gate
- Error class: scope_regression
- Symptom: audit hard misses lowered readiness output but still returned shell success.
- Evidence: negated evidence fixture returned `Product Loop Readiness: 59/100 L1`, `MISS negated evidence claims present: 1`, and `AUDIT_EXIT=0` before the fix.
- Root cause/hypothesis: audit exit semantics treated any L1 artifact set as command success, even when findings included hard misses intended to block automation; negated-evidence parsing also treated `no` inside `non-zero` as a negated claim until the word boundary was tightened.
- Reproduction steps: append `No human gate. Playwright not run. Benchmark Promotion not filled.` to a copied template run log, run `python3 scripts/product_loop_audit.py <fixture>`, and inspect the exit code.
- Severity: high
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: audit-hard-miss-exit-gate
- Matching rule: product-loop audit exit-code logic, thresholding, strict mode, hard-miss detection, or validation commands change.
- Expected result: hard misses return non-zero; `--min-level` fails below the requested level; `--strict` fails on warnings or misses; words such as `non-zero` do not trigger negated-evidence detection.
- Verification command: `python3 scripts/product_loop_audit.py <negated-artifact-fixture>` and `python3 scripts/product_loop_audit.py assets/templates --strict`
- Status: active
- State promoted: audit commands used as gates must specify minimum readiness or strict mode.
- Benchmark promoted: audit hard-miss exit-code regression case.

### 2026-06-30T07:17:26Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals:
  - Code review found behavior false positives in `benchmark/run_pressure_eval.py`: a UX/UI transcript could say taste/slop checks were skipped or not run and still satisfy required pattern matches.
  - Code review found artifact audit false positives in `scripts/product_loop_audit.py`: negated evidence such as `No human gate`, `Playwright not run`, or `Benchmark Promotion not filled` could still contribute to a high readiness score.
  - The benchmark promotion pressure case did not require structured Raw Run Result, Finding, and Benchmark Promotion sections, so a transcript could mention those words without filling durable fields.
- Handoff:
  - Harden transcript scoring against skipped/not-run evidence.
  - Require structured raw result, finding, and promotion fields for failed-iteration promotion pressure tests.
  - Harden artifact audit so negated evidence caps readiness instead of passing as positive evidence.
  - Keep schema detection separate from positive-evidence detection so a valid failure symptom can describe missing behavior without invalidating the finding field.
- Selected intervention: false-positive hardening for benchmark scoring and artifact audit.
- Execution strategy: single-agent
- Agent tasks: false-positive-benchmark-audit-hardening
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source validation complete before installed sync
- Verification evidence:
  - `python3 scripts/product_loop_audit.py self/loop-runs` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates` passed at 87/100 L2 with expected template warnings for no real run activity.
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py` passed.
  - UX skipped/not-run transcript smoke failed as expected, including forbidden hits for skipped/not-run taste/slop benchmark evidence.
  - Negated artifact smoke returned 59/100 L1 with `MISS negated evidence claims present: 1`.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic valid transcripts at 10/10.
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `git diff --check` passed.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ <skill-source>/ <codex-home>/skills/loop-harness/`
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <codex-home>/skills/loop-harness` passed.
  - `python3 <codex-home>/skills/loop-harness/scripts/product_loop_audit.py <codex-home>/skills/loop-harness/self/loop-runs` passed at 100/100 L3.
  - `python3 <codex-home>/skills/loop-harness/scripts/product_loop_audit.py <codex-home>/skills/loop-harness/assets/templates` passed at 87/100 L2.
  - `python3 -m py_compile <codex-home>/skills/loop-harness/scripts/product_loop_audit.py <codex-home>/skills/loop-harness/scripts/product_loop_cost.py <codex-home>/skills/loop-harness/benchmark/run_pressure_eval.py` passed.
  - Installed `benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic valid transcripts at 10/10.
  - Installed UX skipped/not-run transcript smoke failed as expected.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Error output: none
- Failed assertions: none
- Verdict: PASS
- Files changed:
  - `benchmark/manifest.json`
  - `benchmark/run_pressure_eval.py`
  - `scripts/product_loop_audit.py`
  - `self/loop-runs/product-loop-run-log.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-06-30-false-positive-benchmark-audit
- Error class: scope_regression
- Symptom: benchmark and audit checks could accept superficial text mentions or negated evidence instead of requiring executed checks and structured fields.
- Evidence: synthetic UX transcript with skipped taste/slop checks now fails; synthetic negated artifact set now caps readiness at 59/100 L1.
- Root cause/hypothesis: the scorers used substring/regex presence as positive evidence without distinguishing required evidence, skipped checks, negated claims, and structured field completion.
- Reproduction steps: run a transcript containing `design-taste-frontend was skipped` and `design-slop-ban was not run`; run artifact audit on a copied template set with `No human gate. Playwright not run. Benchmark Promotion not filled.`
- Severity: high
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: false-positive-benchmark-audit-hardening
- Matching rule: loop-harness scoring, audit, or benchmark promotion logic changes.
- Expected result: skipped/not-run taste/slop transcripts fail; negated evidence artifacts cannot score above L1; failed-iteration promotion requires Raw Run Result, Finding, and Benchmark Promotion fields with real values.
- Verification command: `python3 benchmark/run_pressure_eval.py --transcripts <negative-and-positive-fixtures>` and `python3 scripts/product_loop_audit.py <negated-artifact-fixture>`
- Status: active
- State promoted: benchmark/audit evidence must distinguish positive evidence from skipped or negated evidence.
- Benchmark promoted: active regression cases for skipped UX benchmark, negated artifact evidence, and structured failed-iteration promotion fields.

### 2026-06-30T07:04:04Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals:
  - User confirmed a single active run log should contain raw run errors and findings.
  - Package had both `assets/templates/product-loop-run-log.md` and `self/loop-runs/product-loop-run-log.md`, causing confusion between template and active log.
  - Existing run-log template lacked explicit Raw Run Result, Finding, and Benchmark Promotion sections.
- Handoff:
  - Rename the template to `assets/templates/product-loop-run-log.template.md`.
  - Keep `self/loop-runs/product-loop-run-log.md` as the only active run log for loop-harness self-runs.
  - Update skill contract and schema so one run-log entry contains raw result, finding, and benchmark promotion decision.
- Selected intervention: single-log schema and template rename.
- Execution strategy: single-agent
- Agent tasks: single-run-log-finding-schema
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source and installed validation complete
- Verification evidence:
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py`
  - `python3 scripts/product_loop_audit.py self/loop-runs` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates` passed at 87/100 L2 with expected template warnings for no real run activity.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic transcripts at 10/10.
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ <skill-source>/ <codex-home>/skills/loop-harness/`
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <codex-home>/skills/loop-harness` passed.
  - `python3 <codex-home>/skills/loop-harness/scripts/product_loop_audit.py <codex-home>/skills/loop-harness/self/loop-runs` passed at 100/100 L3.
  - Installed run-log path check found only `assets/templates/product-loop-run-log.template.md` and `self/loop-runs/product-loop-run-log.md`.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Error output: none
- Failed assertions: none
- Verdict: PASS
- Files changed:
  - `SKILL.md`
  - `references/state-schema.md`
  - `assets/templates/product-loop-run-log.template.md`
  - `scripts/product_loop_audit.py`
  - `benchmark/manifest.json`
  - `benchmark/cases/failed_iteration_promotes_benchmark.md`
  - `self/loop-runs/product-loop-run-log.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-06-30-single-run-log-schema
- Error class: scope_regression
- Symptom: template run-log and active self-run log shared the same filename, and the run-log schema did not explicitly capture finding before benchmark promotion.
- Evidence: `find <skill-source> -path '*product-loop-run-log*'` returned both template and active self-run log paths.
- Root cause/hypothesis: template files used final artifact names, which is convenient for copying but ambiguous inside the skill package.
- Reproduction steps: inspect `assets/templates/` and `self/loop-runs/` for `product-loop-run-log.md`.
- Severity: medium
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: single-run-log-finding-schema
- Matching rule: loop-harness package structure or state schema touches run-log, findings, or benchmark promotion.
- Expected result: exactly one active run log per loop context; template files use `.template.md`; each run-log entry contains Raw Run Result, Finding, and Benchmark Promotion blocks.
- Verification command: `find <skill-dir> -path '*product-loop-run-log*' -print`
- Status: active
- State promoted: single active run-log convention and finding schema.
- Benchmark promoted: do not create separate error-log/findings files; promote benchmark only from run-log finding.

### 2026-06-30T05:29:01Z

- Profile: engineering-quality, content-docs
- Discovery signals:
  - Package root mixed runtime skill files with self-run loop artifacts.
  - User requested a dedicated `benchmark/` folder for eval/benchmark criteria such as UX/UI.
  - Existing self-eval suite lived under `evals/`, which was less clear than `benchmark/`.
- Handoff:
  - Move skill behavior evals into `benchmark/`.
  - Move self-run loop artifacts into `self/loop-runs/`.
  - Keep target-repo scaffold templates in `assets/templates/`.
  - Add a UX/UI criteria file under `benchmark/criteria/`.
- Selected intervention: reorganize package layout, update path references, make benchmark runner cwd-independent, and teach the audit script to find templates from self-loop artifact folders.
- Execution strategy: single-agent
- Agent tasks: package-structure-benchmark-folder
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source and installed validation complete
- Verification evidence:
  - Package root file check: only `.gitignore` and `SKILL.md` remain at root.
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py`
  - `python3 scripts/product_loop_audit.py self/loop-runs` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates` passed at 87/100 L2 with expected template warnings for no real run activity.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic transcripts at 10/10.
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ <skill-source>/ <codex-home>/skills/loop-harness/`
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <codex-home>/skills/loop-harness` passed.
  - `python3 <codex-home>/skills/loop-harness/scripts/product_loop_audit.py <codex-home>/skills/loop-harness/self/loop-runs` passed at 100/100 L3.
  - Installed package root file check: only `.gitignore` and `SKILL.md` remain at installed root.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Persistence:
  - `evals/` moved to `benchmark/`.
  - Root self-run artifacts moved to `self/loop-runs/`.
  - `benchmark/criteria/ux-ui.md` added.
  - `SKILL.md` updated with package layout boundaries.
  - `benchmark/run_pressure_eval.py` now resolves default files relative to its own folder.
  - `scripts/product_loop_audit.py` can audit self-loop artifacts while finding package templates in parent folders.
- Promotion:
  - State: package root must stay runtime-focused.
  - Benchmark: benchmark criteria and pressure cases live under `benchmark/`; self-run logs/state live under `self/loop-runs/`.
- Error classification: none
- Benchmark regression case: none
- Verdict: PASS
- Files changed:
  - `SKILL.md`
  - `benchmark/`
  - `scripts/product_loop_audit.py`
  - `self/loop-runs/`
- Next scheduling decision: stop_success

### 2026-06-30T05:20:25Z

- Profile: engineering-quality, ux-product
- Discovery signals:
  - `references/verification.md` required Playwright for app/prototype evaluation.
  - Existing pressure cases covered Playwright while omitting a visual-quality benchmark requirement.
  - User requested combining `design-taste-frontend` and `design-slop-ban` for UX/UI benchmark coverage.
- Handoff:
  - Add a combined UX/UI taste/slop benchmark gate while preserving Playwright as required runtime evidence.
  - Keep the change bounded to skill instructions, verification reference, pressure eval, benchmark artifacts, and templates.
- Selected intervention: add UX taste/slop verification rules, a critical pressure eval case, a case fixture, rubric updates, benchmark rules, and entrypoint guidance.
- Execution strategy: single-agent
- Agent tasks: ux-taste-slop-benchmark
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: source and installed validation complete
- Verification evidence:
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py`
  - `python3 scripts/product_loop_audit.py self/loop-runs` passed at 100/100 L3.
  - `python3 scripts/product_loop_audit.py assets/templates` passed at 87/100 L2 with expected template warnings for no real run activity.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>` passed.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic transcripts at 10/10.
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ <skill-source>/ <codex-home>/skills/loop-harness/`
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <codex-home>/skills/loop-harness` passed.
  - `python3 <codex-home>/skills/loop-harness/scripts/product_loop_audit.py <codex-home>/skills/loop-harness/self/loop-runs` passed at 100/100 L3.
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Persistence:
  - `references/verification.md` updated with UX Taste And Slop Benchmark.
  - `benchmark/manifest.json` updated with `ux_requires_taste_slop_benchmark`.
  - `benchmark/cases/ux_requires_taste_slop_benchmark.md` added.
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md` and template benchmark updated.
  - `self/loop-runs/PRODUCT_LOOP_STATE.md` updated for iteration 2.
- Promotion:
  - State: UX/UI visual-quality PASS cannot rely on Playwright alone.
  - Benchmark: active pressure case requires Playwright plus taste/slop score `>=8/10` and no critical slop violation.
- Error classification: none
- Benchmark regression case: none
- Verdict: PASS
- Files changed:
  - `SKILL.md`
  - `references/verification.md`
  - `benchmark/manifest.json`
  - `benchmark/cases/ux_requires_taste_slop_benchmark.md`
  - `benchmark/rubric.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/product-loop-run-log.md`
  - `assets/templates/PRODUCT_LOOP_BENCHMARK.md`
- Next scheduling decision: stop_success; apply the new UX taste/slop benchmark in future visual UI loop runs

### 2026-06-30T04:53:51Z

- Profile: engineering-quality, content-docs
- Discovery signals:
  - `loop-harness` had static audit and artifact checks.
  - It lacked pressure-test behavior benchmark files for real agent transcripts.
  - New execution orchestration contract needed benchmark cases for metric gate, Playwright gate, benchmark promotion, active benchmark blocking, parallel agents, and worktree isolation.
- Handoff:
  - Add `benchmark/` benchmark scaffold and self-loop artifacts under `self/loop-runs/`.
  - Keep intervention bounded to eval/benchmark support.
- Selected intervention: create pressure eval manifest, six critical cases, transcript scorer, and self-loop persistence files.
- Execution strategy: single-agent
- Agent tasks: self-behavior-benchmark-scaffold
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel conflicts
- Integration verification: pending final coordinator validation after merge
- Verification evidence:
  - `python3 -m py_compile scripts/product_loop_audit.py scripts/product_loop_cost.py benchmark/run_pressure_eval.py`
  - `python3 scripts/product_loop_audit.py self/loop-runs`
  - `python3 scripts/product_loop_audit.py assets/templates`
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d`
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts as expected.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed synthetic complete transcripts at 10/10.
  - `python3 <skill-creator-dir>/scripts/quick_validate.py <skill-source>`
- Playwright evidence:
  - URL: not applicable
  - Viewport: not applicable
  - Flow steps: not applicable
  - Assertions: not applicable
  - Screenshot/trace: not applicable
- Persistence:
  - Self-loop state added under `self/loop-runs/`.
  - Pressure benchmark cases added.
  - Handoff and worktree map added.
- Promotion:
  - State: behavior benchmark scaffold is the current active opportunity outcome.
  - Benchmark: six critical pressure cases define future regression checks.
- Error classification: none
- Benchmark regression case: none
- Verdict: PASS
- Files changed:
  - `benchmark/`
  - `self/loop-runs/PRODUCT_LOOP.md`
  - `self/loop-runs/PRODUCT_LOOP_STATE.md`
  - `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`
  - `self/loop-runs/product-loop-run-log.md`
  - `self/loop-runs/product-loop-budget.md`
  - `self/loop-runs/AGENT_HANDOFF.md`
  - `self/loop-runs/worktree-map.md`
- Next scheduling decision: stop_success after merge, installed sync, and final validation

### 2026-07-09T03:27:48Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals: review found four self-development defects: L3 audit passed while latest run-log validator failed, frontmatter description summarized workflow instead of trigger conditions, scheduling next-action docs used inconsistent enum values, and engineering-quality skill-package benchmark selection returned zero cases.
- Handoff: run one sequential execution batch across shared skill package files with lanes for latest run-log hard gate, trigger metadata, canonical scheduling docs, self-benchmark selection, and persistence.
- Selected intervention: add failing regression tests, make product_loop_audit enforce latest run-log validation, rewrite trigger metadata, align scheduling next-action docs, make strict_run_log_validator match self-development selection, and persist new active regression cases.
- Execution strategy: sequential coordinator execution within one run-until-done iteration batch.
- Agent tasks: self-latest-run-log-hardening, trigger-metadata-canonical-scheduling, self-benchmark-selection, self-loop-persistence
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: no parallel agents or worktrees used; changed files are shared package files reviewed in one workspace.
- Integration verification: source and installed copies verified after installed sync.
- Verification evidence: RED `python3 benchmark/test_tooling_regressions.py` failed 4 targeted cases; GREEN `python3 benchmark/test_tooling_regressions.py` passed 15/15 in source and installed copies. Source and installed `python3 -m py_compile scripts/*.py benchmark/*.py` passed. `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK. Source and installed `python3 scripts/select_benchmarks.py --repo <skill-dir> --profile engineering-quality --intent ENGINEERING_QUALITY --surface skill-package --include-skill --require` selected `strict_run_log_validator`. Source and installed template audits passed 100/100 L2. Source and installed self audits passed 100/100 L3. Source and installed latest run-log validation passed. Source and installed pressure eval passed 15/15 with suite score 10.00/10. Source and installed quick_validate passed. UX web-route benchmark selection returned 2 cases. `select_knowledge.py` returned built-in fallback UX criteria and seed.
- Playwright evidence: not_applicable for skill-package self-development; no app, route, local dev server, deployed page, or interactive prototype was under test.
- Error output: RED suite before implementation showed failures for latest run-log audit, operation next actions, self benchmark selection, and frontmatter trigger-only description.
- Failed assertions: current GREEN suite has none; RED assertions are preserved in `benchmark/test_tooling_regressions.py`.
- Verdict: PASS
- Files changed: `SKILL.md`, `references/operation.md`, `scripts/product_loop_audit.py`, `benchmark/manifest.json`, `benchmark/test_tooling_regressions.py`, `self/loop-runs/PRODUCT_LOOP_STATE.md`, `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`, `self/loop-runs/product-loop-run-log.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-07-09-self-development-validation-hardening
- Error class: scope_regression
- Symptom: loop-harness self-development could appear clean while the latest run-log entry was invalid, trigger metadata encouraged shortcut behavior, scheduling docs used mixed next-action terms, and benchmark selection had no self-development case for engineering-quality skill-package work.
- Evidence: pre-fix `validate_run_log_entry.py self/loop-runs/product-loop-run-log.md` failed while `product_loop_audit.py self/loop-runs --min-level L3` passed; pre-fix tooling regression suite failed 4 targeted cases.
- Root cause/hypothesis: previous readiness checks searched schema fields across the whole log instead of validating the latest entry, and skill metadata plus scheduling/benchmark matching had not been covered by deterministic regression tests.
- Reproduction steps: run `python3 scripts/validate_run_log_entry.py self/loop-runs/product-loop-run-log.md`, inspect `SKILL.md` frontmatter description, inspect `references/operation.md` scheduling text, and run `python3 scripts/select_benchmarks.py --repo <skill-source> --profile engineering-quality --intent ENGINEERING_QUALITY --surface skill-package --include-skill --require` on the pre-fix package.
- Severity: high
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: latest-run-log-validator-hard-gate, skill-frontmatter-trigger-only, canonical-scheduling-next-actions, skill-package-self-benchmark-selection
- Matching rule: changes touch product_loop_audit, validate_run_log_entry, SKILL.md frontmatter, operation scheduling docs, benchmark manifest matching, self-development validation commands, or self-loop persistence artifacts.
- Expected result: L3 audit fails when the latest run-log entry is invalid; skill description starts with `Use when` and stays trigger-only; scheduling next actions use canonical lowercase action values; engineering-quality skill-package benchmark selection returns at least `strict_run_log_validator`.
- Verification command: `python3 benchmark/test_tooling_regressions.py`; `python3 scripts/validate_run_log_entry.py self/loop-runs/product-loop-run-log.md`; `python3 scripts/product_loop_audit.py self/loop-runs --min-level L3`; `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass`
- Status: active
- State promoted: self-development validator hardening, trigger-only frontmatter metadata, canonical scheduling next actions, and self-development benchmark selection coverage.
- Benchmark promoted: active regression cases for latest run-log validator hard gate, frontmatter trigger-only metadata, canonical scheduling next actions, and engineering-quality skill-package benchmark selection.

### 2026-07-09T04:17:58Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals: user requested parallel-agent self-fix of loop-harness; independent audits found runtime evaluation contract scaffold gap, benchmark scale risk in a single markdown file, split active benchmark selection/audit gaps, archive semantics gaps, and pressure coverage gaps for those behaviors.
- Handoff: dispatch parallel audit lanes for evaluation-contract, benchmark-scale, and self-coverage findings; coordinator owns file edits and integrated validation.
- Selected intervention: add locked runtime criteria scaffold, split active benchmark storage/selection/audit behavior, archive retention guidance, controller compact-index promotion, pressure cases/fixtures, and self-loop persistence.
- Execution strategy: multi-lane audit with coordinator implementation in one run-until-done iteration batch.
- Agent tasks: galileo-evaluation-contract-audit, raman-benchmark-scale-audit, noether-self-coverage-audit
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: audit agents were read-only; coordinator integrated shared script, template, manifest, fixture, and self-loop artifact edits in one workspace.
- Integration verification: targeted GREEN tooling suite passed 7/7; full tooling regression suite passed 22/22; pressure eval passed 18/18 at 10/10; template audit passed 100/100 L2; source and installed gates passed after installed sync.
- Verification evidence: RED tests first failed for criteria/current scaffold gap, split active benchmark selection gap, and evaluation-contract pressure case gap; GREEN tests now cover scaffold runtime dirs, selector active/archive behavior, audit active/archive behavior, controller split promotion, templates retention guidance, and pressure cases.
- Playwright evidence: not_applicable for skill-package self-development; no app, route, local dev server, deployed page, or interactive prototype was under test.
- Error output: RED targeted tests reported missing `.loop-harness/criteria/current.md`, selector selected zero split active cases, and pressure eval returned `No cases selected` for `evaluation_contract_before_action`.
- Failed assertions: current GREEN suites have none; RED assertions are preserved in `benchmark/test_tooling_regressions.py`.
- Verdict: PASS
- Files changed: `SKILL.md`, `references/operation.md`, `references/state-schema.md`, `scripts/init_loop.py`, `scripts/run_loop_controller.py`, `scripts/select_benchmarks.py`, `scripts/product_loop_audit.py`, `assets/templates/`, `benchmark/`, `self/loop-runs/`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-07-09-scale-contract-hardening
- Error class: scope_regression
- Symptom: loop-harness could start actioning without a scaffolded repo-local evaluation contract, keep appending full promoted cases to one benchmark markdown file, miss active split case files, and treat archive behavior as undefined.
- Evidence: pre-fix targeted tests failed for scaffold runtime criteria, split active benchmark selection, and evaluation-contract pressure coverage; audit-only agents independently identified the same contract, scale, and self-coverage gaps.
- Root cause/hypothesis: earlier package hardening focused on core run-log and artifact schema but did not define a scalable active benchmark store or a runtime criteria contract generated per target repo.
- Reproduction steps: run the pre-fix `python3 benchmark/test_tooling_regressions.py ToolingRegressionTests.test_scaffold_creates_runtime_criteria_and_archive_dirs ToolingRegressionTests.test_select_benchmarks_reads_split_active_case_files ToolingRegressionTests.test_pressure_eval_covers_evaluation_contract_before_action`.
- Severity: high
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: runtime-evaluation-contract-scaffold, split-active-benchmark-files, compact-benchmark-index-controller-promotion, self-pressure-coverage-scale-contract
- Matching rule: changes touch criteria/current scaffold, pre-action evaluation contract rules, benchmark storage/selection/audit, controller promotion, archive retention, pressure manifest/fixtures, or self-loop persistence artifacts.
- Expected result: target repos scaffold `.loop-harness/criteria/current.md` and split retention dirs; actioning requires `Contract status: locked`; controller writes full active cases to `benchmarks/active/` when available; selector and audit read active split files and ignore archive; pressure eval covers these behaviors.
- Verification command: `python3 benchmark/test_tooling_regressions.py`; `python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass`; `python3 scripts/product_loop_audit.py assets/templates --min-level L2`; `python3 scripts/product_loop_audit.py self/loop-runs --strict`
- Status: active
- State promoted: runtime evaluation contract scaffold, split active benchmark storage, compact benchmark index, archive retention semantics, and self pressure coverage for scale/contract behavior.
- Benchmark promoted: active regression cases for runtime evaluation contract scaffold, split active benchmark files, compact controller promotion, and self pressure coverage.

### 2026-07-09T04:45:18Z

#### Raw Run Result

- Profile: engineering-quality, content-docs
- Discovery signals: Task C asked for user-facing skill docs/templates and self-loop persistence updates for watchdog scheduler semantics only, with scripts, benchmark tests, and manifest outside scope.
- Handoff: execute one coordinator-owned docs lane across the assigned markdown files, preserving concurrent edits already present in the worktree.
- Selected intervention: document `watchdog.py setup/status/pause/resume/tail/uninstall/tick`, fresh-process continuation through `.loop-harness/*`, locked criteria for scheduled `run-until-done`, overlap lock behavior, and `.loop-harness/schedules/` status/log paths; persist matching self-loop state, benchmark, handoff, and worktree entries.
- Execution strategy: single-lane docs update in the current coordinator workspace.
- Agent tasks: watchdog-scheduler-semantics
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: assigned files had existing edits; this entry was layered on top without touching unassigned scripts, tests, or manifest files.
- Integration verification: latest run-log validator and strict self-loop audit are the acceptance checks for this docs-only scheduler semantics update.
- Verification evidence: `python3 scripts/validate_run_log_entry.py self/loop-runs/product-loop-run-log.md`; `python3 scripts/product_loop_audit.py self/loop-runs --strict`.
- Error output: clean docs-only scheduler semantics entry prepared for validation.
- Failed assertions: clean docs-only scheduler semantics entry prepared for validation.
- Verdict: PASS
- Files changed: `SKILL.md`, `references/operation.md`, `references/state-schema.md`, `assets/templates/PRODUCT_LOOP.md`, `assets/templates/PRODUCT_LOOP_STATE.md`, `assets/templates/product-loop-budget.md`, `self/loop-runs/PRODUCT_LOOP.md`, `self/loop-runs/PRODUCT_LOOP_STATE.md`, `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`, `self/loop-runs/product-loop-run-log.md`, `self/loop-runs/AGENT_HANDOFF.md`, `self/loop-runs/worktree-map.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-07-09-watchdog-scheduler-semantics
- Error class: scope_regression
- Symptom: watchdog scheduler lifecycle semantics needed concise user-facing docs/templates and self-loop persistence coverage.
- Evidence: Task C required command documentation, scheduled fresh-process persistence semantics, locked criteria for scheduled `run-until-done`, overlap lock semantics, and `.loop-harness/schedules/` status/log locations.
- Root cause/hypothesis: previous scheduling docs covered canonical next actions and criteria locking, while watchdog lifecycle commands and persisted-state scheduler process model needed explicit wording.
- Reproduction steps: inspect the pre-update scheduler sections in `SKILL.md`, `references/operation.md`, `references/state-schema.md`, and the product loop templates for watchdog command lifecycle and `.loop-harness/schedules/` details.
- Severity: medium
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: watchdog-scheduler-lifecycle-semantics
- Matching rule: changes touch scheduling docs, scheduler templates, state schema, budget template, self-loop persistence artifacts, or watchdog command names.
- Expected result: user-facing docs/templates list `watchdog.py setup/status/pause/resume/tail/uninstall/tick`, define scheduled ticks as fresh processes continuing from `.loop-harness/*` state, require locked criteria for scheduled `run-until-done`, describe the overlap lock, and locate status/logs under `.loop-harness/schedules/`.
- Verification command: `python3 scripts/validate_run_log_entry.py self/loop-runs/product-loop-run-log.md`; `python3 scripts/product_loop_audit.py self/loop-runs --strict`
- Status: active
- State promoted: watchdog scheduler lifecycle semantics in docs/templates and self-loop state.
- Benchmark promoted: active regression case for watchdog scheduler lifecycle semantics.

### 2026-07-09T05:04:30Z

#### Raw Run Result

- Profile: engineering-quality, content-docs, release-readiness
- Discovery signals: public readiness review found missing README/LICENSE, no configured remote, personal absolute local paths in self artifacts, local cache/runtime files not broadly ignored, and no deterministic gate preventing these regressions before GitHub publish.
- Handoff: dispatch independent public-release agents for README/LICENSE, path sanitization, and git/GitHub readiness; coordinator owns integration, regression test, final verification, commit, and push.
- Selected intervention: add public README and MIT license, replace personal absolute paths with portable placeholders, expand `.gitignore`, add public release hygiene tooling regression, and persist a promoted benchmark case.
- Execution strategy: multi-lane public-release batch with parallel agents and coordinator integration.
- Agent tasks: public-release-docs, public-path-sanitize, github-readiness-ignore, public-release-hygiene-test
- Worktree map: self/loop-runs/worktree-map.md
- Conflict review: agents owned disjoint files; coordinator reviewed integrated diff and added the regression test without reverting existing loop-harness fixes.
- Integration verification: targeted public hygiene regression, full source gates, installed-copy smoke gates, and quick_validate passed after the expected RED missing-test failure.
- Verification evidence: RED `python3 benchmark/test_tooling_regressions.py ToolingRegressionTests.test_public_release_hygiene_has_docs_and_no_local_paths` failed because the test method did not exist; GREEN targeted test passed after adding README examples, LICENSE, sanitize checks, scheduler wording check, and token/path scanning. Source gates passed: 29 tooling tests, 19/19 pressure cases at 10/10, self audit 100/100 L3, template audit 100/100 L2, latest run-log validator, py_compile, cost smoke, benchmark selection, public path/token scan, diff check, and quick_validate. Installed-copy gates passed: quick_validate, self audit 100/100 L3, template audit 100/100 L2, latest run-log validator, 19/19 pressure cases, and 29 tooling tests.
- Playwright evidence: not_applicable for skill-package public-release hygiene; no app, route, local dev server, deployed page, or interactive prototype was under test.
- Error output: RED targeted test reported `ToolingRegressionTests` had no attribute `test_public_release_hygiene_has_docs_and_no_local_paths`; first GREEN attempt caught the test's own absolute-local-path regex literal, then pattern construction was corrected.
- Failed assertions: current targeted GREEN test has none.
- Verdict: PASS
- Files changed: `README.md`, `LICENSE`, `.gitignore`, `SKILL.md`, `benchmark/test_tooling_regressions.py`, `self/loop-runs/PRODUCT_LOOP_STATE.md`, `self/loop-runs/PRODUCT_LOOP_BENCHMARK.md`, `self/loop-runs/product-loop-run-log.md`, `self/loop-runs/AGENT_HANDOFF.md`, `self/loop-runs/worktree-map.md`
- Next scheduling decision: stop_success

#### Finding

- Finding id: finding-2026-07-09-public-release-hygiene
- Error class: scope_regression
- Symptom: loop-harness was functionally validated but not public-release clean because the package lacked public README/LICENSE, contained machine-local path evidence in committed self artifacts, had no remote, and did not have a repeatable release hygiene regression.
- Evidence: pre-cleanup `git status` showed no README/LICENSE and no remote; review found personal absolute paths in self artifacts; targeted RED test did not exist before implementation.
- Root cause/hypothesis: previous self-development iterations optimized runtime loop behavior and scheduler semantics but did not codify public GitHub packaging hygiene as a benchmarked requirement.
- Reproduction steps: inspect pre-cleanup repo for README/LICENSE, run `git remote -v`, scan public text files for personal absolute local paths and token literals, and run the pre-cleanup targeted tooling regression method.
- Severity: high
- Confidence: high
- Status: promoted

#### Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: public-release-hygiene
- Matching rule: changes touch README, LICENSE, `.gitignore`, skill validation docs, self-loop artifacts, public release workflow, or token/path scanning patterns.
- Expected result: README/LICENSE exist; README uses `$loop-harness` examples and does not claim automatic OS scheduler installation; `.gitignore` excludes local caches and `.loop-harness/`; public text files have no personal absolute local paths or secret-literal patterns; GitHub remote/push readiness is checked before publish.
- Verification command: `python3 benchmark/test_tooling_regressions.py ToolingRegressionTests.test_public_release_hygiene_has_docs_and_no_local_paths`; public text-file scan for absolute local user paths and token/API-key literals
- Status: active
- State promoted: public release docs, license, path hygiene, gitignore coverage, and deterministic public hygiene gate.
- Benchmark promoted: active regression case for public-release hygiene before GitHub publish.
