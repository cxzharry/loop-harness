# Worktree Map

Use this file when loop execution creates or reuses isolated worktrees.

## Current Run 2026-07-09T05:04:30Z

- Repo root: `<skill-source>`
- Existing linked-worktree detection: current checkout used as coordinator workspace
- Submodule check: none
- Native worktree tool or git fallback used: current workspace with disjoint agent-owned file scopes
- Project-local worktree ignore verification: `.gitignore` includes `.worktrees/`
- Integration decision: coordinator integrated public docs, sanitize, gitignore, and regression test changes before final validation and push

| Task id | Branch | Path | Agent | Status | Verification | Integration decision |
|---|---|---|---|---|---|---|
| public-release-docs | current | <skill-source> | Euclid | integrated | README/LICENSE readback | accepted |
| public-path-sanitize | current | <skill-source> | Halley | integrated | sanitize grep, run-log validator, strict self audit | accepted |
| github-readiness-ignore | current | <skill-source> | Pasteur | integrated | git/gh readiness checks | accepted |
| public-release-hygiene-test | current | <skill-source> | coordinator | integrated | targeted public hygiene regression test | accepted |

## Current Run 2026-07-09T04:45:18Z

- Repo root: `<skill-source>`
- Existing linked-worktree detection: current checkout used as coordinator workspace
- Submodule check: none
- Native worktree tool or git fallback used: current workspace
- Project-local worktree ignore verification: existing `.worktrees/` ignore convention preserved
- Integration decision: coordinator applied assigned-file docs and self-loop persistence edits in place

| Task id | Branch | Path | Agent | Status | Verification | Integration decision |
|---|---|---|---|---|---|---|
| watchdog-scheduler-semantics | current | <skill-source> | coordinator | integrated | run-log validator and strict self audit | docs-only scheduler semantics persisted |

## Current Run 2026-07-09T04:17:58Z

- Repo root: `<skill-source>`
- Existing linked-worktree detection: current checkout used as coordinator workspace
- Submodule check: none
- Native worktree tool or git fallback used: not required because audit agents were read-only
- Project-local worktree ignore verification: existing `.worktrees/` ignore convention preserved
- Integration decision: coordinator applied edits in the main workspace after parallel audit findings completed

| Task id | Branch | Path | Agent | Status | Verification | Integration decision |
|---|---|---|---|---|---|---|
| galileo-evaluation-contract-audit | not_applicable | not_applicable | Galileo | integrated | criteria scaffold and evaluation-contract pressure tests | findings implemented by coordinator |
| raman-benchmark-scale-audit | not_applicable | not_applicable | Raman | integrated | split active selector/audit/controller tests | findings implemented by coordinator |
| noether-self-pressure-coverage-audit | not_applicable | not_applicable | Noether | integrated | pressure eval 18/18 | findings implemented by coordinator |

## Isolation Check

- Repo root: `<skill-source>`
- Already in linked worktree: no at start; feature worktree created
- Submodule check: none
- Native worktree tool available: none in this environment
- Fallback used: `git worktree`
- Project-local worktree directory ignored: yes, `.worktrees/probe` matched `.gitignore`

## Worktrees

| Task id | Branch | Path | Agent | Status | Verification | Integration decision |
|---|---|---|---|---|---|---|
| self-behavior-benchmark-scaffold | loop-harness-behavior-benchmarks | .worktrees/loop-harness-behavior-benchmarks | coordinator | integrated | py_compile, audit, quick_validate, cost, pressure eval smoke | merge after validation |

## Cleanup

- Branches merged:
- Worktrees removed:
- Worktrees retained: `.worktrees/loop-harness-behavior-benchmarks` until final merge
- Cleanup blocker: none
