interface StepIndicatorProps {
  steps: { id: number; title: string }[];
  currentStep: number;
}

export function StepIndicator({ steps, currentStep }: StepIndicatorProps) {
  return (
    <ol className="flex flex-wrap items-center gap-4" aria-label="Registration steps">
      {steps.map((step, index) => {
        const status = index < currentStep ? 'complete' : index === currentStep ? 'current' : 'upcoming';
        return (
          <li key={step.id} className="flex items-center gap-2 text-sm">
            <span
              className={`flex h-7 w-7 items-center justify-center rounded-full border text-xs font-semibold ${
                status === 'complete'
                  ? 'border-indigo-500 bg-indigo-500 text-white'
                  : status === 'current'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-slate-200 text-slate-400'
              }`.trim()}
              aria-hidden
            >
              {index + 1}
            </span>
            <span
              className={`font-medium ${
                status === 'complete'
                  ? 'text-slate-600'
                  : status === 'current'
                    ? 'text-indigo-600'
                    : 'text-slate-400'
              }`.trim()}
            >
              {step.title}
            </span>
            {index < steps.length - 1 ? <span className="text-slate-300">/</span> : null}
          </li>
        );
      })}
    </ol>
  );
}
