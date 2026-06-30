import { test, expect } from '@playwright/test';

const url = process.env.LOOP_URL;

test('loop harness visible surface smoke', async ({ page }, testInfo) => {
  test.skip(!url, 'Set LOOP_URL to the app route under verification.');

  await page.setViewportSize({ width: Number(process.env.LOOP_WIDTH || 1280), height: Number(process.env.LOOP_HEIGHT || 800) });
  const errors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') errors.push(message.text());
  });
  page.on('pageerror', (error) => errors.push(error.message));

  await page.goto(url!, { waitUntil: 'networkidle' });
  await expect(page.locator('body')).toBeVisible();
  await testInfo.attach('loop-screenshot', {
    body: await page.screenshot({ fullPage: true }),
    contentType: 'image/png',
  });
  expect(errors, errors.join('\n')).toEqual([]);
});
