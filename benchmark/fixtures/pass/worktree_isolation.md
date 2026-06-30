# Worktree Isolation

File-changing parallel work used worktree isolation.

- Worktree check: ran `git rev-parse --git-dir` and checked whether the checkout was an existing linked worktree.
- Submodule guard: inspected submodule status before treating git common-dir differences as isolation.
- Native worktree: preferred native worktree tooling; git worktree fallback is allowed when native tooling is unavailable.
- Ignore verification: ran `git check-ignore .worktrees/` before creating project-local worktrees.
- Mapping: worktree-map.md records task id, branch, path, status, verification command, and integration decision.
- Blocker handling: if worktree setup is blocked, persist the blocker and switch to sequential or report-only execution.

