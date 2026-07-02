import type { InputHTMLAttributes } from 'react'
import type { UseFormRegisterReturn } from 'react-hook-form'

type TextInputProps = Omit<
  InputHTMLAttributes<HTMLInputElement>,
  'aria-describedby' | 'aria-invalid' | 'className' | 'id' | 'name'
> & {
  id: string
  label: string
  error?: string
  hint?: string
  registration: UseFormRegisterReturn
  className?: string
}

export function TextInput({
  id,
  label,
  error,
  hint,
  registration,
  className,
  ...inputProps
}: TextInputProps) {
  const hintId = hint ? `${id}-hint` : undefined
  const errorId = error ? `${id}-error` : undefined
  const describedBy = [hintId, errorId].filter(Boolean).join(' ') || undefined

  return (
    <div className={className ?? 'space-y-2'}>
      <label htmlFor={id} className="block text-sm font-medium text-slate-800">
        {label}
      </label>
      {hint ? (
        <p id={hintId} className="text-sm leading-6 text-slate-600">
          {hint}
        </p>
      ) : null}
      <input
        id={id}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={describedBy}
        className="block min-h-11 w-full rounded-md border border-slate-300 px-3 py-2 text-slate-950 shadow-sm transition outline-none placeholder:text-slate-400 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600 aria-invalid:border-red-500 aria-invalid:focus:border-red-600 aria-invalid:focus:ring-red-600"
        {...inputProps}
        {...registration}
      />
      {error ? (
        <p id={errorId} className="text-sm text-red-700" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}
