import { expect, test } from '@playwright/test'

async function expectReady(page: import('@playwright/test').Page) {
  await page.goto('/')

  await expect(
    page.getByRole('heading', { name: /user registration/i }),
  ).toBeVisible()
  await expect(
    page.getByRole('heading', { name: /account details/i }),
  ).toBeVisible()
  await expect(page.getByLabel(/email address/i)).toBeVisible()
  await expect(page.getByLabel(/username/i)).toBeVisible()
  await expect(page.getByLabel(/^password$/i)).toBeVisible()
  await expect(page.getByLabel(/confirm password/i)).toBeVisible()
  await expect(page.getByLabel(/i accept the terms/i)).toBeVisible()
}

async function fillValidRegistration(
  page: import('@playwright/test').Page,
  username = 'morgan_lee',
) {
  await page.getByLabel(/email address/i).fill('Morgan@Example.COM')
  await page.getByLabel(/username/i).fill(username)
  await expect(page.getByText(/username is available/i)).toBeVisible()
  await page.getByLabel(/^password$/i).fill('Sup3r$ecurePass')
  await page.getByLabel(/confirm password/i).fill('Sup3r$ecurePass')
  await page.getByLabel(/i accept the terms/i).check()
}

test.describe('registration form', () => {
  test('renders the primary form on desktop and mobile widths', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1280, height: 900 })
    await expectReady(page)
    await expect(
      page.getByRole('button', { name: /create account/i }),
    ).toBeVisible()

    await page.setViewportSize({ width: 390, height: 844 })
    await page.reload()
    await expectReady(page)
    await expect(page.getByText(/password strength/i)).toBeVisible()
  })

  test('shows accessible inline errors on empty submit', async ({ page }) => {
    await expectReady(page)

    await page.getByRole('button', { name: /create account/i }).click()

    await expect(page.getByText(/enter a valid email address/i)).toBeVisible()
    await expect(
      page.getByText(/username must be at least 3 characters/i),
    ).toBeVisible()
    await expect(
      page.getByText(/password must be at least 8 characters/i),
    ).toBeVisible()
    await expect(page.getByText(/confirm your password/i)).toBeVisible()
    await expect(page.getByText(/you must accept the terms/i)).toBeVisible()

    await expect(page.getByLabel(/email address/i)).toHaveAttribute(
      'aria-invalid',
      'true',
    )
    await expect(page.getByLabel(/username/i)).toHaveAttribute(
      'aria-invalid',
      'true',
    )
  })

  test('checks username availability with loading, unavailable, and available states', async ({
    page,
  }) => {
    await expectReady(page)

    await page.getByLabel(/username/i).fill('admin')

    await expect(
      page.getByText(/checking username availability/i),
    ).toBeVisible()
    await expect(page.getByText(/choose another username/i)).toBeVisible()
    await expect(
      page.getByText(/that username is already taken/i),
    ).toBeVisible()

    await page.getByLabel(/username/i).fill('morgan_lee')

    await expect(
      page.getByText(/checking username availability/i),
    ).toBeVisible()
    await expect(page.getByText(/username is available/i)).toBeVisible()
    await expect(page.getByText(/choose another username/i)).toHaveCount(0)
  })

  test('updates password strength feedback as requirements are met', async ({
    page,
  }) => {
    await expectReady(page)

    const password = page.getByLabel(/^password$/i)
    const strength = page.getByRole('progressbar', {
      name: /password strength/i,
    })

    await expect(strength).toHaveAttribute('aria-valuenow', '0')
    await expect(page.getByText('Empty')).toBeVisible()

    await password.fill('weak')
    await expect(strength).toHaveAttribute('aria-valuenow', '1')
    await expect(page.getByText('Weak')).toBeVisible()

    await password.fill('Sup3r$ecurePass')
    await expect(strength).toHaveAttribute('aria-valuenow', '5')
    await expect(page.getByText('Excellent')).toBeVisible()
    await expect(page.getByText(/met: one special character/i)).toBeAttached()
  })

  test('submits a valid registration and normalizes email casing', async ({
    page,
  }) => {
    await expectReady(page)
    await fillValidRegistration(page)

    await page.getByRole('button', { name: /create account/i }).click()

    await expect(
      page.getByText(/registration ready for morgan@example.com/i),
    ).toBeVisible()
    await expect(page.getByLabel(/email address/i)).toHaveValue('')
    await expect(page.getByLabel(/username/i)).toHaveValue('')
  })

  test('supports keyboard navigation through the form controls', async ({
    page,
  }) => {
    await expectReady(page)

    await page.keyboard.press('Tab')
    await expect(page.getByLabel(/email address/i)).toBeFocused()

    await page.keyboard.press('Tab')
    await expect(page.getByLabel(/username/i)).toBeFocused()

    await page.keyboard.press('Tab')
    await expect(page.getByLabel(/^password$/i)).toBeFocused()

    await page.keyboard.press('Tab')
    await expect(page.getByLabel(/confirm password/i)).toBeFocused()

    await page.keyboard.press('Tab')
    await expect(page.getByLabel(/i accept the terms/i)).toBeFocused()
  })
})
