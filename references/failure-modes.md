# Failure Modes

## Generic Optimization

Symptom: The loop suggests broad improvements without evidence.

Fix: Return to Discovery. Require real signal and one bounded hypothesis.

## Metric Theater

Symptom: The loop claims conversion or retention improvement without data.

Fix: Mark result `UNKNOWN`; add instrumentation or wait for a valid window.

## UX Churn

Symptom: The loop repeatedly redesigns surfaces based on taste.

Fix: Require a task, user segment, friction signal, and verification path.

## Verification Debt

Symptom: Changes accumulate faster than checks.

Fix: Pause actioning; run release-readiness and engineering-quality verification.

## State Rot

Symptom: State references resolved issues, stale routes, or obsolete metrics.

Fix: Prune state during Discovery before selecting new work.

## Token Blowout

Symptom: Frequent scheduled loops run full scans without actionable findings.

Fix: Add early exit, lower cadence, and budget checks.

## Cognitive Surrender

Symptom: Humans stop reviewing medium-risk product decisions.

Fix: Reinstate human gates and report-only mode for ambiguous product direction.

## Endless Optimization Loop

Symptom: The loop keeps changing the product after evidence has stopped improving.

Fix: Use run-until-done stop conditions: SUCCESS, EXHAUSTED, PLATEAU, REGRESSION, BUDGET, HUMAN_GATE, ENV, UNKNOWN.

## Implementation-Only Loop

Symptom: The loop repeats edits without rerunning discovery, persistence, or scheduling.

Fix: Require every iteration to execute all five phases, then record the verdict and next targeted criterion.
