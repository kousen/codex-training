import { useEffect, useState } from 'react';
import { useFormContext } from 'react-hook-form';
import type { RegistrationFormData } from '../../../schemas/registration';
import { fetchCountries, type Country } from '../../../services/api';
import { FormInput } from '../FormInput';
import { Spinner } from '../../ui/Spinner';

export function ProfileStep() {
  const {
    register,
    watch,
    formState: { errors },
  } = useFormContext<RegistrationFormData>();
  const [countries, setCountries] = useState<Country[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const load = async () => {
      setLoading(true);
      try {
        const response = await fetchCountries();
        if (active) {
          setCountries(response);
        }
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : 'Unable to load countries');
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    load();
    return () => {
      active = false;
    };
  }, []);

  const newsletter = watch('newsletter');
  const newsletterRegistration = register('newsletter');

  return (
    <div className="space-y-6" aria-describedby="profile-step-description">
      <div className="space-y-1">
        <h2 className="text-lg font-semibold text-slate-800">Profile information</h2>
        <p id="profile-step-description" className="text-sm text-slate-500">
          Tell us more about yourself. These details are optional and help tailor your experience.
        </p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <FormInput name="firstName" label="First name" optional placeholder="Jane" />
        <FormInput name="lastName" label="Last name" optional placeholder="Doe" />
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <FormInput
          name="phoneNumber"
          label="Phone number"
          optional
          type="tel"
          inputMode="tel"
          placeholder="+1234567890"
          description="Include your country code for international format."
        />
        <div className="space-y-1">
          <label htmlFor="dateOfBirth" className="text-sm font-medium text-slate-700">
            Date of birth
          </label>
          <input
            id="dateOfBirth"
            type="date"
            className={`block w-full rounded-md border px-3 py-2 text-sm shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-0 ${
              errors.dateOfBirth ? 'border-red-500 text-red-900 focus:ring-red-500' : 'border-slate-300'
            }`.trim()}
            aria-invalid={errors.dateOfBirth ? 'true' : 'false'}
            aria-describedby={errors.dateOfBirth ? 'dob-error' : undefined}
            {...register('dateOfBirth')}
          />
          {errors.dateOfBirth ? (
            <p id="dob-error" className="text-xs text-red-600" role="alert">
              {errors.dateOfBirth.message}
            </p>
          ) : (
            <p className="text-xs text-slate-500">You must be at least 18 years old.</p>
          )}
        </div>
      </div>
      <div className="space-y-1">
        <label htmlFor="country" className="text-sm font-medium text-slate-700">
          Country
        </label>
        <div className="relative">
          <select
            id="country"
            className="block w-full appearance-none rounded-md border border-slate-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            {...register('country')}
          >
            <option value="">Select your country (optional)</option>
            {countries.map((country) => (
              <option key={country.code} value={country.code}>
                {country.name}
              </option>
            ))}
          </select>
          <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400" aria-hidden>
            ▾
          </span>
        </div>
        {error ? <p className="text-xs text-red-600">{error}</p> : null}
        {loading ? (
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Spinner className="h-3 w-3" ariaHidden />
            <span>Loading country list…</span>
          </div>
        ) : null}
      </div>
      <label className="flex items-center gap-3 rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
        <input
          type="checkbox"
          className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
          {...newsletterRegistration}
          checked={Boolean(newsletter)}
          onChange={(event) => newsletterRegistration.onChange(event)}
        />
        <span>Keep me updated with product news and offers.</span>
      </label>
    </div>
  );
}
