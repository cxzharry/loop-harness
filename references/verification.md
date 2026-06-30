# Verification

Verification must be evidence-backed and profile-specific.

## Common Evidence Requirements

- Commands: exact command, directory, pass/fail, relevant output.
- Browser checks: URL, viewport, flow steps, screenshots when useful.
- Metrics: query/source, time window, baseline, sample size caveat.
- Docs/content: source-of-truth checked, link validation, generated mirrors.
- Risk: touched files/surfaces and denylist confirmation.
- Parallel execution: agent task ids, conflict review, integrated verification, worktree paths when used.

## Playwright Requirement For App Evaluation

When a product surface is an app, route, local dev server, deployed page, or interactive prototype, verification must use Playwright rather than static code review alone.

Required evidence:
- Dev server command or deployed URL.
- Actual URL visited.
- Browser viewport.
- User flow steps performed.
- Assertions checked.
- Console, page, or network errors if relevant.
- Screenshot/trace path when visual or interaction quality matters.

If the app cannot be started, classify as `ENV` or `UNKNOWN` and persist the blocker. Do not pass a product optimization loop without real browser evidence when the acceptance criteria depend on UI behavior.

## Reject Conditions

Reject or escalate when:
- Tests are skipped, disabled, or weakened.
- The change touches denylisted paths without approval.
- The loop repeats the same failed attempt.
- Verification is only a claim without source evidence.
- The expected metric cannot be observed and no instrumentation is proposed.
- A matching active benchmark regression case fails.

## Benchmark Gate

Before accepting a new intervention, load `PRODUCT_LOOP_BENCHMARK.md` and run active regression cases matching the same surface, profile, changed files, or metric.

Rules:
- Run matching benchmark cases before judging new optimization success.
- If any matching active case fails, verdict is `REGRESSION`.
- Do not continue to unrelated optimization while a matching benchmark is red.
- New failures must be classified and promoted into benchmark regression cases.

## Parallel Agent Integration Checks

When execution used multiple agents:
- Confirm each task had a bounded scope, constraints, expected output, and verification command.
- Review each agent summary and changed files before integration.
- Check whether agents touched the same files, surfaces, fixtures, or state artifacts.
- Run matching active benchmark cases after integration, not only in each agent workspace.
- Run the relevant full verification suite in the coordinator workspace after integrating changes.
- Persist conflict review, integrated verification, and worktree decisions in `AGENT_HANDOFF.md`, `worktree-map.md`, and `product-loop-run-log.md`.
- If integrated verification cannot run, verdict is `UNKNOWN` or `ENV`, not `PASS`.

## Profile Checks

### ux-product

- Load the actual screen when possible.
- Use Playwright when an app/route/prototype is available.
- Verify primary task completion.
- Check responsive fit and text overflow.
- Check empty/loading/error states if relevant.

### metrics-growth

- Confirm the metric is real and queryable.
- Validate event instrumentation before optimizing.
- Do not claim metric improvement without post-change data.

### engineering-quality

- Run focused test for the changed behavior.
- Run broader tests/build when shared code changes.
- Inspect diff scope for unrelated edits.

### content-docs

- Verify facts against source files or product behavior.
- Check links and IDs.
- Preserve taxonomy, ownership, and status labels.

### release-readiness

- Smoke core flows.
- Use Playwright for browser-visible release flows.
- Confirm build/test/lint result or explain why unavailable.
- Verify rollback/escalation path.
