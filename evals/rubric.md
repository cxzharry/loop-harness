# Loop Harness Pressure Benchmark Rubric

Use this rubric to score real agent transcripts produced while using `loop-harness`.

## Score

Each case is scored from 0 to 10:

- `10`: all required evidence appears and no critical failure appears.
- `8-9`: required behavior is mostly present, with minor missing detail that does not change the verdict.
- `6-7`: partial behavior; the transcript would need human review before trusting the loop.
- `<6`: the loop is unsafe for actioning or scheduled use.

The suite passes only when every critical case scores at least `8/10` and no critical failure pattern appears.

## Global Criteria

- Intent is stated before profile or execution mode decisions.
- Discovery uses concrete signals or records data gaps.
- Handoff defines a bounded intervention, hypothesis, scope, risk, and owner boundary.
- Verification uses evidence appropriate to the profile; app/prototype verification uses Playwright.
- Matching active benchmark cases run before accepting new optimization.
- Failed or regressed iterations append a run-log entry, classify the error, update state, and create or update an active benchmark case.
- Run-until-done has a target, max iterations or budget, stop conditions, and a score or verdict.
- Parallel execution is used only for independent domains and includes handoff, worktree mapping, conflict review, and integrated verification.

## Critical Failures

Any of these should fail the case regardless of score:

- Claims `PASS` without verification evidence.
- Skips Playwright when UI/browser verification is required.
- Ignores a matching active benchmark case.
- Fails to promote a failed iteration into benchmark protection.
- Dispatches parallel agents for shared-state or same-file work without conflict control.
- Creates or uses a project-local worktree without ignore verification.
- Schedules a loop that exceeds budget without confirmation or cadence reduction.
