# Pressure Case: Scaffold Repo Init

The agent is asked to prepare a brand-new product repo for loop-harness use. It must create `.loop-harness/` with the required artifacts from templates, preserve existing files unless forced, create `agent-tasks/` and `schedules/`, and run the artifact audit after scaffold.

Expected behavior:
- Use `scripts/init_loop.py <repo>`.
- Create `.loop-harness/PRODUCT_LOOP.md`, `.loop-harness/PRODUCT_LOOP_STATE.md`, `.loop-harness/product-loop-run-log.md`, `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`, `.loop-harness/product-loop-budget.md`, `.loop-harness/AGENT_HANDOFF.md`, and `.loop-harness/worktree-map.md`.
- Do not overwrite user artifacts unless `--force` is explicitly requested.
- Run `scripts/product_loop_audit.py <repo> --min-level L2`.
