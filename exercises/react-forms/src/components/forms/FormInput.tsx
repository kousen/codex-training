import { ExclamationCircleIcon, InformationCircleIcon } from '@heroicons/react/24/outline';
import type { FieldPath } from 'react-hook-form';
import { useFormContext } from 'react-hook-form';
import type { RegistrationFormData } from '../../schemas/registration';

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  name: FieldPath<RegistrationFormData>;
  label: string;
  description?: string;
  optional?: boolean;
  hint?: string;
}

export function FormInput({ name, label, description, optional, hint, id, className, ...props }: FormInputProps) {
  const {
    register,
    formState: { errors },
    getFieldState,
  } = useFormContext<RegistrationFormData>();

  const fieldId = id ?? name;
  const error = errors[name];
  const fieldState = getFieldState(name);
  const describedBy = [description ? `${fieldId}-description` : null, hint ? `${fieldId}-hint` : null]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={`space-y-1 ${className ?? ''}`.trim()}>
      <label
        htmlFor={fieldId}
        className="flex items-center justify-between text-sm font-medium text-slate-700"
      >
        <span>{label}</span>
        {optional ? <span className="text-xs font-normal text-slate-400">Optional</span> : null}
      </label>
      <div className="relative">
        <input
          id={fieldId}
          className={`block w-full rounded-md border px-3 py-2 text-sm shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0 ${
            error ? 'border-red-500 pr-10 text-red-900 placeholder:text-red-300 focus:ring-red-500' : 'border-slate-300'
          }`.trim()}
          aria-invalid={fieldState.invalid}
          aria-describedby={describedBy || undefined}
          {...props}
          {...register(name)}
        />
        {error ? (
          <ExclamationCircleIcon className="absolute inset-y-0 right-0 mr-3 h-5 w-5 text-red-500" aria-hidden />
        ) : null}
      </div>
      {description ? (
        <p id={`${fieldId}-description`} className="text-xs text-slate-500">
          {description}
        </p>
      ) : null}
      {hint ? (
        <div id={`${fieldId}-hint`} className="flex items-center gap-1 text-xs text-slate-500">
          <InformationCircleIcon className="h-4 w-4" aria-hidden />
          <span>{hint}</span>
        </div>
      ) : null}
      {error ? (
        <p className="flex items-center gap-1 text-xs text-red-600" role="alert">
          <ExclamationCircleIcon className="h-4 w-4" aria-hidden />
          <span>{String(error.message)}</span>
        </p>
      ) : null}
    </div>
  );
}
