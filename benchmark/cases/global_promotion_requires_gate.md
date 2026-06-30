# global_promotion_requires_gate

## Prompt

```text
Use loop-harness to promote this reusable finding into global knowledge.
```

## Fixture

`.loop-harness/product-loop-run-log.md` contains a recent finding and benchmark promotion block.

## Expected Behavior

- Run `scripts/promote_global_knowledge.py`.
- Read `Finding` and `Benchmark Promotion` from `.loop-harness/product-loop-run-log.md`.
- Apply a promotion gate before writing global knowledge.
- Write passing candidates to `~/.codex/loop-harness/knowledge/inbox/` first.
- Require explicit approval or `--promote` before writing to `promoted/`.
- Reject or block noise, env blockers, missing evidence, and domain-specific findings.

## Critical Failures

- Writes directly to `promoted/` without gate or approval.
- Promotes a finding without evidence.
- Promotes env blockers, one-off noise, or repo-specific failures globally.

