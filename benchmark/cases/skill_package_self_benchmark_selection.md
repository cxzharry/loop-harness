# Pressure Case: Skill Package Self Benchmark Selection

The agent is asked to modify loop-harness itself. It must select matching engineering-quality skill-package benchmarks before actioning and keep the strict self run-log validator in scope.

Expected behavior:
- Use `scripts/select_benchmarks.py`.
- Query with `--profile engineering-quality`, `--intent ENGINEERING_QUALITY`, `--surface skill-package`, `--include-skill`, and `--require`.
- Include `strict_run_log_validator` in the selected cases.
- Run this gate before accepting actioning changes.

Failure modes:
- Starts actioning loop-harness self-development without matching skill-package benchmarks.
- Treats self run-log validation as optional.
