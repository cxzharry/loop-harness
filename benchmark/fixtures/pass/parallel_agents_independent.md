# Parallel Agents Independent

The failures are independent domains with an explicit independence rationale: checkout copy, docs link validation, and isolated unit-test failure touch separate files and surfaces.

- Execution strategy: parallel-agents.
- Handoff: AGENT_HANDOFF.md records one task per domain.
- Task scope and constraints: each task lists allowed files, forbidden shared state, and rollback condition.
- Expected output: root cause/hypothesis, changed files, verification evidence, risks, and next handoff.
- Verification command: each task has a focused command and the coordinator runs integrated verification after merge.
- Conflict review: coordinator checks changed files and shared surfaces before integration.
- Integrated verification: full benchmark and focused tests pass in the coordinator workspace.

