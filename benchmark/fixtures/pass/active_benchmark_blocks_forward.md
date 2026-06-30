# Active Benchmark Blocks Forward

Discovery loaded the matching active benchmark case and applied its matching rule before any new optimization work was accepted.

- Active benchmark: checkout-error-regression
- Matching rule: current surface, profile, and changed files overlap the active case.
- Benchmark verdict: PASS
- Result: benchmark passed before accepting optimization.
- Scheduling: if this benchmark returned REGRESSION, it would blocks forward work and the loop would fix that case first.

