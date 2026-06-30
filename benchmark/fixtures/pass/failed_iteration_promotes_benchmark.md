# Failed Iteration Promotes Benchmark

Verdict: FAIL
Error classification: runtime_error
The failed iteration evidence is persisted in product-loop-run-log.md, then promoted into PRODUCT_LOOP_STATE.md and PRODUCT_LOOP_BENCHMARK.md as an active Regression Case with a matching rule.

## Raw Run Result

- Verdict: FAIL
- Verification evidence: command `npm test -- checkout` failed on the checkout total assertion.
- Error output: expected total 42 but received 41.
- Failed assertions: checkout total should include service fee.

## Finding

- Finding id: finding-2026-06-30-checkout-total
- Error class: runtime_error
- Symptom: checkout total omits service fee during verification.
- Evidence: test output shows expected total 42 but received 41.
- Root cause/hypothesis: service-fee calculation lost the cart-update branch.
- Reproduction steps: run checkout total test after changing cart quantity.
- Severity: high
- Confidence: high
- Status: promoted

## Benchmark Promotion

- Promotion decision: promoted
- Benchmark case id: checkout-total-includes-service-fee
- Matching rule: checkout calculation, cart update, or total display changes.
- Expected result: checkout total includes service fee after cart quantity changes.
- Verification command: npm test -- checkout
- Status: active
