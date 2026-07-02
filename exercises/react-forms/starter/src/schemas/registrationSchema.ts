import { z } from 'zod'

const passwordRequirements = {
  minLength: /.{8,}/,
  uppercase: /[A-Z]/,
  lowercase: /[a-z]/,
  number: /\d/,
  specialCharacter: /[^A-Za-z0-9]/,
}

export const emailSchema = z
  .string({ error: 'Email is required' })
  .trim()
  .toLowerCase()
  .pipe(
    z.email({
      pattern: z.regexes.html5Email,
      error: 'Enter a valid email address',
    }),
  )

export const usernameSchema = z
  .string({ error: 'Username is required' })
  .trim()
  .min(3, 'Username must be at least 3 characters')
  .max(20, 'Username must be 20 characters or less')
  .regex(
    /^[A-Za-z0-9_]+$/,
    'Username can only contain letters, numbers, and underscores',
  )

export const passwordSchema = z
  .string({ error: 'Password is required' })
  .regex(
    passwordRequirements.minLength,
    'Password must be at least 8 characters',
  )
  .regex(
    passwordRequirements.uppercase,
    'Password must include an uppercase letter',
  )
  .regex(
    passwordRequirements.lowercase,
    'Password must include a lowercase letter',
  )
  .regex(passwordRequirements.number, 'Password must include a number')
  .regex(
    passwordRequirements.specialCharacter,
    'Password must include a special character',
  )

export const termsSchema = z
  .boolean({ error: 'You must accept the terms to create an account' })
  .refine((value) => value, 'You must accept the terms to create an account')

export const registrationSchema = z
  .object({
    email: emailSchema,
    username: usernameSchema,
    password: passwordSchema,
    confirmPassword: z
      .string({ error: 'Confirm your password' })
      .min(1, 'Confirm your password'),
    terms: termsSchema,
  })
  .superRefine(({ password, confirmPassword }, ctx) => {
    if (password !== confirmPassword) {
      ctx.addIssue({
        code: 'custom',
        path: ['confirmPassword'],
        message: 'Passwords must match',
      })
    }
  })

export type RegistrationData = z.infer<typeof registrationSchema>
export type RegistrationInput = z.input<typeof registrationSchema>

export { passwordRequirements }
