# Verification

Verification must be evidence-backed and profile-specific.

## Common Evidence Requirements

- Commands: exact command, directory, pass/fail, relevant output.
- Browser checks: URL, viewport, flow steps, screenshots when useful.
- Metrics: query/source, time window, baseline, sample size caveat.
- Docs/content: source-of-truth checked, link validation, generated mirrors.
- Risk: touched files/surfaces and denylist confirmation.
- Parallel execution: agent task ids, conflict review, integrated verification, worktree paths when used.
- UX/UI quality: Playwright evidence plus `design-taste-frontend` and `design-slop-ban` benchmark results when visual quality, product comprehension, landing-page quality, redesign quality, or conversion experience matters.

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

## UX Taste And Slop Benchmark

Playwright proves that a browser surface loads and behaves; it does not prove that the UI is good. When a run touches a visible product surface, combine runtime evidence with design quality gates.

Use `design-taste-frontend` for:
- Landing pages, portfolios, marketing sites, redesigns, and conversion-focused web surfaces.
- Brief inference, design read, visual differentiation, hierarchy, composition, copy fit, and taste scoring.

Use `design-slop-ban` for:
- Websites, landing pages, web apps, mobile UI, redesigns, design systems, UI copy, hero sections, motion, accessibility, and visible product screens.
- Strict linting against generic AI visuals, weak hierarchy, broken responsive behavior, inaccessible controls, fake product UI, and overexplained in-app text.

For dashboards, admin panels, data tables, multi-step product tools, and dense operational UI, record that the full `design-taste-frontend` landing-page rubric is not directly applicable. Still run the relevant `design-slop-ban` checks and any applicable taste checks for hierarchy, visual confidence, copy clarity, responsive fit, and product specificity.

UX/UI verification PASS requires:
- Playwright evidence when an app, route, local dev server, deployed page, or prototype exists.
- Viewport coverage for the primary desktop and mobile states affected by the change.
- A visible-flow assertion, not only a static screenshot.
- Taste/slop score `>=8/10` when visual quality matters.
- No critical slop violation.
- Any non-applicability decision recorded with a reason.

Critical slop failures include:
- Claiming UX PASS from static code review when the surface can be opened.
- Skipping the design read or visual benchmark for a visual-quality intervention.
- Generic AI-default styling: purple/blue neon gradients, beige/brass luxury defaults, decorative blobs/orbs, fake glassmorphism, or stock-card layouts unrelated to the product.
- Oversized hero or panel type that wraps awkwardly, hides the next section, or overwhelms the actual product.
- Text overflow, clipped controls, CTA wrapping, or overlapping UI at target viewports.
- Weak contrast, keyboard-inaccessible controls, missing focus states, or motion with no reduced-motion handling.
- Placeholder screenshots, fake product interfaces, hand-rolled icons when the project has an icon library, or visible explanatory text that describes how to use the interface instead of making it usable.
- Duplicate CTA intent, ambiguous action labels, or UI copy containing em/en dashes in visible customer-facing text.

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
- For visual UI work, run the combined `design-taste-frontend` plus `design-slop-ban` benchmark and require score `>=8/10` with no critical slop violation.
- If `design-taste-frontend` is not the right rubric for the surface, record why and still apply `design-slop-ban` plus relevant hierarchy, copy, responsive, and product-specificity checks.

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
