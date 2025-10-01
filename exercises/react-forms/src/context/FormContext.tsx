import { createContext, useContext, useMemo, useReducer } from 'react';
import type { RegistrationFormData } from '../schemas/registration';

export interface FormErrors {
  [key: string]: string | undefined;
}

export interface TouchedFields {
  [key: string]: boolean | undefined;
}

export interface FormState {
  currentStep: number;
  data: Partial<RegistrationFormData>;
  errors: FormErrors;
  touched: TouchedFields;
  isSubmitting: boolean;
  isValid: boolean;
  submissionMessage?: string;
}

export type FormAction =
  | { type: 'SET_FIELD'; field: keyof RegistrationFormData; value: RegistrationFormData[keyof RegistrationFormData] }
  | { type: 'SET_FIELDS'; data: Partial<RegistrationFormData> }
  | { type: 'SET_ERRORS'; errors: FormErrors }
  | { type: 'SET_TOUCHED'; touched: TouchedFields }
  | { type: 'NEXT_STEP' }
  | { type: 'PREV_STEP' }
  | { type: 'SET_STEP'; step: number }
  | { type: 'SUBMIT_START' }
  | { type: 'SUBMIT_SUCCESS'; message?: string }
  | { type: 'SUBMIT_ERROR'; message?: string }
  | { type: 'RESET' };

const initialState: FormState = {
  currentStep: 0,
  data: {},
  errors: {},
  touched: {},
  isSubmitting: false,
  isValid: false,
  submissionMessage: undefined,
};

const reducer = (state: FormState, action: FormAction): FormState => {
  switch (action.type) {
    case 'SET_FIELD':
      return {
        ...state,
        data: {
          ...state.data,
          [action.field]: action.value,
        },
      };
    case 'SET_FIELDS':
      return {
        ...state,
        data: {
          ...state.data,
          ...action.data,
        },
      };
    case 'SET_ERRORS':
      return { ...state, errors: action.errors };
    case 'SET_TOUCHED':
      return { ...state, touched: { ...state.touched, ...action.touched } };
    case 'NEXT_STEP':
      return { ...state, currentStep: state.currentStep + 1 };
    case 'PREV_STEP':
      return { ...state, currentStep: Math.max(0, state.currentStep - 1) };
    case 'SET_STEP':
      return { ...state, currentStep: action.step };
    case 'SUBMIT_START':
      return { ...state, isSubmitting: true, submissionMessage: undefined };
    case 'SUBMIT_SUCCESS':
      return {
        ...state,
        isSubmitting: false,
        isValid: true,
        submissionMessage: action.message ?? 'Registration complete.',
      };
    case 'SUBMIT_ERROR':
      return {
        ...state,
        isSubmitting: false,
        submissionMessage: action.message ?? 'Unable to complete registration. Please try again.',
      };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
};

interface RegistrationContextValue {
  state: FormState;
  dispatch: React.Dispatch<FormAction>;
  stepCount: number;
}

const RegistrationContext = createContext<RegistrationContextValue | undefined>(undefined);

interface RegistrationProviderProps {
  children: React.ReactNode;
  stepCount?: number;
}

export function RegistrationProvider({ children, stepCount = 3 }: RegistrationProviderProps) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const value = useMemo(
    () => ({
      state,
      dispatch,
      stepCount,
    }),
    [state, stepCount],
  );

  return <RegistrationContext.Provider value={value}>{children}</RegistrationContext.Provider>;
}

export function useRegistrationForm() {
  const context = useContext(RegistrationContext);
  if (!context) {
    throw new Error('useRegistrationForm must be used within a RegistrationProvider');
  }
  return context;
}
