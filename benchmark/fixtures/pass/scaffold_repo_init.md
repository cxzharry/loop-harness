## Transcript

I detected a new product repo and scaffolded `.loop-harness/` with `scripts/init_loop.py /tmp/product-repo`.

- Created `.loop-harness/PRODUCT_LOOP.md`
- Created `.loop-harness/PRODUCT_LOOP_STATE.md`
- Created `.loop-harness/product-loop-run-log.md`
- Created `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`
- Created `.loop-harness/product-loop-budget.md`
- Created `.loop-harness/criteria/current.md`
- Created `.loop-harness/AGENT_HANDOFF.md`
- Created `.loop-harness/worktree-map.md`
- Created `.loop-harness/agent-tasks/`
- Created `.loop-harness/schedules/`
- Created `.loop-harness/benchmarks/active/`
- Created `.loop-harness/benchmarks/archive/`
- Created `.loop-harness/runs/`
- Created `.loop-harness/runs/archive/`

Existing user artifacts were kept because `--force` was not requested. Then I ran `scripts/product_loop_audit.py /tmp/product-repo --min-level L2`; the scaffold reached L2.
