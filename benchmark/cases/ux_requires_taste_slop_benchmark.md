# Case: UX Requires Taste And Slop Benchmark

## Prompt

Use `$loop-harness` to improve the first-run onboarding route of a web app. The app can be started locally. The goal is better user comprehension and a more polished UI.

## Fixture

- Surface: local web app route `/onboarding`
- Profile: `ux-product`
- The agent changes visible layout, typography, copy, empty states, or navigation.
- Playwright can open the route.

## Expected Behavior

- State intent as `UX_OPTIMIZE`.
- Use `run-until-done` for actioning changes.
- Open the app with Playwright when available.
- Record URL, viewport, flow steps, visible-flow assertions, and screenshot or trace evidence when visual quality matters.
- Apply `design-taste-frontend` when the surface is marketing, onboarding, redesign, portfolio, or conversion-oriented.
- Apply `design-slop-ban` for visible UI linting.
- Require taste/slop score `>=8/10`.
- Require no critical slop violation before claiming `PASS`.
- If the full taste rubric is not applicable, record the reason and still run relevant slop, hierarchy, copy, responsive, accessibility, and product-specificity checks.
- Persist any fail/error into `product-loop-run-log.md`, `PRODUCT_LOOP_STATE.md`, and `PRODUCT_LOOP_BENCHMARK.md`.

## Critical Failures

- Claims `PASS` from static review while Playwright could open the route.
- Claims `PASS` with no taste benchmark.
- Claims `PASS` with no slop benchmark.
- Uses only a screenshot without visible-flow assertions.
- Ignores text overflow, contrast, CTA wrapping, duplicated CTA intent, generic AI visual defaults, or mobile collapse failures.
- Fails to promote a visual regression into an active benchmark case.
