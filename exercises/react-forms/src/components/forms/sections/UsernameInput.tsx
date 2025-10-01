import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/react/24/solid';
import { useEffect, useRef, useState } from 'react';
import { useController, useFormContext } from 'react-hook-form';
import { useDebounce } from '../../../hooks/useDebounce';
import { checkUsernameAvailability } from '../../../services/api';
import type { RegistrationFormData } from '../../../schemas/registration';
import { Spinner } from '../../ui/Spinner';

export function UsernameInput() {
  const {
    control,
    formState: { errors },
    setError,
    clearErrors,
  } = useFormContext<RegistrationFormData>();

  const {
    field,
    fieldState,
  } = useController({
    name: 'username',
    control,
  });

  const [status, setStatus] = useState<'idle' | 'loading' | 'available' | 'unavailable'>('idle');
  const debouncedUsername = useDebounce(field.value, 500);
  const isMounted = useRef(true);

  useEffect(() => () => {
    isMounted.current = false;
  }, []);

  useEffect(() => {
    const runValidation = async () => {
      const value = (debouncedUsername ?? '').trim();
      if (!value || errors.username) {
        setStatus('idle');
        return;
      }
      setStatus('loading');
      try {
        const result = await checkUsernameAvailability(value);
        if (!isMounted.current) {
          return;
        }
        if (result.available) {
          setStatus('available');
          clearErrors('username');
        } else {
          setStatus('unavailable');
          setError('username', {
            type: 'validate',
            message: result.message ?? 'Username is already taken',
          });
        }
      } catch (error) {
        if (!isMounted.current) {
          return;
        }
        setStatus('unavailable');
        setError('username', {
          type: 'validate',
          message: error instanceof Error ? error.message : 'Unable to check username availability',
        });
      }
    };

    runValidation();
  }, [debouncedUsername, clearErrors, errors.username, setError]);

  return (
    <div className="space-y-1">
      <label htmlFor="username" className="flex items-center justify-between text-sm font-medium text-slate-700">
        <span>Username</span>
        <span className="text-xs text-slate-400">3-20 characters</span>
      </label>
      <div className="relative">
        <input
          id="username"
          inputMode="text"
          autoComplete="username"
          className={`block w-full rounded-md border px-3 py-2 text-sm shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0 ${
            fieldState.invalid ? 'border-red-500 pr-10 text-red-900 placeholder:text-red-300 focus:ring-red-500' : 'border-slate-300 pr-10'
          }`.trim()}
          aria-invalid={fieldState.invalid}
          aria-describedby={fieldState.invalid ? 'username-error' : 'username-hint'}
          {...field}
        />
        <StatusIndicator status={status} hasError={fieldState.invalid} />
      </div>
      {fieldState.invalid ? (
        <p id="username-error" className="flex items-center gap-1 text-xs text-red-600" role="alert">
          <ExclamationCircleIcon className="h-4 w-4" aria-hidden />
          <span>{errors.username?.message}</span>
        </p>
      ) : (
        <p id="username-hint" className="text-xs text-slate-500">
          Letters, numbers, and underscores only.
        </p>
      )}
    </div>
  );
}

interface StatusIndicatorProps {
  status: 'idle' | 'loading' | 'available' | 'unavailable';
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
  if (status === 'available' && !hasError) {
    return (
      <span className="absolute inset-y-0 right-0 mr-3 flex items-center text-emerald-500">
        <CheckCircleIcon className="h-4 w-4" aria-hidden />
      </span>
    );
  }
  if (status === 'unavailable' || hasError) {
    return (
      <span className="absolute inset-y-0 right-0 mr-3 flex items-center text-red-500">
        <ExclamationCircleIcon className="h-4 w-4" aria-hidden />
      </span>
    );
  }
  return null;
}
