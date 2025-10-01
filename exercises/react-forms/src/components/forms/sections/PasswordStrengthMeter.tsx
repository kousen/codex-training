import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';
import { useMemo } from 'react';
import { useFormContext } from 'react-hook-form';
import { calculatePasswordStrength, passwordRequirements } from '../../../utils/validators';
import type { RegistrationFormData } from '../../../schemas/registration';

const strengthColors = ['bg-red-500', 'bg-orange-400', 'bg-yellow-400', 'bg-emerald-500', 'bg-emerald-600'];
const strengthTextColors = ['text-red-500', 'text-orange-500', 'text-yellow-600', 'text-emerald-600', 'text-emerald-700'];

export function PasswordStrengthMeter() {
  const { watch } = useFormContext<RegistrationFormData>();
  const password = watch('password');

  const strength = useMemo(() => calculatePasswordStrength(password ?? ''), [password]);
  const filledSegments = Array.from({ length: 4 }, (_, index) => index < strength.score);

  return (
    <div className="space-y-2" aria-live="polite">
      <div className="flex items-center justify-between text-xs font-medium text-slate-500">
        <span>Password strength</span>
        <span className={strengthTextColors[Math.min(strength.score, strengthTextColors.length - 1)]}>
          {strength.level}
        </span>
      </div>
      <div className="grid grid-cols-4 gap-1" role="meter" aria-valuemin={0} aria-valuemax={4} aria-valuenow={strength.score}>
        {filledSegments.map((filled, index) => (
          <span
            key={index}
            className={`h-2 rounded ${filled ? strengthColors[Math.min(strength.score, strengthColors.length - 1)] : 'bg-slate-200'}`.trim()}
          />
        ))}
      </div>
      <ul className="space-y-1 text-xs" aria-label="Password requirements">
        {passwordRequirements.map((requirement) => {
          const met = strength.metRequirements.includes(requirement.id);
          return (
            <li key={requirement.id} className="flex items-center gap-2">
              {met ? (
                <CheckCircleIcon className="h-4 w-4 text-emerald-500" aria-hidden />
              ) : (
                <XCircleIcon className="h-4 w-4 text-slate-300" aria-hidden />
              )}
              <span className={met ? 'text-slate-600' : 'text-slate-400'}>{requirement.label}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
