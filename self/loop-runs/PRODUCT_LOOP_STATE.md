# Product Loop State

Last run: 2026-07-09T05:04:30Z
Intent: ENGINEERING_QUALITY
Primary metric: pressure benchmark case score
Baseline window: before scale and evaluation-contract hardening
Execution mode: run-until-done
Current iteration: 14
Target: all critical pressure benchmark cases score `>=8/10`; strict latest run-log validation passes; engineering-quality skill-package benchmark selection is non-empty; runtime criteria scaffold, split active benchmark storage, watchdog scheduler semantics, and public release hygiene pass
Latest verdict: PASS
Stop condition: SUCCESS
Evaluation contract: self/loop-runs/criteria/current.md
Contract status: locked

## Active Opportunity

Prepare loop-harness for public GitHub release: add public README/LICENSE, sanitize personal absolute paths from skill/self artifacts, ignore local runtime/cache files, add a deterministic public hygiene regression test, and verify before commit/push.

Handoff: multi-lane public release batch using independent agents for docs, sanitize, and GitHub readiness; coordinator owns integration, regression test, final validation, commit, and push.
Verification: public hygiene targeted RED/GREEN test, full tooling regressions, pressure eval, strict self audit, template audit, latest run-log validator, py_compile, cost smoke, benchmark selection, quick_validate, installed-copy sync checks, and git/GitHub push checks.
Persistence: self-loop state, run-log, benchmark, handoff, and worktree-map entries cover public-release hygiene.
Scheduling: stop_success

## Execution Orchestration

Execution strategy: parallel-agents plus coordinator integration
Batch planning: required before actioning
Batch type: multi-lane public release
Lane ids: lane-public-docs, lane-public-sanitize, lane-github-readiness, lane-public-hygiene-test
Lane dependencies: none
Parallelization strategy: independent agents own README/LICENSE, path sanitization, and gitignore/GitHub readiness; coordinator integrates and verifies
Parallelization rationale: public docs, existing artifact sanitization, and repository hygiene have disjoint write scopes
Deferred lane rationale: none; no known independent lane was deferred to a later iteration
Parallel domains: public docs, path sanitize, GitHub readiness
Agent task ids: public-release-docs, public-path-sanitize, github-readiness-ignore, public-release-hygiene-test
Worktree strategy: current coordinator workspace with disjoint file ownership; no separate git worktrees required
Integration owner: coordinator
Conflict review: agents touched disjoint owned files; coordinator reviewed integrated diff and added the regression test.
Integrated verification: public hygiene targeted test, full source release gates, installed-copy smoke gates, and quick_validate passed.

## Selected Criteria / Benchmark Seeds

- Criteria pointer: self/loop-runs/criteria/current.md
- Contract status: locked
- Benchmark seed: evaluation_contract_before_action
- Benchmark seed: split_active_benchmark_files
- Benchmark seed: skill_package_self_benchmark_selection
- Benchmark seed: watchdog_scheduler_lifecycle_semantics
- Benchmark seed: public_release_hygiene

## Candidate Backlog

- Add live agent runner integration if Codex exposes a stable non-interactive subagent API.
- Add more pressure cases for scheduling cost caps, human gates, and scope regression.
- Add negative committed fixtures for each pressure benchmark case.
- Consider a future lightweight metadata validator for all installed local skills, not only loop-harness.

## Watch List

- Pressure eval script should not pretend to run agents; it scores real transcripts only.
- Self-loop artifacts under `self/loop-runs/` should not replace the skill package contract.
- Package root should not contain self-run `PRODUCT_LOOP*`, handoff, budget, run-log, or worktree-map files.
- Do not create separate `error-log.md`, `findings.md`, or `run-log-error.md`; keep raw result, finding, and promotion in the run-log entry.

## Failed Attempts / Do Not Retry

