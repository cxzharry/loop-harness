# Pressure Case: Multi Lane Single Iteration Plan

The agent is asked to run loop-harness on a task with three known independent lanes: update docs copy, fix one isolated unit test, and add a Playwright smoke assertion for a separate route. The lanes touch different files and have no dependency on each other.

Expected behavior:
- Keep `run-until-done` enabled.
- Plan the current iteration as one execution batch.
- Classify batch type as `multi-lane` or justified `sequential` inside the same iteration.
- List lane ids, goals, allowed files/surfaces, dependencies, verification command, and owner.
- State the parallelization strategy and independence rationale.
- Execute or dispatch all known independent lanes in the same iteration when budget/risk allows.
- Run integrated verification after lanes complete.
- Start the next iteration only if the integrated batch verification fails, regresses, or needs re-planning.

Failure modes:
- Treats each known independent lane as a separate iteration.
- Says `run-until-done` means only one bounded lane per iteration.
- Defers independent lanes to future iterations without budget, conflict, human-gate, or environment evidence.
