import { passwordRequirements } from '../schemas/registrationSchema'

type PasswordStrengthMeterProps = {
  password: string
}

const requirementItems = [
  {
    id: 'minLength',
    label: 'At least 8 characters',
    pattern: passwordRequirements.minLength,
  },
  {
    id: 'uppercase',
    label: 'One uppercase letter',
    pattern: passwordRequirements.uppercase,
  },
  {
    id: 'lowercase',
    label: 'One lowercase letter',
    pattern: passwordRequirements.lowercase,
  },
  {
    id: 'number',
    label: 'One number',
    pattern: passwordRequirements.number,
  },
  {
    id: 'specialCharacter',
    label: 'One special character',
    pattern: passwordRequirements.specialCharacter,
  },
] as const

const strengthLabels = ['Empty', 'Weak', 'Fair', 'Good', 'Strong', 'Excellent']
const strengthBarColors = [
  'bg-slate-200',
  'bg-red-500',
  'bg-orange-500',
  'bg-amber-500',
  'bg-blue-600',
  'bg-emerald-600',
]

export function PasswordStrengthMeter({
  password,
}: PasswordStrengthMeterProps) {
  const results = requirementItems.map((item) => ({
    ...item,
    met: item.pattern.test(password),
  }))
  const score = password ? results.filter((item) => item.met).length : 0
  const percentage = (score / requirementItems.length) * 100
  const label = strengthLabels[score]

  return (
    <div
      className="rounded-md border border-slate-200 bg-slate-50 p-4"
      aria-labelledby="password-strength-title"
    >
      <div className="flex items-center justify-between gap-4">
        <p
          id="password-strength-title"
          className="text-sm font-medium text-slate-800"
        >
          Password strength
        </p>
        <p className="text-sm font-semibold text-slate-700" aria-live="polite">
          {label}
        </p>
      </div>

      <div
        className="mt-3 h-2 rounded-full bg-slate-200"
        role="progressbar"
        aria-label="Password strength"
        aria-valuemin={0}
        aria-valuemax={requirementItems.length}
        aria-valuenow={score}
        aria-valuetext={`${label}: ${score} of ${requirementItems.length} requirements met`}
      >
        <div
          className={`h-full rounded-full transition-all ${strengthBarColors[score]}`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      <ul className="mt-4 grid gap-2 text-sm text-slate-700 sm:grid-cols-2">
        {results.map((item) => (
          <li key={item.id} className="flex items-center gap-2">
            <span
              aria-hidden="true"
              className={`size-2.5 rounded-full ${
                item.met ? 'bg-emerald-600' : 'bg-slate-300'
              }`}
            />
            <span className={item.met ? 'text-slate-700' : 'text-slate-500'}>
              <span className="sr-only">
                {item.met ? 'Met: ' : 'Missing: '}
              </span>
              {item.label}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
