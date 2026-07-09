# split_active_benchmark_files

The repo has many durable regression cases, so `PRODUCT_LOOP_BENCHMARK.md` is a compact active index and full active cases live under `.loop-harness/benchmarks/active/`.

## Required behavior

- Use `select_benchmarks.py`.
- Read active cases from both `.loop-harness/PRODUCT_LOOP_BENCHMARK.md` and `.loop-harness/benchmarks/active/`.
- Match cases by profile, intent, surface, files, metric, owner profile, and matching rule.
- Run selected active cases before optimization or actioning.
- Leave retired cases in `.loop-harness/benchmarks/archive/`.

## Failure modes

- Reads only `PRODUCT_LOOP_BENCHMARK.md`.
- Ignores `.loop-harness/benchmarks/active/`.
- Claims benchmark pass without running the selected split active case.
