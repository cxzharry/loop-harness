## Transcript

I detected intent `UX_OPTIMIZE` for the checkout web-route and loaded `.loop-harness/criteria/current.md` before product changes.

## Evaluation Contract

- Contract status: locked
- Product surface: checkout web-route
- Primary metric: checkout completion
- Baseline window: last 7 days or current visible-flow smoke when analytics are unavailable
- Target minimum: checkout visible-flow passes on desktop and mobile with no blocking console error
- Acceptance Criteria: submit CTA remains visible, validation errors are announced, and successful checkout reaches the confirmation state
- Benchmark seeds: checkout-visible-flow and prior checkout-submit-regression seed
- Playwright flow steps: open `/checkout`, fill required fields, submit, assert confirmation state and no blocking console/network error
- User confirmation: target and human gate were safely inferred from the user request and repo state

Before actioning, I selected matching benchmark seeds and locked this contract. If any metric, target, criteria, benchmark seed, or verification source had remained unresolved, I would have used report-only evaluation-contract bootstrap instead of product changes.
