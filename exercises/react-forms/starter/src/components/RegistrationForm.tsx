import { useEffect, useRef, useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import {
  registrationSchema,
  type RegistrationData,
} from '../schemas/registrationSchema'

const steps = ['Personal information', 'Account details', 'Confirmation'] as const
const personalFields = ['firstName', 'lastName'] as const
const accountFields = ['email', 'password', 'confirmPassword'] as const

type RegistrationFormProps = {
  onSubmit?: (data: RegistrationData) => Promise<void> | void
}

type FieldErrorProps = {
  id: string
  message?: string
}

function FieldError({ id, message }: FieldErrorProps) {
  if (!message) return null

  return (
    <p className="field-error" id={id} role="alert">
      {message}
    </p>
  )
}

export function RegistrationForm({ onSubmit }: RegistrationFormProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isComplete, setIsComplete] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const stepHeadingRef = useRef<HTMLHeadingElement>(null)
  const hasMounted = useRef(false)

  const {
    register,
    watch,
    trigger,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegistrationData>({
    resolver: zodResolver(registrationSchema),
    mode: 'onBlur',
    reValidateMode: 'onChange',
    defaultValues: {
      firstName: '',
      lastName: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
  })

  const values = watch()

  useEffect(() => {
    if (hasMounted.current) {
      stepHeadingRef.current?.focus()
    } else {
      hasMounted.current = true
    }
  }, [currentStep])

  async function goToNextStep() {
    const fields = currentStep === 0 ? personalFields : accountFields
    const isStepValid = await trigger(fields, { shouldFocus: true })

    if (isStepValid) {
      setCurrentStep((step) => Math.min(step + 1, steps.length - 1))
    }
  }

  function goToPreviousStep() {
    setCurrentStep((step) => Math.max(step - 1, 0))
  }

  async function submitRegistration(data: RegistrationData) {
    setSubmitError(null)

    try {
      await onSubmit?.(data)
      setIsComplete(true)
    } catch {
      setSubmitError('Registration could not be completed. Please try again.')
    }
  }

  function handleEscape(event: React.KeyboardEvent<HTMLFormElement>) {
    if (event.key === 'Escape' && currentStep > 0 && !isSubmitting) {
      goToPreviousStep()
    }
  }

  if (isComplete) {
    return (
      <section className="success-message" aria-labelledby="success-heading" role="status">
        <h2 id="success-heading">Registration complete</h2>
        <p>Thanks, {values.firstName}. Your account has been created.</p>
      </section>
    )
  }

  return (
    <form
      className="registration-form"
      aria-label="Registration"
      noValidate
      onKeyDown={handleEscape}
      onSubmit={(event) => {
        event.preventDefault()
        if (currentStep < steps.length - 1) {
          void goToNextStep()
        } else {
          void handleSubmit(submitRegistration)(event)
        }
      }}
    >
      <nav aria-label="Registration progress">
        <ol className="step-list">
          {steps.map((step, index) => (
            <li
              className={index <= currentStep ? 'step step--active' : 'step'}
              key={step}
              aria-current={index === currentStep ? 'step' : undefined}
            >
              <span aria-hidden="true">{index + 1}</span>
              {step}
            </li>
          ))}
        </ol>
      </nav>

      <p className="step-count" aria-live="polite">
        Step {currentStep + 1} of {steps.length}
      </p>

      {currentStep === 0 && (
        <section aria-labelledby="personal-heading">
          <h2 id="personal-heading" ref={stepHeadingRef} tabIndex={-1}>
            Personal information
          </h2>
          <p>Tell us who you are.</p>

          <div className="field-group">
            <label htmlFor="firstName">First name</label>
            <input
              id="firstName"
              autoComplete="given-name"
              aria-invalid={Boolean(errors.firstName)}
              aria-describedby={errors.firstName ? 'firstName-error' : undefined}
              {...register('firstName')}
            />
            <FieldError id="firstName-error" message={errors.firstName?.message} />
          </div>

          <div className="field-group">
            <label htmlFor="lastName">Last name</label>
            <input
              id="lastName"
              autoComplete="family-name"
              aria-invalid={Boolean(errors.lastName)}
              aria-describedby={errors.lastName ? 'lastName-error' : undefined}
              {...register('lastName')}
            />
            <FieldError id="lastName-error" message={errors.lastName?.message} />
          </div>
        </section>
      )}

      {currentStep === 1 && (
        <section aria-labelledby="account-heading">
          <h2 id="account-heading" ref={stepHeadingRef} tabIndex={-1}>
            Account details
          </h2>
          <p>Choose the credentials you will use to sign in.</p>

          <div className="field-group">
            <label htmlFor="email">Email address</label>
            <input
              id="email"
              type="email"
              inputMode="email"
              autoComplete="email"
              aria-invalid={Boolean(errors.email)}
              aria-describedby={errors.email ? 'email-error' : undefined}
              {...register('email')}
            />
            <FieldError id="email-error" message={errors.email?.message} />
          </div>

          <div className="field-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              autoComplete="new-password"
              aria-invalid={Boolean(errors.password)}
              aria-describedby="password-help password-error"
              {...register('password')}
            />
            <p className="field-help" id="password-help">
              Use at least 8 characters, including an uppercase letter and a number.
            </p>
            <FieldError id="password-error" message={errors.password?.message} />
          </div>

          <div className="field-group">
            <label htmlFor="confirmPassword">Confirm password</label>
            <input
              id="confirmPassword"
              type="password"
              autoComplete="new-password"
              aria-invalid={Boolean(errors.confirmPassword)}
              aria-describedby={errors.confirmPassword ? 'confirmPassword-error' : undefined}
              {...register('confirmPassword')}
            />
            <FieldError
              id="confirmPassword-error"
              message={errors.confirmPassword?.message}
            />
          </div>
        </section>
      )}

      {currentStep === 2 && (
        <section aria-labelledby="confirmation-heading">
          <h2 id="confirmation-heading" ref={stepHeadingRef} tabIndex={-1}>
            Confirm your details
          </h2>
          <p>Review your information before creating your account.</p>

          <dl className="summary-list">
            <div>
              <dt>Name</dt>
              <dd>{values.firstName} {values.lastName}</dd>
            </div>
            <div>
              <dt>Email</dt>
              <dd>{values.email}</dd>
            </div>
            <div>
              <dt>Password</dt>
              <dd>••••••••</dd>
            </div>
          </dl>

          {submitError && (
            <p className="form-error" role="alert">
              {submitError}
            </p>
          )}
        </section>
      )}

      <div className="form-actions">
        {currentStep > 0 && (
          <button type="button" className="button button--secondary" onClick={goToPreviousStep}>
            Back
          </button>
        )}
        <button type="submit" className="button" disabled={isSubmitting}>
          {currentStep === steps.length - 1
            ? isSubmitting
              ? 'Creating account…'
              : 'Create account'
            : 'Next'}
        </button>
      </div>

      {currentStep > 0 && (
        <p className="keyboard-help">Press Escape to return to the previous step.</p>
      )}
    </form>
  )
}
