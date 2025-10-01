import { CheckCircleIcon } from '@heroicons/react/24/solid';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Suspense,
  lazy,
  useCallback,
  useEffect,
  useMemo,
  useRef,
} from 'react';
import { FormProvider, type FieldPath, useForm } from 'react-hook-form';
import { accountStepSchema, registrationSchema, type RegistrationFormData } from '../../schemas/registration';
import { RegistrationProvider, useRegistrationForm } from '../../context/FormContext';
import { useFormPersistence } from '../../hooks/useFormPersistence';
import { api } from '../../services/api';
import { Card, CardContent, CardFooter, CardHeader } from '../ui/Card';
import { StepIndicator } from './StepIndicator';
import { ProgressIndicator } from './ProgressIndicator';
import { FormNavigation } from './FormNavigation';
import { Button } from '../ui/Button';

const AccountStep = lazy(() => import('./steps/AccountStep').then((module) => ({ default: module.AccountStep })));
const ProfileStep = lazy(() => import('./steps/ProfileStep').then((module) => ({ default: module.ProfileStep })));
const ConfirmationStep = lazy(() =>
  import('./steps/ConfirmationStep').then((module) => ({ default: module.ConfirmationStep })),
);

const steps = [
  { id: 0, title: 'Account' },
  { id: 1, title: 'Profile' },
  { id: 2, title: 'Confirm' },
];

const STEP_FIELDS: Array<Array<keyof RegistrationFormData>> = [
  ['email', 'username', 'password', 'confirmPassword'],
  ['firstName', 'lastName', 'phoneNumber', 'dateOfBirth', 'country', 'newsletter'],
  ['terms'],
];

const INITIAL_VALUES: RegistrationFormData = {
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
  firstName: '',
  lastName: '',
  phoneNumber: '',
  dateOfBirth: '',
  country: '',
  newsletter: false,
  terms: false,
};

function RegistrationFormInner() {
  const {
    state: { currentStep, data, isSubmitting, isValid, submissionMessage },
    dispatch,
  } = useRegistrationForm();

  const methods = useForm<RegistrationFormData>({
    defaultValues: {
      ...INITIAL_VALUES,
      ...data,
    },
    mode: 'onBlur',
    reValidateMode: 'onBlur',
    resolver: zodResolver(registrationSchema),
  });

  const { clear } = useFormPersistence(methods);

  const stepContainerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    stepContainerRef.current?.focus();
  }, [currentStep]);

  const { trigger, getValues, formState, handleSubmit, reset } = methods;

  const handleBack = useCallback(() => {
    dispatch({ type: 'PREV_STEP' });
  }, [dispatch]);

  const onSubmit = useCallback(
    async (values: RegistrationFormData) => {
      dispatch({ type: 'SUBMIT_START' });
      try {
        const accountValidation = accountStepSchema.safeParse(values);
        if (!accountValidation.success) {
          dispatch({
            type: 'SUBMIT_ERROR',
            message: 'Account information is invalid. Please review the first step.',
          });
          return;
        }

        const response = await api.post('/register', values);
        const payload = response.data as { success: boolean; message: string };
        if (payload.success) {
          clear();
          dispatch({ type: 'SUBMIT_SUCCESS', message: payload.message });
          reset(INITIAL_VALUES);
        } else {
          dispatch({ type: 'SUBMIT_ERROR', message: payload.message });
        }
      } catch (error) {
        dispatch({
          type: 'SUBMIT_ERROR',
          message: error instanceof Error ? error.message : 'Unexpected error submitting form.',
        });
      }
    },
    [clear, dispatch, reset],
  );

  const handleNext = useCallback(async () => {
    const isLastStep = currentStep === steps.length - 1;

    if (isLastStep) {
      await handleSubmit(onSubmit)();
      return;
    }

    const fields = STEP_FIELDS[currentStep];
    const isValidStep = await trigger(fields as FieldPath<RegistrationFormData>[]);

    if (!isValidStep) {
      const stepErrors = fields.reduce<Record<string, string>>((acc, field) => {
        const message = formState.errors[field]?.message;
        if (message) {
          acc[field] = String(message);
        }
        return acc;
      }, {});
      dispatch({ type: 'SET_ERRORS', errors: stepErrors });
      return;
    }

    const values = getValues();
    dispatch({ type: 'SET_FIELDS', data: values });
    dispatch({ type: 'NEXT_STEP' });
  }, [currentStep, dispatch, formState.errors, getValues, handleSubmit, onSubmit, trigger]);

  const currentStepContent = useMemo(() => {
    switch (currentStep) {
      case 0:
        return <AccountStep />;
      case 1:
        return <ProfileStep />;
      case 2:
        return <ConfirmationStep />;
      default:
        return null;
    }
  }, [currentStep]);

  return (
    <Card className="w-full max-w-3xl" role="form" aria-labelledby="registration-title">
      <CardHeader className="space-y-4">
        <div className="space-y-1">
          <h1 id="registration-title" className="text-2xl font-bold text-slate-900">
            Create your account
          </h1>
          <p className="text-sm text-slate-500">
            Complete all steps to activate your account. Fields marked optional can be filled later.
          </p>
        </div>
        <StepIndicator steps={steps} currentStep={currentStep} />
        <ProgressIndicator currentStep={currentStep} totalSteps={steps.length} />
      </CardHeader>
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <CardContent>
            {isValid ? (
              <SuccessState
                message={submissionMessage ?? 'Registration successful!'}
                onReset={() => {
                  dispatch({ type: 'RESET' });
                  clear();
                  reset(INITIAL_VALUES);
                }}
              />
            ) : (
              <div
                ref={stepContainerRef}
                tabIndex={-1}
                className="space-y-6 focus:outline-none"
                aria-live="polite"
              >
                <Suspense fallback={<div className="py-8 text-center text-sm text-slate-500">Loading step…</div>}>
                  {currentStepContent}
                </Suspense>
              </div>
            )}
          </CardContent>
          {!isValid ? (
            <CardFooter>
              <FormNavigation
                onBack={handleBack}
                onNext={handleNext}
                disableBack={currentStep === 0}
                isSubmitting={isSubmitting}
                canProceed={!isSubmitting}
                isLastStep={currentStep === steps.length - 1}
              />
            </CardFooter>
          ) : null}
        </form>
      </FormProvider>
    </Card>
  );
}

interface SuccessStateProps {
  message: string;
  onReset: () => void;
}

function SuccessState({ message, onReset }: SuccessStateProps) {
  return (
    <div className="flex flex-col items-center gap-4 text-center" role="status">
      <CheckCircleIcon className="h-12 w-12 text-emerald-500" aria-hidden />
      <div className="space-y-2">
        <p className="text-lg font-semibold text-slate-800">{message}</p>
        <p className="text-sm text-slate-500">
          We sent a confirmation email with next steps. You can now explore your dashboard.
        </p>
      </div>
      <Button type="button" onClick={onReset} className="max-w-xs">
        Register another user
      </Button>
    </div>
  );
}

export function RegistrationForm() {
  return (
    <RegistrationProvider stepCount={steps.length}>
      <RegistrationFormInner />
    </RegistrationProvider>
  );
}
