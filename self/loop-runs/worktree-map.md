# Worktree Map

Use this file when loop execution creates or reuses isolated worktrees.

## Isolation Check

- Repo root: `/Users/haido/loop-harness`
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
