import { useFormContext } from 'react-hook-form';
import type { RegistrationFormData } from '../../../schemas/registration';
import { PasswordInput } from '../PasswordInput';
import { PasswordStrengthMeter } from './PasswordStrengthMeter';

export function PasswordSection() {
  const {
    formState: { errors },
  } = useFormContext<RegistrationFormData>();

  return (
    <div className="space-y-4" aria-labelledby="password-section-title">
      <div className="space-y-1">
        <h3 id="password-section-title" className="text-sm font-semibold text-slate-700">
          Password security
        </h3>
        <p className="text-xs text-slate-500">
          Use a unique password that meets the following requirements for the best security.
        </p>
      </div>
      <div className="space-y-4">
        <PasswordInput name="password" label="Password" />
        <PasswordStrengthMeter />
        <PasswordInput name="confirmPassword" label="Confirm password" />
        {errors.confirmPassword ? (
          <p className="text-xs text-red-600">{errors.confirmPassword.message}</p>
        ) : null}
      </div>
    </div>
  );
}
