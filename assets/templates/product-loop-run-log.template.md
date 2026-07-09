# Product Loop Run Log

Append one recent entry per loop run. Keep raw errors, findings, and benchmark promotion decisions in this single file; do not create a separate error log or findings file. When the log grows large, move detailed historical entries under `runs/archive/` and keep archive pointers here.

## Entries

### YYYY-MM-DDTHH:MM:SSZ

#### Raw Run Result

- Profile:
- Discovery signals:
- Handoff:
- Selected intervention:
- Execution strategy:
- Agent tasks:
- Worktree map:
- Conflict review:
- Integration verification:
- Verification evidence:
- Playwright evidence:
  - URL:
  - Viewport:
  - Flow steps:
  - Assertions:
  - Screenshot/trace:
- Error output:
- Failed assertions:
- Verdict:
- Files changed:
- Next scheduling decision:

#### Finding

- Finding id:
- Error class: none | ui_regression | runtime_error | metric_regression | content_drift | env_blocker | scope_regression
- Symptom:
- Evidence:
- Root cause/hypothesis:
- Reproduction steps:
- Severity: none | low | medium | high | critical
- Confidence: low | medium | high
- Status: open | promoted | dismissed | resolved | not_applicable

#### Benchmark Promotion

- Promotion decision: promoted | not_promoted
- Benchmark case id:
- Matching rule:
- Expected result:
- Verification command:
- Status: active | retired | not_applicable
- State promoted:
- Benchmark promoted:
