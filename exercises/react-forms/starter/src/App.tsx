import { RegistrationForm } from './components/RegistrationForm'
import './styles.css'

function App() {
  return (
    <main className="app-shell">
      <div className="form-card">
        <header className="page-header">
          <p className="eyebrow">Create your account</p>
          <h1>User registration</h1>
          <p>Complete the three short steps below.</p>
        </header>
        <RegistrationForm />
      </div>
    </main>
  )
}

export default App
