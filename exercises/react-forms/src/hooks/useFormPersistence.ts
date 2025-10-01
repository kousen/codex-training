import { useEffect, useRef } from 'react';
import type { UseFormReturn } from 'react-hook-form';

interface UseFormPersistenceOptions {
  storageKey?: string;
  enabled?: boolean;
}

type Serializable<T> = {
  [K in keyof T]: T[K] extends Date ? string : T[K];
};

const DEFAULT_STORAGE_KEY = 'registration-form-data';

const canUseStorage = () => typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';

export function useFormPersistence<T extends Record<string, unknown>>(
  form: UseFormReturn<T>,
  options: UseFormPersistenceOptions = {},
) {
  const { storageKey = DEFAULT_STORAGE_KEY, enabled = true } = options;
  const initialized = useRef(false);

  useEffect(() => {
    if (!enabled || !canUseStorage() || initialized.current) {
      return;
    }
    try {
      const raw = window.localStorage.getItem(storageKey);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<Serializable<T>>;
        form.reset({
          ...form.getValues(),
          ...parsed,
        });
      }
    } catch (error) {
      console.warn('Failed to read stored form data', error);
    } finally {
      initialized.current = true;
    }
  }, [enabled, form, storageKey]);

  useEffect(() => {
    if (!enabled || !canUseStorage()) {
      return;
    }

    const subscription = form.watch((value) => {
      if (!initialized.current) {
        return;
      }
      try {
        const sanitizedEntries = Object.entries(value).filter(([key]) =>
          !['password', 'confirmPassword', 'terms'].includes(key),
        );
        const sanitizedValue = Object.fromEntries(sanitizedEntries) as Serializable<T>;
        window.localStorage.setItem(storageKey, JSON.stringify(sanitizedValue));
      } catch (error) {
        console.warn('Failed to persist form data', error);
      }
    });

    return () => subscription.unsubscribe();
  }, [enabled, form, storageKey]);

  const clear = () => {
    if (!canUseStorage()) {
      return;
    }
    window.localStorage.removeItem(storageKey);
  };

  return { clear };
}
