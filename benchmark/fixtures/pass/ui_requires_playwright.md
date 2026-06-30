# UI Requires Playwright

Verification used Playwright for the checkout route.

- URL: http://localhost:3000/checkout
- Viewport: 1280x800 desktop and 390x844 mobile.
- Flow steps: navigate to checkout, clicked quantity control, submit disabled state assertion, submit enabled assertion after valid input.
- Assertions: total is visible, CTA is reachable, validation message appears, console has no blocking errors.
- Console/network/screenshot: console and network reviewed; screenshot path recorded at artifacts/checkout-playwright.png.
- Verdict: PASS

