import { z } from 'zod';
import { calculatePasswordStrength, formatPhoneNumber, isAdult, isDisposableEmail, passwordRequirements } from '../utils/validators';

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters long')
  .refine((value) => passwordRequirements.every((req) => req.test(value)), {
    message: 'Password must include uppercase, lowercase, number, and special character',
  });

export const emailSchema = z
  .string()
  .email('Enter a valid email address')
  .refine((value) => !isDisposableEmail(value), {
    message: 'Disposable email addresses are not allowed',
  });

export const usernameSchema = z
  .string()
  .min(3, 'Username must be at least 3 characters')
  .max(20, 'Username cannot exceed 20 characters')
  .regex(/^[a-zA-Z0-9_]+$/, 'Username can include letters, numbers, and underscores only');

export const accountSchema = z.object({
  email: emailSchema,
  username: usernameSchema,
  password: passwordSchema,
  confirmPassword: z.string(),
});

export const profileSchema = z.object({
  firstName: z.string().max(50, 'First name is too long').optional().or(z.literal('')),
  lastName: z.string().max(50, 'Last name is too long').optional().or(z.literal('')),
  phoneNumber: z
    .string()
    .optional()
    .or(z.literal(''))
    .transform((value) => (value ? formatPhoneNumber(value) : undefined))
    .refine((value) => !value || /^\+[1-9]\d{7,14}$/.test(value), {
      message: 'Enter a valid international phone number',
    }),
  dateOfBirth: z
    .string()
    .optional()
    .or(z.literal(''))
    .refine((value) => !value || isAdult(value), {
      message: 'You must be at least 18 years old',
    }),
  country: z.string().optional(),
});

export const confirmationSchema = z.object({
  newsletter: z.boolean().optional().default(false),
  terms: z
    .boolean()
    .refine((value) => value === true, { message: 'You must accept the terms and conditions' }),
});

const baseRegistrationSchema = accountSchema.merge(profileSchema).merge(confirmationSchema);

export const registrationSchema = baseRegistrationSchema.superRefine((val, ctx) => {
  if (val.password !== val.confirmPassword) {
    ctx.addIssue({
      path: ['confirmPassword'],
      code: z.ZodIssueCode.custom,
      message: 'Passwords must match',
    });
  }

  const strength = calculatePasswordStrength(val.password);
  if (strength.score < 3) {
    ctx.addIssue({
      path: ['password'],
      code: z.ZodIssueCode.custom,
      message: 'Password is too weak. Please strengthen it.',
    });
  }
});

export type RegistrationSchema = z.infer<typeof registrationSchema>;
export type RegistrationFormData = RegistrationSchema;

export const accountStepSchema = accountSchema;
export const confirmationStepSchema = confirmationSchema;
