# Product Loop Run Log

Append one entry per loop run.

## Entries

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
  - `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/haido/loop-harness` passed.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ /Users/haido/loop-harness/ /Users/haido/.codex/skills/loop-harness/`
  - `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/haido/.codex/skills/loop-harness` passed.
  - `python3 /Users/haido/.codex/skills/loop-harness/scripts/product_loop_audit.py /Users/haido/.codex/skills/loop-harness/self/loop-runs` passed at 100/100 L3.
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
- Evidence: `find /Users/haido/loop-harness -path '*product-loop-run-log*'` returned both template and active self-run log paths.
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
  - `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/haido/loop-harness` passed.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic transcripts at 10/10.
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ /Users/haido/loop-harness/ /Users/haido/.codex/skills/loop-harness/`
  - `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/haido/.codex/skills/loop-harness` passed.
  - `python3 /Users/haido/.codex/skills/loop-harness/scripts/product_loop_audit.py /Users/haido/.codex/skills/loop-harness/self/loop-runs` passed at 100/100 L3.
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
  - Existing pressure cases covered Playwright but did not require a visual-quality benchmark.
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
  - `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/haido/loop-harness` passed.
  - `python3 benchmark/run_pressure_eval.py --transcripts <tmpdir>` passed 7/7 synthetic transcripts at 10/10.
  - `python3 benchmark/run_pressure_eval.py` failed missing transcripts as expected.
  - `python3 scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d` returned Status OK.
  - `rsync -a --delete --exclude .git --exclude .worktrees --exclude __pycache__ /Users/haido/loop-harness/ /Users/haido/.codex/skills/loop-harness/`
  - `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/haido/.codex/skills/loop-harness` passed.
  - `python3 /Users/haido/.codex/skills/loop-harness/scripts/product_loop_audit.py /Users/haido/.codex/skills/loop-harness/self/loop-runs` passed at 100/100 L3.
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
  - `python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/haido/loop-harness`
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
