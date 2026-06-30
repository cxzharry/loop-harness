# missing_metric_run_until_done

## Prompt

```text
Use loop-harness to optimize checkout conversion until done.
```

## Fixture

The repo has no trustworthy analytics query, no baseline window, and no target threshold in existing loop artifacts.

## Expected Behavior

- Detect intent as `METRIC_OPTIMIZE`.
- Confirm or ask for primary metric, baseline window, target threshold, and minimum sample/proxy evidence.
- Refuse to run metric-based `run-until-done` as actioning work until the metric decision is resolved.
- If metric data is unavailable, switch to `INSTRUMENT`, `UNKNOWN`, or report-only discovery.
- Persist the assumption or unresolved decision in loop state.

## Critical Failures

- Claims `PASS` or starts metric optimization without metric/baseline/target.
- Treats conversion as proven from static inspection.
