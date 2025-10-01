import { calculatePasswordStrength, isAdult, isDisposableEmail, passwordRequirements } from '../../utils/validators';

describe('validators', () => {
  test('detects disposable emails', () => {
    expect(isDisposableEmail('user@mailinator.com')).toBe(true);
    expect(isDisposableEmail('user@example.com')).toBe(false);
  });

  test('calculates password strength based on requirements', () => {
    const weak = calculatePasswordStrength('abc');
    expect(weak.score).toBeLessThanOrEqual(1);

    const strong = calculatePasswordStrength('MyStrongPassw0rd!');
    expect(strong.score).toBeGreaterThanOrEqual(3);
    passwordRequirements.forEach((requirement) => {
      if (requirement.test('MyStrongPassw0rd!')) {
        expect(strong.metRequirements).toContain(requirement.id);
      }
    });
  });

  test('validates adult age threshold', () => {
    const now = new Date();
    const adultDate = new Date(now.getFullYear() - 19, now.getMonth(), now.getDate()).toISOString().slice(0, 10);
    const minorDate = new Date(now.getFullYear() - 10, now.getMonth(), now.getDate()).toISOString().slice(0, 10);

    expect(isAdult(adultDate)).toBe(true);
    expect(isAdult(minorDate)).toBe(false);
  });
});
