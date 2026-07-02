import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect, useState } from 'react'
import { type SubmitHandler, useForm, useWatch } from 'react-hook-form'

import { useDebouncedValue } from '../hooks/useDebouncedValue'
import {
  type RegistrationData,
  type RegistrationInput,
  registrationSchema,
  usernameSchema,
} from '../schemas/registrationSchema'
import { checkUsernameAvailability } from '../services/usernameService'
import { CheckboxInput } from './CheckboxInput'
import { PasswordStrengthMeter } from './PasswordStrengthMeter'
import { TextInput } from './TextInput'

type UsernameAvailabilityStatus =
  'idle' | 'checking' | 'available' | 'unavailable' | 'error'
type UsernameAvailabilityResult = Exclude<
  UsernameAvailabilityStatus,
  'idle' | 'checking'
>
type CheckedUsername = {
  username: string
  status: UsernameAvailabilityResult
}

export function RegistrationForm() {
  const [submittedData, setSubmittedData] = useState<RegistrationData | null>(
    null,
  )
  const [checkedUsername, setCheckedUsername] =
    useState<CheckedUsername | null>(null)

  const {
    register,
    handleSubmit,
    reset,
    control,
    setError,
    clearErrors,
    formState: { errors, isSubmitting, isValid },
  } = useForm<RegistrationInput, unknown, RegistrationData>({
    resolver: zodResolver(registrationSchema),
    mode: 'onBlur',
    defaultValues: {
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
      terms: false,
    },
  })
  const password = useWatch({ control, name: 'password' }) ?? ''
  const username = useWatch({ control, name: 'username' }) ?? ''
  const currentUsername = username.trim()
  const debouncedUsername = useDebouncedValue(currentUsername, 500)
  const parsedCurrentUsername = usernameSchema.safeParse(currentUsername)
  const parsedUsername = usernameSchema.safeParse(debouncedUsername)
  const normalizedUsername = parsedUsername.success ? parsedUsername.data : ''
  const usernameStatus: UsernameAvailabilityStatus =
    !currentUsername || !parsedCurrentUsername.success
      ? 'idle'
      : currentUsername !== debouncedUsername
        ? 'checking'
        : checkedUsername?.username === normalizedUsername
          ? checkedUsername.status
          : 'checking'

  useEffect(() => {
    if (!normalizedUsername) {
      return
    }

    const abortController = new AbortController()

    clearErrors('username')

    checkUsernameAvailability(normalizedUsername, abortController.signal)
      .then(({ available }) => {
        if (available) {
          setCheckedUsername({
            username: normalizedUsername,
            status: 'available',
          })
          clearErrors('username')
          return
        }

        setCheckedUsername({
          username: normalizedUsername,
          status: 'unavailable',
        })
        setError('username', {
          type: 'manual',
          message: 'That username is already taken',
        })
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') {
          return
        }

        setCheckedUsername({
          username: normalizedUsername,
          status: 'error',
        })
        setError('username', {
          type: 'manual',
          message: 'Username check failed. Try again.',
        })
      })

    return () => abortController.abort()
  }, [clearErrors, normalizedUsername, setError])

  const onSubmit: SubmitHandler<RegistrationData> = async (data) => {
    await new Promise((resolve) => window.setTimeout(resolve, 400))
    setSubmittedData(data)
    setCheckedUsername(null)
    reset({
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
      terms: false,
    })
  }

  return (
    <form
      noValidate
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-6 rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
    >
      <div className="space-y-2">
        <h2 className="text-xl font-semibold text-slate-950">
          Account details
        </h2>
        <p className="text-sm leading-6 text-slate-600">
          Create the first version of the registration flow with schema-backed
          validation.
        </p>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <TextInput
          id="email"
          label="Email address"
          type="email"
          autoComplete="email"
          error={errors.email?.message}
          registration={register('email')}
          className="space-y-2 sm:col-span-2"
        />

        <TextInput
          id="username"
          label="Username"
          type="text"
          autoComplete="username"
          hint="Use 3-20 letters, numbers, or underscores."
          error={errors.username?.message}
          registration={register('username')}
          className="space-y-2 sm:col-span-2"
        />
        <UsernameAvailabilityMessage status={usernameStatus} />

        <div className="space-y-3">
          <TextInput
            id="password"
            label="Password"
            type="password"
            autoComplete="new-password"
            error={errors.password?.message}
            registration={register('password')}
          />
          <PasswordStrengthMeter password={password} />
        </div>

        <TextInput
          id="confirmPassword"
          label="Confirm password"
          type="password"
          autoComplete="new-password"
          error={errors.confirmPassword?.message}
          registration={register('confirmPassword')}
        />
      </div>

      <CheckboxInput
        id="terms"
        label="I accept the terms and privacy policy."
        error={errors.terms?.message}
        registration={register('terms')}
      />

      {submittedData ? (
        <div
          role="status"
          aria-live="polite"
          className="rounded-md border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900"
        >
          Registration ready for {submittedData.email}.
        </div>
      ) : null}

      <button
        type="submit"
        disabled={isSubmitting || usernameStatus === 'checking'}
        className="inline-flex min-h-11 items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 focus:outline-none disabled:cursor-not-allowed disabled:bg-slate-400"
      >
        {isSubmitting ? 'Submitting...' : 'Create account'}
      </button>

      <p className="sr-only" aria-live="polite">
        {isValid ? 'Form is valid.' : 'Form is not valid yet.'}
      </p>
    </form>
  )
}

function UsernameAvailabilityMessage({
  status,
}: {
  status: UsernameAvailabilityStatus
}) {
  if (status === 'idle') {
    return null
  }

  const statusContent = {
    checking: {
      text: 'Checking username availability...',
      className: 'border-blue-200 bg-blue-50 text-blue-800',
    },
    available: {
      text: 'Username is available.',
      className: 'border-emerald-200 bg-emerald-50 text-emerald-900',
    },
    unavailable: {
      text: 'Choose another username.',
      className: 'border-red-200 bg-red-50 text-red-800',
    },
    error: {
      text: 'Unable to check username right now.',
      className: 'border-amber-200 bg-amber-50 text-amber-900',
    },
  } satisfies Record<
    Exclude<UsernameAvailabilityStatus, 'idle'>,
    { text: string; className: string }
  >

  const content = statusContent[status]

  return (
    <div
      role="status"
      aria-live="polite"
      className={`rounded-md border px-3 py-2 text-sm sm:col-span-2 ${content.className}`}
    >
      {content.text}
    </div>
  )
}
