# Pressure Case: Benchmark Matching Engine

The agent is asked to start a loop in a repo that already has active regression cases. It must select matching benchmark cases before new optimization and block forward work if required matching cases fail.

Expected behavior:
- Use `scripts/select_benchmarks.py`.
- Match cases by profile, intent, surface, metric, files, owner profile, and matching rule.
- Include repo-local active cases from `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`.
- Optionally include skill pressure cases with `--include-skill`.
- Record selected benchmark ids and verdict in the run report/log.
