## Transcript

I used `scripts/run_loop_controller.py --repo /tmp/product-repo --benchmark-command "npm test -- benchmark" --command "npm test -- app-flow" --target-score 8 --plateau-patience 3`.

Execution mode was `run-until-done`; no one-shot action mode was used and no fixed three-iteration cap was treated as completion. The controller ran the matching benchmark command before each action iteration, appended `.loop-harness/product-loop-run-log.md` after each iteration, and stopped on `stop_success` when the command returned PASS with `SCORE=9`.

Recognized stop conditions are `stop_success`, `plateau`, `regression`, `budget`, `human_gate`, `env`, and `unknown`.
