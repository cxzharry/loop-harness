# parallel_agents_independent

## Prompt

```text
Use loop-harness to fix these three unrelated product quality failures as fast as possible.
```

## Fixture

There are three independent domains, such as separate test files, separate product surfaces, or unrelated bugs with no shared files or state.

## Expected Behavior

- Decide whether domains are truly independent before dispatching.
- Use `parallel-agents` only when independence is justified.
- Create one focused task per domain.
- Each task includes scope, goal, constraints, expected output, verification command, and allowed files/surfaces.
- Persist tasks in `AGENT_HANDOFF.md` or `agent-tasks/<task-id>.md`.
- Review returned summaries and changed files for conflicts.
- Run integrated verification after merging or applying agent outputs.

## Critical Failures

- Dispatches parallel agents for shared-state work.
- Accepts agent summaries without coordinator verification.
- Does not persist handoff.
