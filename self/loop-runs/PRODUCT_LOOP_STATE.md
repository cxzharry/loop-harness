# Product Loop State

Last run: 2026-06-30T07:54:23Z
Intent: ENGINEERING_QUALITY
Primary metric: pressure benchmark case score
Baseline window: before `benchmark/` behavior benchmark scaffold
Execution mode: run-until-done
Current iteration: 7
Target: all critical pressure benchmark cases score `>=8/10`
Latest verdict: PASS
Stop condition: SUCCESS

## Active Opportunity

Slim `SKILL.md` into a concise entrypoint while preserving the full loop contract through references.

Handoff: single-agent implementation in current coordinator workspace
Verification: line-count check, py_compile, self-loop L3 audit, template L2 audit, pressure eval synthetic smoke, UX skipped negative smoke, negated artifact smoke, cost smoke, skill quick_validate
Persistence: self-loop artifacts under `self/loop-runs/`, operation reference routing benchmark, installed skill sync
Scheduling: stop_success

## Execution Orchestration

Execution strategy: single-agent
Parallel domains: none for this intervention
Agent task ids: skill-md-progressive-disclosure
Worktree strategy: current coordinator workspace; no parallel file-changing agents used
Integration owner: coordinator
Conflict review: no parallel agent conflicts
Integrated verification: source `SKILL.md` 126 lines, `references/operation.md` 143 lines, source quick_validate pass, py_compile pass, self-loop audit L3 100/100, template audit L2 87/100, synthetic pressure eval PASS 10/10 across 7 cases, UX skipped pressure smoke exit 1 as expected, negated artifact audit exit 1 as expected, cost smoke OK, diff check pass, installed sync pass, installed quick_validate pass, installed self-loop audit L3 100/100, installed line-count check matches source

## Candidate Backlog

- Add live agent runner integration if Codex exposes a stable non-interactive subagent API.
- Add more pressure cases for scheduling cost caps, human gates, and scope regression.
- Add golden example transcripts for documentation-only smoke.

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

## Active Benchmark Regressions

- `false-positive-benchmark-audit-hardening`: skipped UX benchmark transcripts fail, negated artifact evidence is capped below pass, and failed-iteration promotion requires filled structured sections.
- `audit-hard-miss-exit-gate`: negated evidence and missing promoted regression cases return non-zero exit codes; self-run gates use `--min-level L3`.
- `skill-md-progressive-disclosure`: `SKILL.md` stays concise and routes full behavior to one-level reference files.

## Iteration History

- 2026-06-30T04:53:51Z: Added pressure benchmark manifest, six critical cases, transcript scorer, and self-loop artifacts; verified negative missing-transcript behavior and synthetic positive pass behavior.
- 2026-06-30T05:20:25Z: Added combined `design-taste-frontend` and `design-slop-ban` UX/UI visual-quality benchmark gate; verified source and installed skill.
- 2026-06-30T05:29:01Z: Moved self-eval suite to `benchmark/`, moved self-run artifacts to `self/loop-runs/`, and added UX/UI benchmark criteria; source verification passed.
- 2026-06-30T07:04:04Z: Added single run-log schema with Raw Run Result, Finding, and Benchmark Promotion; source and installed verification passed.
- 2026-06-30T07:17:26Z: Hardened benchmark/audit scoring against skipped checks, negated evidence, and unfilled structured fields; source and installed verification passed.
- 2026-06-30T07:45:29Z: Added audit min-level/strict gate semantics and blocking-finding non-zero exit behavior; source and installed verification passed.
- 2026-06-30T07:54:23Z: Reduced `SKILL.md` to an entrypoint and moved detailed operations contract to `references/operation.md`; source and installed verification passed.

## Human Decisions

- User requested `$loop-harness` to fix `$loop-harness`.

## User Confirmations

- Benchmark direction: pressure-test agent behavior thật.
- UX/UI benchmark direction: combine `design-taste-frontend` and `design-slop-ban`.
- Structure direction: add a dedicated `benchmark/` folder for skill behavior criteria and keep self-run artifacts out of package root.
- Run-log direction: one active run-log file per loop context; include raw errors and findings inside that file.

## Data Gaps / Instrumentation Needs

- Real pressure transcripts are not yet present. `benchmark/run_pressure_eval.py` will fail missing transcripts until actual case outputs are added.

## Next Scheduled Action

None. Run manually when a new loop-harness change needs behavior validation.
