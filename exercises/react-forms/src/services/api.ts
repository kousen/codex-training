import axios, { type AxiosAdapter, type AxiosResponse } from 'axios';
import type { RegistrationFormData } from '../schemas/registration';

export interface UsernameCheckResponse {
  available: boolean;
  message?: string;
}

export interface EmailCheckResponse {
  unique: boolean;
  message?: string;
}

export interface RegistrationResponse {
  success: boolean;
  message: string;
  csrfToken: string;
}

export interface Country {
  code: string;
  name: string;
}

const RESERVED_USERNAMES = new Set(['admin', 'support', 'root', 'system', 'testuser', 'demo']);
const TAKEN_EMAILS = new Set(['existing@example.com', 'user@example.com']);

const COUNTRIES: Country[] = [
  { code: 'US', name: 'United States' },
  { code: 'CA', name: 'Canada' },
  { code: 'GB', name: 'United Kingdom' },
  { code: 'AU', name: 'Australia' },
  { code: 'DE', name: 'Germany' },
  { code: 'FR', name: 'France' },
  { code: 'JP', name: 'Japan' },
  { code: 'IN', name: 'India' },
];

const requestLog: Record<string, number[]> = {};
const RATE_LIMIT_WINDOW = 10_000; // 10 seconds
const RATE_LIMIT_MAX = 5;

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const recordRequest = (key: string) => {
  const now = Date.now();
  const entries = requestLog[key] ?? [];
  const recent = entries.filter((timestamp) => now - timestamp < RATE_LIMIT_WINDOW);
  if (recent.length >= RATE_LIMIT_MAX) {
    const error = new Error('Too many requests. Please slow down.');
    error.name = 'RateLimitError';
    throw error;
  }
  recent.push(now);
  requestLog[key] = recent;
};

const parseData = <T extends Record<string, unknown>>(payload: unknown): T => {
  if (!payload) {
    return {} as T;
  }
  if (typeof payload === 'string') {
    try {
      return JSON.parse(payload) as T;
    } catch (error) {
      console.warn('Failed to parse payload', error);
      return {} as T;
    }
  }
  return payload as T;
};

const mockAdapter: AxiosAdapter = async (config) => {
  const url = config.url ?? '';
  const method = (config.method ?? 'get').toLowerCase();
  try {
    if (method === 'post' && url.endsWith('/check-username')) {
      recordRequest(url);
      const { username } = parseData<{ username: string }>(config.data);
      const response = await checkUsernameAvailability(username);
      return buildResponse(config, 200, response);
    }

    if (method === 'post' && url.endsWith('/check-email')) {
      recordRequest(url);
      const { email } = parseData<{ email: string }>(config.data);
      const response = await checkEmailUniqueness(email);
      return buildResponse(config, 200, response);
    }

    if (method === 'post' && url.endsWith('/register')) {
      recordRequest(url);
      const payload = parseData<RegistrationFormData>(config.data);
      const response = await registerUser(payload);
      return buildResponse(config, 200, response);
    }

    if (method === 'get' && url.endsWith('/countries')) {
      const response = await fetchCountries();
      return buildResponse(config, 200, response);
    }

    return buildResponse(config, 404, { message: 'Not implemented' });
  } catch (error) {
    return Promise.reject(error);
  }
};

const buildResponse = <T>(config: Parameters<AxiosAdapter>[0], status: number, data: T): AxiosResponse<T> => ({
  config,
  data,
  status,
  statusText: status >= 200 && status < 300 ? 'OK' : 'Error',
  headers: {},
});

export const api = axios.create({
  baseURL: '/api',
  timeout: 1_500,
  adapter: mockAdapter,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function checkUsernameAvailability(username: string): Promise<UsernameCheckResponse> {
  const normalized = username.trim().toLowerCase();
  await delay(600 + Math.random() * 400);
  if (!normalized) {
    return { available: false, message: 'Username is required' };
  }
  if (RESERVED_USERNAMES.has(normalized)) {
    return { available: false, message: 'Username is already taken' };
  }
  return { available: true };
}

export async function checkEmailUniqueness(email: string): Promise<EmailCheckResponse> {
  const normalized = email.trim().toLowerCase();
  await delay(500 + Math.random() * 300);
  if (!normalized) {
    return { unique: false, message: 'Email is required' };
  }
  if (TAKEN_EMAILS.has(normalized)) {
    return { unique: false, message: 'Email is already registered' };
  }
  return { unique: true };
}

export async function registerUser(data: RegistrationFormData): Promise<RegistrationResponse> {
  await delay(800 + Math.random() * 600);

  if (RESERVED_USERNAMES.has(data.username.toLowerCase())) {
    return {
      success: false,
      message: 'Selected username is no longer available. Please choose another one.',
      csrfToken: cryptoRandomToken(),
    };
  }

  TAKEN_EMAILS.add(data.email.toLowerCase());
  RESERVED_USERNAMES.add(data.username.toLowerCase());

  return {
    success: true,
    message: 'Registration successful! Welcome aboard.',
    csrfToken: cryptoRandomToken(),
  };
}

export async function fetchCountries(): Promise<Country[]> {
  await delay(300);
  return COUNTRIES;
}

const cryptoRandomToken = () => {
  const globalCrypto = typeof globalThis !== 'undefined' ? (globalThis.crypto as Crypto | undefined) : undefined;
  if (globalCrypto?.randomUUID) {
    return globalCrypto.randomUUID();
  }
  return Math.random().toString(36).slice(2, 12);
};
