import { registrationSchema } from '../../schemas/registration';

describe('registration schema', () => {
  const baseData = {
    email: 'user@example.com',
    username: 'valid_user',
    password: 'StrongPassw0rd!',
    confirmPassword: 'StrongPassw0rd!',
    firstName: 'Jane',
    lastName: 'Doe',
    phoneNumber: '+12345678901',
    dateOfBirth: '1990-01-01',
    country: 'US',
    newsletter: true,
    terms: true,
  } as const;

  test('validates correct payload', () => {
    expect(() => registrationSchema.parse(baseData)).not.toThrow();
  });

  test('fails when passwords do not match', () => {
    const payload = { ...baseData, confirmPassword: 'Mismatch123!' };
    expect(() => registrationSchema.parse(payload)).toThrow('Passwords must match');
  });

  test('fails when terms are not accepted', () => {
    const payload = { ...baseData, terms: false };
    expect(() => registrationSchema.parse(payload)).toThrow('You must accept the terms and conditions');
  });
});
