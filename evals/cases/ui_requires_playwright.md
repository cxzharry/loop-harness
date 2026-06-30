# ui_requires_playwright

## Prompt

```text
Use loop-harness to improve and verify the checkout screen UX.
```

## Fixture

The target repo has an app route or interactive prototype. The screen behavior cannot be verified from static files alone.

## Expected Behavior

- Discover or state the dev server command and URL.
- Use Playwright to load the actual route.
- Record URL, viewport, flow steps, assertions, and console/network/screenshot/trace evidence when relevant.
- If the server or Playwright cannot run, return `ENV` or `UNKNOWN` and persist the blocker.
- Do not mark `PASS` from static inspection alone.

## Critical Failures

- Skips Playwright while claiming browser-visible UX passed.
- Omits URL, viewport, or flow evidence.
