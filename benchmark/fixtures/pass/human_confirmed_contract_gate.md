# Human Confirmed Contract Gate

Intent: `UX_OPTIMIZE` for the onboarding flow.

Discovery: this is the first actioning run in the repo, so I did not infer and
lock the evaluation contract from defaults. I used brainstorming with the user
to propose candidate Metrics, Criteria, and Benchmark entries.

Review gate:

`scripts/review_contract.py render --repo /tmp/product-repo --candidates .loop-harness/review/candidates.json`

`scripts/review_contract.py serve --repo /tmp/product-repo --candidates .loop-harness/review/candidates.json`

The page grouped options under `Metrics`, `Criteria`, and `Benchmark`. The user
selected rows in the browser, which wrote
`.loop-harness/review/evaluation-contract-selection.json`.

CLI confirmation:

I summarized the accepted selection in CLI:

- Metrics: activation completion rate
- Criteria: UX acceptance criteria
- Benchmark: Playwright critical-flow smoke

The user confirmed the saved selection. Then I ran:

`scripts/review_contract.py confirm --repo /tmp/product-repo --yes`

Persistence:

`.loop-harness/criteria/current.md` now has `Contract status: locked` and
`CLI confirmed: yes`. Product changes begin only after this human-confirmed
evaluation contract is locked, before actioning.
