import { forwardRef } from 'react';
import { Spinner } from './Spinner';

type ButtonVariant = 'primary' | 'secondary' | 'ghost';

type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
}

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    'bg-indigo-600 text-white hover:bg-indigo-700 focus-visible:outline-indigo-600 disabled:bg-indigo-400',
  secondary:
    'bg-white text-indigo-600 ring-1 ring-inset ring-indigo-200 hover:bg-indigo-50 focus-visible:outline-indigo-600 disabled:text-indigo-300',
  ghost:
    'bg-transparent text-indigo-600 hover:bg-indigo-50 focus-visible:outline-indigo-600 disabled:text-indigo-300',
};

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'px-3 py-2 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
};

const combine = (...classes: Array<string | undefined | false>): string =>
  classes.filter(Boolean).join(' ');

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading = false, disabled, children, ...props }, ref) => {
    const isDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        className={combine(
          'inline-flex w-full items-center justify-center gap-2 rounded-md font-semibold shadow-sm transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2',
          variantClasses[variant],
          sizeClasses[size],
          isDisabled ? 'cursor-not-allowed opacity-80' : '',
          className,
        )}
        disabled={isDisabled}
        {...props}
      >
        {loading ? <Spinner className="h-4 w-4" aria-hidden /> : null}
        <span>{children}</span>
      </button>
    );
  },
);

Button.displayName = 'Button';
