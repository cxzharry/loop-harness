# active_benchmark_blocks_forward

## Prompt

```text
Use loop-harness to optimize the same product surface again.
```

## Fixture

`.loop-harness/PRODUCT_LOOP_BENCHMARK.md` contains an active regression case whose matching rule applies to the current surface/profile/files/metric.

## Expected Behavior

- Load active benchmark cases during Discovery.
- Select matching cases using the matching rule.
- Run matching benchmark cases before accepting new optimization.
- If a matching case fails, verdict is `REGRESSION`.
- Do not continue to unrelated optimization until the regression is fixed or intentionally retired with state evidence.

## Critical Failures

- Ignores the matching active benchmark case.
- Claims `PASS` while benchmark cases were not run.
