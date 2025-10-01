import { act } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { RegistrationForm } from '../../components/forms/RegistrationForm';

jest.mock('../../services/api', () => ({
  checkEmailUniqueness: jest.fn().mockResolvedValue({ unique: true }),
  checkUsernameAvailability: jest.fn().mockResolvedValue({ available: true }),
  fetchCountries: jest.fn().mockResolvedValue([]),
  api: {
    post: jest.fn().mockResolvedValue({ data: { success: true, message: 'Registration successful!' } }),
  },
}));

describe('RegistrationForm integration', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  test('completes registration flow', async () => {
    const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
    render(<RegistrationForm />);

    expect(screen.getByRole('heading', { name: /create your account/i })).toBeInTheDocument();

    await waitFor(() => expect(screen.queryByText(/loading step/i)).not.toBeInTheDocument());

    const emailInput = await screen.findByLabelText(/email address/i);

    await user.type(emailInput, 'newuser@example.com');
    await act(async () => {
      await user.tab();
    });
    await act(async () => {
      jest.advanceTimersByTime(1_000);
    });

    const usernameInput = await screen.findByLabelText(/username/i);
    await user.type(usernameInput, 'new_user_123');
    await act(async () => {
      jest.advanceTimersByTime(600);
    });

    const passwordInput = await screen.findByLabelText(/^password$/i);
    const confirmInput = await screen.findByLabelText(/confirm password/i);
    await user.type(passwordInput, 'StrongPassw0rd!');
    await user.type(confirmInput, 'StrongPassw0rd!');

    await user.click(screen.getByRole('button', { name: /continue/i }));
    await waitFor(() => expect(screen.getByRole('heading', { name: /profile information/i })).toBeInTheDocument());

    await user.type(await screen.findByLabelText(/first name/i), 'Jane');
    await user.type(await screen.findByLabelText(/last name/i), 'Doe');

    await user.click(await screen.findByRole('checkbox', { name: /keep me updated/i }));

    await user.click(screen.getByRole('button', { name: /continue/i }));
    await waitFor(() => expect(screen.getByRole('heading', { name: /review and confirm/i })).toBeInTheDocument());

    await user.click(await screen.findByRole('checkbox', { name: /i agree/i }));

    await user.click(await screen.findByRole('button', { name: /submit/i }));
    await act(async () => {
      jest.runAllTimers();
      await Promise.resolve();
    });

    await waitFor(() => expect(screen.getByText(/registration successful/i)).toBeInTheDocument());
  });
});