- Do not rely only on `product_loop_audit.py` for behavior quality.
- Do not mark pressure behavior pass without transcript evidence.
- Do not claim UX/UI visual-quality PASS from Playwright alone when visual quality matters.
- Do not put skill self-run logs or state back at package root.
- Do not promote a benchmark case from a failure until the run-log entry contains a structured finding.
- Do not treat skipped/not-run benchmark mentions as positive evidence.
- Do not treat negated artifact statements such as `No human gate`, `Playwright not run`, or `Benchmark Promotion not filled` as passing evidence.
- Do not allow hard audit misses to return exit code 0.
- Do not let `SKILL.md` grow into the full operations manual when reference files can carry detailed contract sections.
- Do not report template-placeholder state/log absence as WARN when auditing `assets/templates` as a template package.
- Do not rely on uncommitted tmpdir transcripts for pressure eval smoke validation.
- Do not scatter target-repo loop artifacts across repo root; use `.loop-harness/` by default.
- Do not make users pass `.loop-harness/` explicitly when audit can auto-detect it from repo root.
- Do not write runtime learning into the skill package; keep reusable cross-repo knowledge in `~/.codex/loop-harness/knowledge/`.
- Do not promote global knowledge directly from noisy, incomplete, env-blocked, inactive, or unreviewed findings.
- Do not rely on `product_loop_audit.py` L3 unless the latest run-log entry also passes `validate_run_log_entry.py`.
- Do not put process/workflow summaries in skill frontmatter descriptions; use trigger-only wording.
- Do not let self-development benchmark selection return zero cases for `engineering-quality` + `skill-package`.
- Do not document scheduled jobs as chat-session continuation; use persisted `.loop-harness/*` state and `.loop-harness/schedules/` lifecycle files.

## Active Benchmark Regressions

- `false-positive-benchmark-audit-hardening`: skipped UX benchmark transcripts fail, negated artifact evidence is capped below pass, and failed-iteration promotion requires filled structured sections.
- `audit-hard-miss-exit-gate`: negated evidence and missing promoted regression cases return non-zero exit codes; self-run gates use `--min-level L3`.
- `skill-md-progressive-disclosure`: `SKILL.md` stays concise and routes full behavior to one-level reference files.
- `template-placeholder-audit-no-warning`: `assets/templates` audit passes L2 without WARN/MISS while still not claiming L3 scheduled readiness.
- `committed-pressure-pass-fixtures`: pressure eval has committed pass fixtures for all critical cases and scores 10/10.
- `default-loop-artifact-root`: target-repo artifacts live in `.loop-harness/`, pressure transcripts require that path, and audit auto-detects it from repo root.
- `global-local-knowledge-store`: global local criteria are selected as matching subsets, and reusable global promotion goes through inbox/gate before promoted knowledge.
- `latest-run-log-validator-hard-gate`: L3 audit fails if the latest run-log entry is missing strict structured sections.
- `skill-frontmatter-trigger-only`: `SKILL.md` frontmatter description starts with `Use when` and does not summarize workflow.
- `canonical-scheduling-next-actions`: scheduling docs use `stop_success`, `run_again_now`, `schedule`, `pause`, or `escalate` as next actions.
- `skill-package-self-benchmark-selection`: engineering-quality skill-package self-development selects at least one matching benchmark case.
- `runtime-evaluation-contract-scaffold`: target repos scaffold `.loop-harness/criteria/current.md`, and actioning requires a locked evaluation contract.
- `split-active-benchmark-files`: selectors and audits read active split case files under `benchmarks/active/` and ignore `benchmarks/archive/`.
- `compact-benchmark-index-controller-promotion`: controller promotions write full cases to split active files when available and keep `PRODUCT_LOOP_BENCHMARK.md` compact.
- `self-pressure-coverage-scale-contract`: pressure fixtures cover evaluation-contract, split-active benchmark, scaffold, and self skill-package selection behavior.
- `watchdog-scheduler-lifecycle-semantics`: docs/templates describe watchdog commands, fresh-process persisted-state continuation, locked criteria, overlap lock, and `.loop-harness/schedules/` status/logs.
- `public-release-hygiene`: public package includes README/LICENSE, generic install/use docs, no personal absolute paths or token literals, and `.gitignore` excludes local caches/runtime artifacts.

