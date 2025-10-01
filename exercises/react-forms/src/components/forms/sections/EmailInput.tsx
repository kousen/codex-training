import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/solid';
import { useCallback, useEffect, useRef, useState } from 'react';
import { useFormContext } from 'react-hook-form';
import { checkEmailUniqueness } from '../../../services/api';
import type { RegistrationFormData } from '../../../schemas/registration';
import { Spinner } from '../../ui/Spinner';

export function EmailInput() {
  const {
    register,
    setError,
    clearErrors,
    formState: { errors },
  } = useFormContext<RegistrationFormData>();
  const [status, setStatus] = useState<'idle' | 'loading' | 'valid' | 'error'>('idle');
  const isMounted = useRef(true);

  useEffect(() => () => {
    isMounted.current = false;
  }, []);

  const handleBlur = useCallback(
    async (event: React.FocusEvent<HTMLInputElement>) => {
      const value = event.target.value;
      if (!value || errors.email) {
        return;
      }
      setStatus('loading');
      try {
        const response = await checkEmailUniqueness(value);
        if (!isMounted.current) {
          return;
        }
        if (response.unique) {
          setStatus('valid');
          clearErrors('email');
        } else {
          setStatus('error');
          setError('email', { type: 'validate', message: response.message ?? 'Email already registered' });
        }
      } catch (error) {
        if (!isMounted.current) {
          return;
        }
        setStatus('error');
        setError('email', {
          type: 'validate',
          message: error instanceof Error ? error.message : 'Unable to validate email right now',
        });
      }
    },
    [clearErrors, errors.email, setError],
  );

  const registration = register('email', {
    onBlur: handleBlur,
  });

  return (
    <div className="space-y-1">
      <label htmlFor="email" className="flex items-center justify-between text-sm font-medium text-slate-700">
        <span>Email address</span>
      </label>
      <div className="relative">
        <input
          id="email"
          type="email"
          inputMode="email"
          autoComplete="email"
          className={`block w-full rounded-md border px-3 py-2 text-sm shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0 ${
            errors.email ? 'border-red-500 pr-10 text-red-900 placeholder:text-red-300 focus:ring-red-500' : 'border-slate-300 pr-10'
          }`.trim()}
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : 'email-helper'}
          {...registration}
        />
        <StatusIndicator status={status} hasError={Boolean(errors.email)} />
      </div>
      {errors.email ? (
        <p id="email-error" className="flex items-center gap-1 text-xs text-red-600" role="alert">
          <ExclamationCircleIcon className="h-4 w-4" aria-hidden />
          <span>{errors.email.message}</span>
        </p>
      ) : (
        <p id="email-helper" className="text-xs text-slate-500">We will never share your email with anyone else.</p>
      )}
    </div>
  );
}

interface StatusIndicatorProps {
  status: 'idle' | 'loading' | 'valid' | 'error';
  hasError: boolean;
}

function StatusIndicator({ status, hasError }: StatusIndicatorProps) {
  if (status === 'idle') {
    return null;
  }
  if (status === 'loading') {
    return (
      <span className="absolute inset-y-0 right-0 mr-3 flex items-center" aria-hidden>
        <Spinner className="h-4 w-4" ariaHidden />
      </span>
    );
  }
  if (status === 'valid' && !hasError) {
    return (
      <span className="absolute inset-y-0 right-0 mr-3 flex items-center text-emerald-500">
        <CheckCircleIcon className="h-4 w-4" aria-hidden />
      </span>
    );
  }
  if (status === 'error' || hasError) {
    return (
      <span className="absolute inset-y-0 right-0 mr-3 flex items-center text-red-500">
        <ExclamationCircleIcon className="h-4 w-4" aria-hidden />
      </span>
    );
  }
  return null;
}
