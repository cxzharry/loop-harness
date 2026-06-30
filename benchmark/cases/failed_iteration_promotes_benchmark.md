# failed_iteration_promotes_benchmark

## Prompt

```text
Use loop-harness to continue the current loop after the latest verification failed.
```

## Fixture

`product-loop-run-log.md` contains a recent failed or regressed iteration.

## Expected Behavior

- Classify the failure as one of the supported error classes.
- Append raw evidence to `product-loop-run-log.md`.
- Promote durable facts into `PRODUCT_LOOP_STATE.md`.
- Create or update an active `Regression Case` in `PRODUCT_LOOP_BENCHMARK.md`.
- Include source run-log entry, trigger condition, expected result, failure evidence, matching rule, owner profile, last failed, and `Status: active`.
- Target the failed benchmark before unrelated optimization.

## Critical Failures

- Leaves failed iteration only in chat.
- Does not create active benchmark protection.
- Continues optimizing forward while the failure is unclassified.
