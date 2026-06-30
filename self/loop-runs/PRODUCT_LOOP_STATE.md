# Product Loop State

Last run: 2026-06-30T05:29:01Z
Intent: ENGINEERING_QUALITY
Primary metric: pressure benchmark case score
Baseline window: before `benchmark/` behavior benchmark scaffold
Execution mode: run-until-done
Current iteration: 3
Target: all critical pressure benchmark cases score `>=8/10`
Latest verdict: PASS
Stop condition: SUCCESS

## Active Opportunity

Separate runtime skill resources from self-eval benchmarks and self-run loop artifacts so the package root is not ambiguous.

Handoff: single-agent implementation in current coordinator workspace
Verification: py_compile, self-loop audit, template audit, pressure eval synthetic smoke, skill quick_validate
Persistence: self-loop artifacts under `self/loop-runs/`, benchmark folder, installed skill sync
Scheduling: stop_success; keep benchmark criteria under `benchmark/` and self-run artifacts under `self/loop-runs/`

## Execution Orchestration

Execution strategy: single-agent
Parallel domains: none for this intervention
Agent task ids: package-structure-benchmark-folder
Worktree strategy: current coordinator workspace; no parallel file-changing agents used
Integration owner: coordinator
Conflict review: no parallel agent conflicts
Integrated verification: py_compile pass, package root self-artifact check pass, self-loop audit L3 100/100, template audit L2 87/100, source quick_validate pass, synthetic pressure eval PASS 10/10 across 7 cases, missing-transcript negative smoke FAIL as expected, cost smoke OK, installed sync pass, installed quick_validate pass, installed self-loop audit L3 100/100, installed root self-artifact check pass

## Candidate Backlog

- Add live agent runner integration if Codex exposes a stable non-interactive subagent API.
- Add more pressure cases for scheduling cost caps, human gates, and scope regression.
- Add golden example transcripts for documentation-only smoke.

## Watch List

- Pressure eval script should not pretend to run agents; it scores real transcripts only.
- Self-loop artifacts under `self/loop-runs/` should not replace the skill package contract.
- Package root should not contain self-run `PRODUCT_LOOP*`, handoff, budget, run-log, or worktree-map files.

## Failed Attempts / Do Not Retry

- Do not rely only on `product_loop_audit.py` for behavior quality.
- Do not mark pressure behavior pass without transcript evidence.
- Do not claim UX/UI visual-quality PASS from Playwright alone when visual quality matters.
- Do not put skill self-run logs or state back at package root.

## Active Benchmark Regressions

None.

## Iteration History

- 2026-06-30T04:53:51Z: Added pressure benchmark manifest, six critical cases, transcript scorer, and self-loop artifacts; verified negative missing-transcript behavior and synthetic positive pass behavior.
- 2026-06-30T05:20:25Z: Added combined `design-taste-frontend` and `design-slop-ban` UX/UI visual-quality benchmark gate; verified source and installed skill.
- 2026-06-30T05:29:01Z: Moved self-eval suite to `benchmark/`, moved self-run artifacts to `self/loop-runs/`, and added UX/UI benchmark criteria; source verification passed.

## Human Decisions

- User requested `$loop-harness` to fix `$loop-harness`.

## User Confirmations

- Benchmark direction: pressure-test agent behavior thật.
- UX/UI benchmark direction: combine `design-taste-frontend` and `design-slop-ban`.
- Structure direction: add a dedicated `benchmark/` folder for skill behavior criteria and keep self-run artifacts out of package root.

## Data Gaps / Instrumentation Needs

- Real pressure transcripts are not yet present. `benchmark/run_pressure_eval.py` will fail missing transcripts until actual case outputs are added.

## Next Scheduled Action

None. Run manually when a new loop-harness change needs behavior validation.
