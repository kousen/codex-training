import { expect, test } from '@playwright/test';

test('user can complete the registration flow', async ({ page }) => {
  await page.goto('/');

  await page.getByLabel('Email address').fill('playwright@example.com');
  await page.getByLabel('Username').fill('playwright_user');
  await page.getByLabel('Password').fill('StrongPassw0rd!');
  await page.getByLabel('Confirm password').fill('StrongPassw0rd!');
  await page.getByRole('button', { name: 'Continue' }).click();

  await expect(page.getByRole('heading', { name: 'Profile information' })).toBeVisible();

  await page.getByRole('button', { name: 'Continue' }).click();
  await page.getByRole('checkbox', { name: /i agree/i }).check();
  await page.getByRole('button', { name: 'Submit' }).click();

  await expect(page.getByText(/Registration successful/i)).toBeVisible();
});
