# Product Loop Patterns

Use these patterns to avoid generic "improve the product" loops. Pattern details live in `assets/templates/product-loop-patterns.json` so scripts can read the same source.

## daily-product-triage

Low-risk recurring scan of UX, errors, docs, and feedback. Start here for new products.

Default mode: L1 report-only.

Best when the user asks for broad product improvement without a single metric target.

## ux-sweeper

Systematic UX pass over one route, flow, or prototype. It checks task completion, responsive fit, copy, loading/empty/error states, and accessibility.

Default mode: L2 assisted.

Best when a visual/product surface needs quality improvement.

## metric-instrumentation

Find missing or unreliable analytics before claiming growth improvement. It maps events, validates logging, and proposes instrumentation.

Default mode: L1 report-only until data quality is proven.

Best when metrics are absent, stale, or not trustworthy.

## release-readiness

Pre-ship loop for changed surfaces. It discovers risk, checks core flows, verifies tests/build/smoke, and escalates unsafe changes.

Default mode: L2 assisted.

Best before deployment or release.

## post-launch-learning

After launch, read metrics, feedback, support issues, and errors. Produce learnings, follow-up candidates, and do-not-retry notes.

Default mode: L1 report-only, then L2 for bounded follow-ups.

Best after a shipped feature or experiment.

## Choosing A Pattern

- Unknown product quality problem: `daily-product-triage`.
- Known screen or user flow: `ux-sweeper`.
- Growth goal without reliable analytics: `metric-instrumentation`.
- Shipping soon: `release-readiness`.
- Feature already launched: `post-launch-learning`.
