# Product Loop State

Last run: 2026-06-30T08:50:55Z
Intent: ENGINEERING_QUALITY
Primary metric: pressure benchmark case score
Baseline window: before `benchmark/` behavior benchmark scaffold
Execution mode: run-until-done
Current iteration: 9
Target: all critical pressure benchmark cases score `>=8/10`
Latest verdict: PASS
Stop condition: SUCCESS

## Active Opportunity

Standardize target-repo loop artifacts under `.loop-harness/` while preserving audit compatibility with repo-root commands.

Handoff: single-agent implementation in current coordinator workspace
Verification: repo-root `.loop-harness` auto-discovery smoke, committed pressure pass fixtures, self-loop strict L3 audit, template L2 audit without WARN/MISS, py_compile, cost smoke, skill quick_validate, source and installed validation
Persistence: self-loop artifacts under `self/loop-runs/`, `.loop-harness` artifact-root benchmark, installed skill sync
Scheduling: stop_success

## Execution Orchestration

Execution strategy: single-agent
Parallel domains: none for this intervention
Agent task ids: default-loop-artifact-root
Worktree strategy: current coordinator workspace; no parallel file-changing agents used
Integration owner: coordinator
Conflict review: no parallel agent conflicts
Integrated verification: repo-root auto-discovery smoke passed against a temp repo with `.loop-harness/` artifacts at 87/100 L2 and no WARN/MISS; source quick_validate pass, py_compile pass, self-loop strict audit L3 100/100, template audit L2 100/100 with no WARN/MISS, committed pressure fixture eval PASS 10/10 across 7 cases, cost smoke OK, diff check pass, installed sync pass, installed quick_validate pass, installed repo-root auto-discovery smoke pass, installed self-loop strict audit L3 100/100, installed template audit L2 100/100 with no WARN/MISS, installed committed pressure fixture eval PASS 10/10

## Candidate Backlog

- Add live agent runner integration if Codex exposes a stable non-interactive subagent API.
- Add more pressure cases for scheduling cost caps, human gates, and scope regression.
- Add negative committed fixtures for each pressure benchmark case.

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

## Active Benchmark Regressions

- `false-positive-benchmark-audit-hardening`: skipped UX benchmark transcripts fail, negated artifact evidence is capped below pass, and failed-iteration promotion requires filled structured sections.
- `audit-hard-miss-exit-gate`: negated evidence and missing promoted regression cases return non-zero exit codes; self-run gates use `--min-level L3`.
- `skill-md-progressive-disclosure`: `SKILL.md` stays concise and routes full behavior to one-level reference files.
- `template-placeholder-audit-no-warning`: `assets/templates` audit passes L2 without WARN/MISS while still not claiming L3 scheduled readiness.
- `committed-pressure-pass-fixtures`: pressure eval has committed pass fixtures for all critical cases and scores 10/10.
- `default-loop-artifact-root`: target-repo artifacts live in `.loop-harness/`, pressure transcripts require that path, and audit auto-detects it from repo root.

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

## Human Decisions

- User requested `$loop-harness` to fix `$loop-harness`.

## User Confirmations

- Benchmark direction: pressure-test agent behavior thật.
- UX/UI benchmark direction: combine `design-taste-frontend` and `design-slop-ban`.
- Structure direction: add a dedicated `benchmark/` folder for skill behavior criteria and keep self-run artifacts out of package root.
- Run-log direction: one active run-log file per loop context; include raw errors and findings inside that file.

## Data Gaps / Instrumentation Needs

- Live run transcripts should still be captured from real agent behavior; committed pass fixtures exist only for smoke-testing the scorer and benchmark contract.

## Next Scheduled Action

None. Run manually when a new loop-harness change needs behavior validation.
