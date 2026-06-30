# Global Promotion Requires Gate

Persistence considered reusable knowledge after repo-local evidence existed.

- Tool: promote_global_knowledge.py
- Source: .loop-harness/product-loop-run-log.md
- Evidence chain: Raw Run Result, Finding, and Benchmark Promotion are present.
- Promotion gate: validates finding fields, benchmark promotion fields, active repo benchmark status, and evidence quality.
- Destination: passing candidates go to ~/.codex/loop-harness/knowledge/inbox/ first.
- Approval: writing to promoted/ requires --promote or explicit approval after review.
- Blocked cases: noise, env blocker, missing evidence, not promoted repo findings, inactive benchmarks, and domain-specific failures are rejected or not promoted.
- Result: not promoted globally until gate and approval are satisfied.

