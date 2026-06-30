# worktree_isolation

## Prompt

```text
Use loop-harness to run independent file-changing tasks in parallel.
```

## Fixture

The repo is a normal git checkout. Parallel agents will edit files.

## Expected Behavior

- Detect whether the current checkout is already a linked worktree.
- Run the submodule guard before treating `GIT_DIR != GIT_COMMON` as worktree isolation.
- Prefer native worktree tooling if available.
- Fall back to `git worktree` only when no native worktree tool exists.
- Verify project-local `.worktrees/` or `worktrees/` is ignored before creating worktrees.
- Record task-to-worktree mapping in `.loop-harness/worktree-map.md`.
- If worktree creation fails, persist the blocker and run sequentially or report-only.

## Critical Failures

- Creates worktree without ignore verification.
- Creates nested worktree inside an existing linked worktree.
- Loses task-to-branch/path mapping.
