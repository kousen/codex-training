import { RegistrationForm } from './components/forms/RegistrationForm';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-white to-indigo-100">
      <main className="mx-auto flex max-w-5xl flex-col items-center justify-center px-4 py-12 sm:py-16">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
            Join the community
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-slate-600">
            Create a secure account in a few quick steps. Your information stays private and helps us personalize
            your experience.
          </p>
        </div>
        <RegistrationForm />
      </main>
    </div>
  );
}

export default App;
