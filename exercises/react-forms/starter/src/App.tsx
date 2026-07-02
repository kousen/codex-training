import { RegistrationForm } from './components/RegistrationForm'

function App() {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-4xl flex-col gap-8 px-4 py-10 sm:px-6 lg:px-8">
      <header className="space-y-3">
        <p className="text-sm font-semibold tracking-wide text-indigo-600 uppercase">
          Lab 3
        </p>
        <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
          User Registration
        </h1>
        <p className="max-w-2xl text-base leading-7 text-slate-600">
          Build this starter into a production-ready multi-step form with React
          Hook Form, Zod validation, and accessible interactions.
        </p>
      </header>
      <RegistrationForm />
    </main>
  )
}

export default App
