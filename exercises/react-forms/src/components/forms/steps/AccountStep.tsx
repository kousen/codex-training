import { EmailInput } from '../sections/EmailInput';
import { PasswordSection } from '../sections/PasswordSection';
import { UsernameInput } from '../sections/UsernameInput';

export function AccountStep() {
  return (
    <div className="space-y-6" aria-describedby="account-step-description">
      <div className="space-y-1">
        <h2 className="text-lg font-semibold text-slate-800">Account details</h2>
        <p id="account-step-description" className="text-sm text-slate-500">
          Provide the information we will use to create and secure your account.
        </p>
      </div>
      <div className="space-y-6">
        <EmailInput />
        <UsernameInput />
        <PasswordSection />
      </div>
    </div>
  );
}
