import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe'
import { describe, expect, it } from 'vitest'

import { RegistrationForm } from './RegistrationForm'

expect.extend(toHaveNoViolations)

async function fillValidForm(username = 'morgan_lee') {
  const user = userEvent.setup()

  await user.type(screen.getByLabelText(/email address/i), 'Morgan@Example.COM')
  await user.type(screen.getByLabelText(/username/i), username)
  await user.type(screen.getByLabelText(/^password$/i), 'Sup3r$ecurePass')
  await user.type(screen.getByLabelText(/confirm password/i), 'Sup3r$ecurePass')
  await user.click(screen.getByLabelText(/i accept the terms/i))

  return user
}

describe('RegistrationForm', () => {
  it('renders accessible form controls and password strength guidance', async () => {
    render(<RegistrationForm />)

    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/i accept the terms/i)).toBeInTheDocument()

    const strength = screen.getByRole('progressbar', {
      name: /password strength/i,
    })
    expect(strength).toHaveAttribute('aria-valuenow', '0')

    const user = userEvent.setup()
    await user.type(screen.getByLabelText(/^password$/i), 'Sup3r$ecurePass')

    expect(strength).toHaveAttribute('aria-valuenow', '5')
    expect(screen.getByText('Excellent')).toBeInTheDocument()
    expect(screen.getByText('One special character')).toBeInTheDocument()
  })

  it('shows inline validation errors for invalid submit attempts', async () => {
    const user = userEvent.setup()

    render(<RegistrationForm />)

    await user.click(screen.getByRole('button', { name: /create account/i }))

    expect(await screen.findByText(/enter a valid email address/i)).toHaveRole(
      'alert',
    )
    expect(
      screen.getByText(/username must be at least 3 characters/i),
    ).toHaveRole('alert')
    expect(
      screen.getByText(/password must be at least 8 characters/i),
    ).toHaveRole('alert')
    expect(screen.getByText(/confirm your password/i)).toHaveRole('alert')
    expect(screen.getByText(/you must accept the terms/i)).toHaveRole('alert')
  })

  it('checks username availability with loading and unavailable states', async () => {
    const user = userEvent.setup()

    render(<RegistrationForm />)

    await user.type(screen.getByLabelText(/username/i), 'admin')

    expect(
      await screen.findByText(/checking username availability/i),
    ).toBeInTheDocument()
    expect(
      await screen.findByText(
        /choose another username/i,
        {},
        { timeout: 2500 },
      ),
    ).toBeVisible()
    expect(screen.getByText(/that username is already taken/i)).toHaveRole(
      'alert',
    )
  })

  it('submits valid form data after username availability succeeds', async () => {
    render(<RegistrationForm />)

    await fillValidForm()

    expect(
      await screen.findByText(/username is available/i, {}, { timeout: 2500 }),
    ).toBeVisible()

    await userEvent.click(
      screen.getByRole('button', { name: /create account/i }),
    )

    expect(
      await screen.findByText(
        /registration ready for morgan@example.com/i,
        {},
        { timeout: 1500 },
      ),
    ).toBeVisible()
  })

  it('has no detectable axe accessibility violations', async () => {
    const { container } = render(<RegistrationForm />)

    await fillValidForm('accessible_user')
    await screen.findByText(/username is available/i, {}, { timeout: 2500 })

    const results = await axe(container)

    expect(results).toHaveNoViolations()
  })

  it('keeps username status scoped to the current typed value', async () => {
    const user = userEvent.setup()

    render(<RegistrationForm />)

    const usernameField = screen.getByLabelText(/username/i)
    await user.type(usernameField, 'admin')

    expect(
      await screen.findByText(
        /choose another username/i,
        {},
        { timeout: 2500 },
      ),
    ).toBeVisible()

    await user.clear(usernameField)
    await user.type(usernameField, 'new_user')

    expect(screen.queryByText(/choose another username/i)).toBeNull()
    expect(
      await screen.findByText(/username is available/i, {}, { timeout: 2500 }),
    ).toBeVisible()
  })
})
