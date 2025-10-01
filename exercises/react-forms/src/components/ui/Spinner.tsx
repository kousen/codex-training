interface SpinnerProps extends React.SVGAttributes<SVGElement> {
  label?: string;
  ariaHidden?: boolean;
}

export function Spinner({ className = 'h-5 w-5', label = 'Loading', ariaHidden, ...props }: SpinnerProps) {
  return (
    <svg
      className={`animate-spin text-indigo-600 ${className}`}
      viewBox="0 0 24 24"
      role={ariaHidden ? undefined : 'status'}
      aria-live={ariaHidden ? undefined : 'polite'}
      aria-label={ariaHidden ? undefined : label}
      {...props}
    >
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
      />
    </svg>
  );
}
