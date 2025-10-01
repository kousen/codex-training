import { useMemo } from 'react';
import { useFormContext } from 'react-hook-form';
import type { RegistrationFormData } from '../../../schemas/registration';

export function ConfirmationStep() {
  const {
    watch,
    register,
    formState: { errors },
  } = useFormContext<RegistrationFormData>();

  const data = watch();

  const summary = useMemo(
    () => [
      { label: 'Email', value: data.email },
      { label: 'Username', value: data.username },
      { label: 'First name', value: data.firstName || '—' },
      { label: 'Last name', value: data.lastName || '—' },
      { label: 'Phone', value: data.phoneNumber || '—' },
      { label: 'Date of birth', value: data.dateOfBirth || '—' },
      { label: 'Country', value: data.country || '—' },
      { label: 'Newsletter', value: data.newsletter ? 'Subscribed' : 'Not subscribed' },
    ],
    [data],
  );

  return (
    <div className="space-y-6" aria-describedby="confirmation-step-description">
      <div className="space-y-1">
        <h2 className="text-lg font-semibold text-slate-800">Review and confirm</h2>
        <p id="confirmation-step-description" className="text-sm text-slate-500">
          Please confirm your details. You can go back to make changes before submitting.
        </p>
      </div>
      <dl className="grid gap-4 rounded-lg border border-slate-200 bg-white p-4 md:grid-cols-2">
        {summary.map((item) => (
          <div key={item.label}>
            <dt className="text-xs uppercase tracking-wide text-slate-400">{item.label}</dt>
            <dd className="text-sm text-slate-700">{item.value}</dd>
          </div>
        ))}
      </dl>
      <div className="space-y-3 rounded-md border border-slate-200 bg-slate-50 p-4">
        <label className="flex items-start gap-3 text-sm text-slate-700">
          <input
            type="checkbox"
            className="mt-1 h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
            {...register('terms')}
          />
          <span>
            I agree to the <a href="#" className="text-indigo-600 underline">Terms of Service</a> and{' '}
            <a href="#" className="text-indigo-600 underline">Privacy Policy</a>.
          </span>
        </label>
        {errors.terms ? (
          <p className="text-xs text-red-600" role="alert">
            {errors.terms.message}
          </p>
        ) : (
          <p className="text-xs text-slate-500">You must agree before submitting.</p>
        )}
      </div>
      <p className="text-xs text-slate-500">
        By submitting, you acknowledge that we will process your information in accordance with our privacy policy.
      </p>
    </div>
  );
}
