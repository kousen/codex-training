import type { InputHTMLAttributes, ReactNode } from 'react'
import type { UseFormRegisterReturn } from 'react-hook-form'

type CheckboxInputProps = Omit<
  InputHTMLAttributes<HTMLInputElement>,
  'aria-describedby' | 'aria-invalid' | 'className' | 'id' | 'name' | 'type'
> & {
  id: string
  label: ReactNode
  error?: string
  hint?: string
  registration: UseFormRegisterReturn
  className?: string
}

export function CheckboxInput({
  id,
  label,
  error,
  hint,
  registration,
  className,
  ...inputProps
}: CheckboxInputProps) {
  const hintId = hint ? `${id}-hint` : undefined
  const errorId = error ? `${id}-error` : undefined
  const describedBy = [hintId, errorId].filter(Boolean).join(' ') || undefined

  return (
    <div className={className ?? 'space-y-2'}>
      <label
        htmlFor={id}
        className="flex items-start gap-3 text-sm leading-6 text-slate-700"
      >
        <input
          id={id}
          type="checkbox"
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={describedBy}
          className="mt-1 size-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-600 aria-invalid:border-red-500 aria-invalid:ring-red-600"
          {...inputProps}
          {...registration}
        />
        <span>{label}</span>
      </label>
      {hint ? (
        <p id={hintId} className="pl-7 text-sm leading-6 text-slate-600">
          {hint}
        </p>
      ) : null}
      {error ? (
        <p id={errorId} className="pl-7 text-sm text-red-700" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}
