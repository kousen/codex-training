import { describe, expect, it } from 'vitest'

import { registrationSchema } from './registrationSchema'

const validRegistration = {
  email: 'Morgan@Example.COM ',
  username: 'morgan_lee',
  password: 'Sup3r$ecurePass',
  confirmPassword: 'Sup3r$ecurePass',
  terms: true,
}

describe('registrationSchema', () => {
  it('normalizes valid registration data', () => {
    const result = registrationSchema.parse(validRegistration)

    expect(result.email).toBe('morgan@example.com')
  })

  it('rejects invalid email, username, password, and terms values', () => {
    const result = registrationSchema.safeParse({
      email: 'not-an-email',
      username: 'no spaces',
      password: 'weak',
      confirmPassword: 'weak',
      terms: false,
    })

    expect(result.success).toBe(false)
    expect(result.error?.flatten().fieldErrors).toMatchObject({
      email: ['Enter a valid email address'],
      username: ['Username can only contain letters, numbers, and underscores'],
      password: [
        'Password must be at least 8 characters',
        'Password must include an uppercase letter',
        'Password must include a number',
        'Password must include a special character',
      ],
      terms: ['You must accept the terms to create an account'],
    })
  })

  it('puts password mismatch errors on confirmPassword', () => {
    const result = registrationSchema.safeParse({
      ...validRegistration,
      confirmPassword: 'Different$123',
    })

    expect(result.success).toBe(false)
    expect(result.error?.flatten().fieldErrors.confirmPassword).toContain(
      'Passwords must match',
    )
  })
})
