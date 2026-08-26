import { expect, test } from '@playwright/test'

test.beforeEach(async ({ page }) => {
  await page.goto('/')
})

test('keeps the user on a step and identifies invalid fields', async ({ page }) => {
  await page.getByRole('button', { name: 'Next' }).click()

  await expect(page.getByText('First name is required')).toBeVisible()
  await expect(page.getByText('Last name is required')).toBeVisible()
  await expect(page.getByLabel('First name')).toBeFocused()
  await expect(page.getByLabel('First name')).toHaveAttribute('aria-invalid', 'true')
  await expect(page.getByRole('heading', { name: 'Personal information' })).toBeVisible()
})

test('completes the registration journey', async ({ page }) => {
  await page.getByLabel('First name').fill('Ada')
  await page.getByLabel('Last name').fill('Lovelace')
  await page.getByRole('button', { name: 'Next' }).click()

  await expect(page.getByRole('heading', { name: 'Account details' })).toBeFocused()
  await page.getByLabel('Email address').fill('ada@example.com')
  await page.getByLabel('Password', { exact: true }).fill('Analytical1')
  await page.getByLabel('Confirm password').fill('Analytical1')
  await page.getByRole('button', { name: 'Next' }).click()

  await expect(page.getByRole('heading', { name: 'Confirm your details' })).toBeFocused()
  await expect(page.getByText('Ada Lovelace')).toBeVisible()
  await expect(page.getByText('ada@example.com')).toBeVisible()
  await expect(page.getByText('Analytical1')).toHaveCount(0)

  await page.getByRole('button', { name: 'Create account' }).click()

  await expect(page.getByRole('heading', { name: 'Registration complete' })).toBeVisible()
  await expect(page.getByText('Thanks, Ada. Your account has been created.')).toBeVisible()
})
