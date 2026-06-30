# Verification

Verification must be evidence-backed and profile-specific.

## Common Evidence Requirements

- Commands: exact command, directory, pass/fail, relevant output.
- Browser checks: URL, viewport, flow steps, screenshots when useful.
- Metrics: query/source, time window, baseline, sample size caveat.
- Docs/content: source-of-truth checked, link validation, generated mirrors.
- Risk: touched files/surfaces and denylist confirmation.

## Reject Conditions

Reject or escalate when:
- Tests are skipped, disabled, or weakened.
- The change touches denylisted paths without approval.
- The loop repeats the same failed attempt.
- Verification is only a claim without source evidence.
- The expected metric cannot be observed and no instrumentation is proposed.

## Profile Checks

### ux-product

- Load the actual screen when possible.
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
- Confirm build/test/lint result or explain why unavailable.
- Verify rollback/escalation path.
