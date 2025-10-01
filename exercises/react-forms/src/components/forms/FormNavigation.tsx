import { Button } from '../ui/Button';

interface FormNavigationProps {
  onBack: () => void;
  onNext: () => void;
  disableBack?: boolean;
  isSubmitting?: boolean;
  canProceed?: boolean;
  isLastStep?: boolean;
}

export function FormNavigation({
  onBack,
  onNext,
  disableBack = false,
  isSubmitting = false,
  canProceed = true,
  isLastStep = false,
}: FormNavigationProps) {
  return (
    <div className="flex flex-col gap-3 border-t border-slate-100 pt-4 md:flex-row md:items-center md:justify-between">
      <div className="flex w-full gap-3 md:w-auto">
        <Button type="button" variant="secondary" onClick={onBack} disabled={disableBack || isSubmitting}>
          Back
        </Button>
        <Button
          type="button"
          onClick={onNext}
          loading={isSubmitting}
          disabled={!canProceed || isSubmitting}
        >
          {isLastStep ? 'Submit' : 'Continue'}
        </Button>
      </div>
      <p className="text-xs text-slate-400 md:text-right">
        {isLastStep ? 'Review your details and submit to finish.' : 'You can review your details before submitting.'}
      </p>
    </div>
  );
}
