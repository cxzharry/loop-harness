# UX/UI Benchmark Criteria

Use this criteria file when scoring `loop-harness` transcripts for visible product UI work.

## Required Gates

- Intent is classified as `UX_OPTIMIZE` or includes `ux-product`.
- App, route, prototype, or deployed page verification uses Playwright when the surface can be opened.
- Evidence includes URL, viewport, flow steps, visible assertions, and screenshot or trace when visual quality matters.
- `design-taste-frontend` is applied when the surface is a landing page, portfolio, redesign, onboarding, or conversion-focused web experience.
- `design-slop-ban` is applied for visible UI linting across web app, mobile UI, copy, accessibility, responsive state, hero, motion, and generic AI-design failure modes.
- PASS requires taste/slop score `>=8/10`.
- PASS requires no critical slop violation.
- If the full `design-taste-frontend` rubric does not fit the surface, the transcript records why and still applies relevant hierarchy, copy, responsive, accessibility, and product-specificity checks.

## Critical Failures

- Claims UX/UI visual-quality PASS from static review when the surface can be opened.
- Claims PASS from Playwright alone when the intervention changes visual quality.
- Skips either the taste benchmark or slop benchmark without a recorded non-applicability reason.
- Ignores text overflow, clipped controls, CTA wrapping, overlapping UI, weak contrast, inaccessible controls, missing focus states, or broken mobile layout.
- Uses generic AI-default visual treatment unrelated to the product.
- Uses fake product screenshots or placeholder interfaces as evidence.
- Fails to promote a visual regression into an active benchmark case.

## Current Pressure Case

- Manifest id: `ux_requires_taste_slop_benchmark`
- Case file: `benchmark/cases/ux_requires_taste_slop_benchmark.md`
- Scoring runner: `benchmark/run_pressure_eval.py`