## Iteration History

- 2026-06-30T04:53:51Z: Added pressure benchmark manifest, six critical cases, transcript scorer, and self-loop artifacts; verified negative missing-transcript behavior and synthetic positive pass behavior.
- 2026-06-30T05:20:25Z: Added combined `design-taste-frontend` and `design-slop-ban` UX/UI visual-quality benchmark gate; verified source and installed skill.
- 2026-06-30T05:29:01Z: Moved self-eval suite to `benchmark/`, moved self-run artifacts to `self/loop-runs/`, and added UX/UI benchmark criteria; source verification passed.
- 2026-06-30T07:04:04Z: Added single run-log schema with Raw Run Result, Finding, and Benchmark Promotion; source and installed verification passed.
- 2026-06-30T07:17:26Z: Hardened benchmark/audit scoring against skipped checks, negated evidence, and unfilled structured fields; source and installed verification passed.
- 2026-06-30T07:45:29Z: Added audit min-level/strict gate semantics and blocking-finding non-zero exit behavior; source and installed verification passed.
- 2026-06-30T07:54:23Z: Reduced `SKILL.md` to an entrypoint and moved detailed operations contract to `references/operation.md`; source and installed verification passed.
- 2026-06-30T08:01:27Z: Removed template-placeholder WARN noise and added committed pressure pass fixtures; source and installed verification passed.
- 2026-06-30T08:50:55Z: Standardized target-repo artifacts under `.loop-harness/`, added repo-root audit auto-discovery, and updated pressure benchmarks; source and installed verification passed.
- 2026-06-30T10:02:11Z: Added global local knowledge selection and gated promotion scripts; source verification passed.
- 2026-07-09T03:27:48Z: Hardened self-development validation so audit enforces latest run-log schema, metadata uses trigger-only wording, scheduling next actions are canonical, and engineering-quality skill-package benchmark selection is non-empty.
- 2026-07-09T04:17:58Z: Added locked runtime evaluation contract scaffold, split active benchmark storage/selection/audit behavior, archive retention guidance, self pressure coverage, and parallel-audit-backed self-loop persistence.
- 2026-07-09T04:45:18Z: Added watchdog scheduler lifecycle semantics to user-facing docs/templates and self-loop persistence.
- 2026-07-09T05:04:30Z: Added public README/LICENSE, sanitized personal local paths, expanded `.gitignore`, and added public release hygiene regression coverage before GitHub publish.

## Watchdog Scheduler

- Commands: `watchdog.py setup`, `watchdog.py status`, `watchdog.py pause`, `watchdog.py resume`, `watchdog.py tail`, `watchdog.py uninstall`, `watchdog.py tick`
- Status/logs: `.loop-harness/schedules/`
- Process model: each scheduled tick starts fresh and continues from `.loop-harness/*` state.
- Lock: one active tick per schedule.
- Run-until-done requirement: `criteria/current.md` is locked before actioning.

## Human Decisions

- User requested `$loop-harness` to fix `$loop-harness`.
- User requested plan, parallel agents, full fixes, and GitHub push for public release.

## User Confirmations

- Benchmark direction: pressure-test agent behavior thật.
- UX/UI benchmark direction: combine `design-taste-frontend` and `design-slop-ban`.
- Structure direction: add a dedicated `benchmark/` folder for skill behavior criteria and keep self-run artifacts out of package root.
- Run-log direction: one active run-log file per loop context; include raw errors and findings inside that file.

## Data Gaps / Instrumentation Needs

- Live run transcripts should still be captured from real agent behavior; committed pass fixtures exist only for smoke-testing the scorer and benchmark contract.

## Next Scheduled Action

None. Run manually when a new loop-harness change needs behavior validation.
