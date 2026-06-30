# Optimization Profiles

Use profiles to keep product optimization concrete. Select the smallest set that covers the user's goal.

## ux-product

Use for product surface quality: flows, layout, copy, accessibility, friction, empty states, mobile/desktop fit, first-run experience.

Discovery:
- Inspect the live route or prototype.
- Capture screenshots when visual quality matters.
- Check common paths, empty/error/loading states, and responsiveness.

Verification:
- Browser smoke and screenshot review.
- Accessibility checks when available.
- Confirm text fits and core tasks can be completed.

## metrics-growth

Use for activation, conversion, retention, completion rate, funnel movement, onboarding drop-off, or growth experiments.

Before actioning, confirm the primary metric, baseline window, target threshold, and whether proxy evidence is acceptable while waiting for real post-change data.

Discovery:
- Query real analytics or logs when available.
- Identify event taxonomy and baseline windows.
- If metrics are absent, propose instrumentation before optimization.

Verification:
- Validate event firing and data quality.
- Compare against baseline only when enough data exists.
- For low traffic, use proxy checks and mark metric result pending.

## engineering-quality

Use for bugs, CI failures, performance, reliability, security-adjacent hygiene, regressions, and maintainability that blocks product quality.

Discovery:
- Read CI, tests, logs, recent commits, error reports, performance traces.

Verification:
- Run focused tests first, then broader checks if risk warrants.
- Confirm no unrelated changes or disabled tests.
- Record exact commands and outcomes.

## content-docs

Use for PRD, SRS, help docs, onboarding, changelog, release notes, product specs, support-facing content.

Discovery:
- Compare docs to actual product behavior and source-of-truth contracts.
- Identify ambiguity, stale facts, broken links, and missing states.

Verification:
- Validate facts, IDs, dates, links, examples, and generated mirrors.
- Preserve existing taxonomy and ownership boundaries.

## release-readiness

Use before shipping or deploying.

Discovery:
- Identify changed surfaces, risky paths, migrations, flags, and user-visible flows.

Verification:
- Smoke core flows.
- Run build/test/lint as appropriate.
- Check rollback and human gate criteria.

## Profile Selection Heuristic

- If the user says "make the product better" with no metric, start with `ux-product` plus `engineering-quality`.
- If the user says "optimize conversion/activation/retention", use `metrics-growth` plus `ux-product`.
- If the user says "before release/deploy", use `release-readiness` plus `engineering-quality`.
- If the product surface is documentation or specs, use `content-docs`.
