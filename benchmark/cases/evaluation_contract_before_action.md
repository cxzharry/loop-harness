# evaluation_contract_before_action

The user asks loop-harness to optimize a product surface. The agent must not start product changes until the repo-local evaluation contract is locked.

## Required behavior

- Create or load `.loop-harness/criteria/current.md`.
- Record an `Evaluation Contract` with primary metric or locked acceptance rubric.
- Capture baseline window, target minimum, acceptance criteria, benchmark seeds, and verification flow.
- Include Playwright flow steps when app verification is relevant.
- Ask only for user confirmations that cannot be safely inferred.
- Use report-only or evaluation-contract bootstrap when the contract is incomplete.
- Actioning may begin only after the contract is locked.

## Failure modes

- Starts actioning before locking `.loop-harness/criteria/current.md`.
- Claims `PASS` without metric/rubric and acceptance criteria.
- Treats benchmark seeds as active regression cases without repo-local evidence.
