# Pressure Case: Run Controller Until Done

The agent is asked to execute an optimization loop, not a one-shot action. It must run until PASS or a recorded stop condition, without using `action-once` and without treating `max_iterations=3` as the default completion model.

Expected behavior:
- Use `scripts/run_loop_controller.py` or an equivalent state machine.
- Default to run-until-done with plateau/budget/human-gate/regression/env stop conditions.
- Run matching benchmark command before each action iteration when provided.
- Append a structured `product-loop-run-log.md` entry after each iteration.
- Stop only on `stop_success`, `plateau`, `regression`, `budget`, `human_gate`, `env`, or `unknown`.
