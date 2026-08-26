import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { RegistrationForm } from './RegistrationForm'

function completePersonalStep() {
  fireEvent.change(screen.getByLabelText('First name'), { target: { value: 'Ada' } })
  fireEvent.change(screen.getByLabelText('Last name'), { target: { value: 'Lovelace' } })
  fireEvent.click(screen.getByRole('button', { name: 'Next' }))
}

async function completeAccountStep() {
  await screen.findByRole('heading', { name: 'Account details' })
  fireEvent.change(screen.getByLabelText('Email address'), { target: { value: 'ada@example.com' } })
  fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'Analytical1' } })
  fireEvent.change(screen.getByLabelText('Confirm password'), { target: { value: 'Analytical1' } })
  fireEvent.click(screen.getByRole('button', { name: 'Next' }))
}

describe('RegistrationForm', () => {
  it('shows inline errors and remains on a step when required fields are empty', async () => {
    render(<RegistrationForm />)

    fireEvent.click(screen.getByRole('button', { name: 'Next' }))

    expect(await screen.findByText('First name is required')).toBeInTheDocument()
    expect(screen.getByText('Last name is required')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Personal information' })).toBeInTheDocument()
    expect(screen.getByLabelText('First name')).toHaveAttribute('aria-invalid', 'true')
  })

  it('supports the complete registration flow', async () => {
    const onSubmit = vi.fn()
    render(<RegistrationForm onSubmit={onSubmit} />)

    completePersonalStep()
    await completeAccountStep()

    expect(await screen.findByRole('heading', { name: 'Confirm your details' })).toHaveFocus()
    expect(screen.getByText('Ada Lovelace')).toBeInTheDocument()
    expect(screen.getByText('ada@example.com')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Create account' }))

    await waitFor(() => expect(onSubmit).toHaveBeenCalledTimes(1))
    expect(onSubmit).toHaveBeenCalledWith({
      firstName: 'Ada',
      lastName: 'Lovelace',
      email: 'ada@example.com',
      password: 'Analytical1',
      confirmPassword: 'Analytical1',
    })
    expect(await screen.findByRole('heading', { name: 'Registration complete' })).toBeInTheDocument()
  })

  it('returns to the previous step when Escape is pressed', async () => {
    render(<RegistrationForm />)

    completePersonalStep()
    await screen.findByRole('heading', { name: 'Account details' })
    fireEvent.keyDown(screen.getByRole('form'), { key: 'Escape' })

    expect(await screen.findByRole('heading', { name: 'Personal information' })).toHaveFocus()
  })

  it('announces submission failures and allows another attempt', async () => {
    const onSubmit = vi.fn().mockRejectedValue(new Error('Network unavailable'))
    render(<RegistrationForm onSubmit={onSubmit} />)

    completePersonalStep()
    await completeAccountStep()
    await screen.findByRole('heading', { name: 'Confirm your details' })
    fireEvent.click(screen.getByRole('button', { name: 'Create account' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Registration could not be completed. Please try again.',
    )
    expect(screen.getByRole('button', { name: 'Create account' })).toBeEnabled()
  })
})
