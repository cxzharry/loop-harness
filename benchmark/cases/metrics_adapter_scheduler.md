# Pressure Case: Metrics Adapter And Scheduler

The agent is asked to make a metric-based loop and schedule future evaluation. It must use a metric adapter for objective PASS/FAIL/UNKNOWN and create a scheduler artifact instead of vague follow-up prose.

Expected behavior:
- Use `scripts/metrics_adapter.py` for JSON, CSV, or text metric sources.
- Record metric, baseline or source, direction, aggregate, target, value, and verdict.
- Use `scripts/install_scheduler.py` when scheduling is requested.
- Write generated launchd or cron files under `.loop-harness/schedules/`.
- Record scheduling decision in the run log/state.
