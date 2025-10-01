export interface PasswordRequirement {
  id: string;
  label: string;
  test: (password: string) => boolean;
}

const DISPOSABLE_DOMAINS = new Set([
  'mailinator.com',
  'trashmail.com',
  '10minutemail.com',
  'guerrillamail.com',
  'tempmail.com',
  'yopmail.com',
]);

export const passwordRequirements: PasswordRequirement[] = [
  {
    id: 'length',
    label: 'At least 8 characters',
    test: (password) => password.length >= 8,
  },
  {
    id: 'uppercase',
    label: 'Contains an uppercase letter',
    test: (password) => /[A-Z]/.test(password),
  },
  {
    id: 'lowercase',
    label: 'Contains a lowercase letter',
    test: (password) => /[a-z]/.test(password),
  },
  {
    id: 'number',
    label: 'Contains a number',
    test: (password) => /\d/.test(password),
  },
  {
    id: 'special',
    label: 'Contains a special character',
    test: (password) => /[^A-Za-z0-9\s]/.test(password),
  },
];

export type PasswordStrengthLevel = 'Weak' | 'Fair' | 'Good' | 'Strong' | 'Very Strong';

export interface PasswordStrength {
  score: number;
  level: PasswordStrengthLevel;
  metRequirements: string[];
}

export function calculatePasswordStrength(password: string): PasswordStrength {
  if (!password) {
    return { score: 0, level: 'Weak', metRequirements: [] };
  }

  const metRequirements = passwordRequirements
    .filter((requirement) => requirement.test(password))
    .map((requirement) => requirement.id);

  const lengthScore = Math.min(password.length / 12, 1);
  const varietyScore = metRequirements.length / passwordRequirements.length;
  const bonus = /[^A-Za-z0-9]/.test(password) && password.length >= 12 ? 0.1 : 0;

  const rawScore = Math.min(lengthScore * 0.4 + varietyScore * 0.6 + bonus, 1);
  const normalizedScore = Math.round(rawScore * 4);

  const levelMap: PasswordStrengthLevel[] = ['Weak', 'Weak', 'Fair', 'Good', 'Strong'];
  const level = levelMap[Math.min(normalizedScore, levelMap.length - 1)];

  return {
    score: normalizedScore,
    level,
    metRequirements,
  };
}

export function isDisposableEmail(email: string): boolean {
  const domain = email.split('@')[1]?.toLowerCase();
  if (!domain) {
    return false;
  }
  return DISPOSABLE_DOMAINS.has(domain);
}

export function isAdult(dateOfBirth?: string | null): boolean {
  if (!dateOfBirth) {
    return true;
  }

  const parsed = new Date(dateOfBirth);
  if (Number.isNaN(parsed.getTime())) {
    return false;
  }

  const today = new Date();
  const age = today.getFullYear() - parsed.getFullYear();
  const monthDiff = today.getMonth() - parsed.getMonth();
  const dayDiff = today.getDate() - parsed.getDate();

  if (age > 18) {
    return true;
  }
  if (age === 18) {
    if (monthDiff > 0) {
      return true;
    }
    if (monthDiff === 0 && dayDiff >= 0) {
      return true;
    }
  }
  return false;
}

export function formatPhoneNumber(phone?: string | null): string {
  if (!phone) {
    return '';
  }
  const sanitized = phone.replace(/[^+\d]/g, '');
  if (!sanitized.startsWith('+')) {
    return `+${sanitized}`;
  }
  return sanitized;
}
