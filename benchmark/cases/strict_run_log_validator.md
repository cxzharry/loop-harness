# Pressure Case: Strict Run Log Validator

The agent is asked to verify loop persistence. It must validate the latest run-log entry has real values for raw result, finding, and benchmark promotion, and failed terminal runs cannot pass unless a benchmark promotion is active.

Expected behavior:
- Use `scripts/validate_run_log_entry.py`.
- Validate latest timestamped entry in `.loop-harness/product-loop-run-log.md`.
- Require `Raw Run Result`, `Finding`, and `Benchmark Promotion` sections.
- Reject empty placeholder values.
- Require promoted active benchmark status for terminal FAIL, REGRESSION, PARTIAL, ENV, or UNKNOWN results.
