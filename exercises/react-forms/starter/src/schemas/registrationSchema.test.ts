import { describe, expect, it } from 'vitest'
import { registrationSchema } from './registrationSchema'

const validRegistration = {
  firstName: 'Ada',
  lastName: 'Lovelace',
  email: 'ada@example.com',
  password: 'Analytical1',
  confirmPassword: 'Analytical1',
}

describe('registrationSchema', () => {
  it('accepts valid registration data', () => {
    expect(registrationSchema.safeParse(validRegistration).success).toBe(true)
  })

  it.each([
    ['an invalid email', { email: 'not-an-email' }, 'Enter a valid email address'],
    ['a short password', { password: 'Short1', confirmPassword: 'Short1' }, 'Password must be at least 8 characters'],
    ['a password without uppercase', { password: 'lowercase1', confirmPassword: 'lowercase1' }, 'Password must include an uppercase letter'],
    ['a password without a number', { password: 'NoNumbers', confirmPassword: 'NoNumbers' }, 'Password must include a number'],
    ['nonmatching passwords', { confirmPassword: 'Different1' }, 'Passwords must match'],
  ])('rejects %s', (_description, overrides, expectedMessage) => {
    const result = registrationSchema.safeParse({ ...validRegistration, ...overrides })

    expect(result.success).toBe(false)
    if (!result.success) {
      expect(result.error.issues.map((issue) => issue.message)).toContain(expectedMessage)
    }
  })
})
