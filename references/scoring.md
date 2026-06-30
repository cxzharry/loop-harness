# Scoring

## Candidate Prioritization

Score each candidate 1-5.

| Criterion | Meaning |
|---|---|
| Impact | User/product/business value if fixed |
| Confidence | Evidence quality and causal clarity |
| Effort | Lower implementation and verification cost scores higher |
| Risk | Lower safety/product/reversibility risk scores higher |

Recommended priority:

```text
priority = impact + confidence + effort + risk
```

Break ties by choosing the candidate with stronger verification evidence.

## Loop Readiness Levels

| Level | Meaning | Minimum bar |
|---|---|---|
| L0 | Draft | `PRODUCT_LOOP.md` describes goal/scope |
| L1 | Report-only | Discovery writes state; no source changes |
| L2 | Assisted optimization | Bounded changes with independent verification |
| L3 | Scheduled/unattended-capable | State, run log, budget, verifier, human gates, proven activity |

Never start at L3. Run at least one L1 loop and review state before enabling actioning behavior.

## Pattern Readiness

A reusable product loop pattern should define:
- `id`, `name`, `goal`, `profiles`, `cadence`, `risk`, and `default_level`.
- All five phases: discovery, handoff, verification, persistence, scheduling.
- Human gates.
- Cost fields: noop, report, action, daily cap, and early-exit requirement.

Use `scripts/product_loop_cost.py` before scheduling a pattern.

## Verdict Criteria

Use `PASS` only when evidence matches the profile's success condition.

Use `PARTIAL` when a bounded improvement landed but the product outcome is not yet proven.

Use `FAIL` when checks fail, scope expands unexpectedly, or the evidence contradicts the hypothesis.

Use `UNKNOWN` when data or environment prevents judgment.

## Run-Until-Done Criteria

Use run-until-done only when the loop has:
- A measurable target or locked acceptance rubric.
- Confirmed primary metric when the target is metric-based.
- A safety budget or kill switch.
- Plateau patience for repeated no-improvement iterations.
- Stop conditions.
- State fields for current iteration, latest verdict, and what not to retry.

Do not classify a scheduled loop as L3 if it cannot stop itself on success, plateau, regression, budget, human gate, or repeated environment failure.
