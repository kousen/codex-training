import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';
import type { FieldPath } from 'react-hook-form';
import { useFormContext } from 'react-hook-form';
import type { RegistrationFormData } from '../../schemas/registration';

interface PasswordInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  name: FieldPath<RegistrationFormData>;
  label: string;
  description?: string;
}

export function PasswordInput({ name, label, description, id, className, ...props }: PasswordInputProps) {
  const {
    register,
    formState: { errors },
    getFieldState,
  } = useFormContext<RegistrationFormData>();
  const [visible, setVisible] = useState(false);
  const fieldId = id ?? name;
  const error = errors[name];
  const fieldState = getFieldState(name);

  return (
    <div className={`space-y-1 ${className ?? ''}`.trim()}>
      <label
        htmlFor={fieldId}
        className="flex items-center justify-between text-sm font-medium text-slate-700"
      >
        <span>{label}</span>
      </label>
      <div className="relative">
        <input
          id={fieldId}
          type={visible ? 'text' : 'password'}
          className={`block w-full rounded-md border px-3 py-2 text-sm shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0 ${
            error ? 'border-red-500 pr-10 text-red-900 placeholder:text-red-300 focus:ring-red-500' : 'border-slate-300 pr-10'
          }`.trim()}
          aria-invalid={fieldState.invalid}
          aria-describedby={description ? `${fieldId}-description` : undefined}
          autoComplete={props.autoComplete ?? 'new-password'}
          {...props}
          {...register(name)}
        />
        <button
          type="button"
          className="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-500 hover:text-slate-700"
          onClick={() => setVisible((prev) => !prev)}
          aria-label={visible ? 'Hide password' : 'Show password'}
        >
          {visible ? <EyeSlashIcon className="h-5 w-5" aria-hidden /> : <EyeIcon className="h-5 w-5" aria-hidden />}
        </button>
      </div>
      {description ? (
        <p id={`${fieldId}-description`} className="text-xs text-slate-500">
          {description}
        </p>
      ) : null}
      {error ? (
        <p className="flex items-center gap-1 text-xs text-red-600" role="alert">
          <span>{String(error.message)}</span>
        </p>
      ) : null}
    </div>
  );
}
