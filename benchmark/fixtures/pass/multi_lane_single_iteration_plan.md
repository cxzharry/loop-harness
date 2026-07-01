# Multi Lane Single Iteration Plan

Execution mode: run-until-done.

Iteration plan:
- Batch type: multi-lane.
- Execution batch: one planned batch for iteration 1.
- Parallelization strategy: three independent lanes can run together because they touch separate files/surfaces and have no shared state.
- Independence rationale: docs copy, isolated unit test, and Playwright smoke assertion have different owner boundaries and verification commands.

Lane decomposition:
- Lane id: lane-docs-copy
  - Goal: tighten docs copy.
  - Allowed files/surfaces: docs/guide.md.
  - Dependencies: none.
  - Verification command: npm run lint:docs.
  - Owner: local controller or docs agent.
- Lane id: lane-unit-test
  - Goal: fix isolated unit test failure.
  - Allowed files/surfaces: src/math.ts and src/math.test.ts.
  - Dependencies: none.
  - Verification command: npm test -- src/math.test.ts.
  - Owner: local controller or engineering agent.
- Lane id: lane-playwright-smoke
  - Goal: add one smoke assertion for a separate route.
  - Allowed files/surfaces: tests/smoke/account.spec.ts.
  - Dependencies: none.
  - Verification command: npx playwright test tests/smoke/account.spec.ts.
  - Owner: local controller or browser agent.

Integrated verification:
- Run matching active benchmark cases before accepting.
- Run npm test, npm run lint:docs, and npx playwright test tests/smoke/account.spec.ts after lanes complete.
- Integrated verification must pass before `PASS`.

Scheduling:
- Next iteration starts only if integrated batch verification fails, regresses, hits a human gate, exceeds budget, or needs re-planning.
- No independent known lane is deferred to iteration 2.
