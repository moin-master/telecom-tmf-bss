import { useState, type FormEvent } from 'react'
import { useAuth } from '../hooks/useAuth'
import { apiError } from '../lib/errors'

export type AuthMode = 'register' | 'signIn'

// Create an account or sign in. The error from the backend is shown under the fields.
export function AuthForm({ mode }: { mode: AuthMode }) {
  const { signIn, register } = useAuth()
  const [givenName, setGivenName] = useState('')
  const [familyName, setFamilyName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const creating = mode === 'register'

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    setError(null)
    setBusy(true)
    try {
      if (creating) await register({ email, password, givenName, familyName })
      else await signIn(email, password)
    } catch (e) {
      const err = apiError(e)
      setError(err.code === 'Conflict' ? 'That email is already registered. Sign in instead.' : err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="auth" onSubmit={onSubmit}>
      {creating && (
        <div className="auth__row">
          <label className="field">
            <span>First name</span>
            <input value={givenName} onChange={(e) => setGivenName(e.target.value)} autoComplete="given-name" required />
          </label>
          <label className="field">
            <span>Last name</span>
            <input value={familyName} onChange={(e) => setFamilyName(e.target.value)} autoComplete="family-name" required />
          </label>
        </div>
      )}
      <label className="field">
        <span>Email</span>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="email" required />
      </label>
      <label className="field">
        <span>Password</span>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete={creating ? 'new-password' : 'current-password'}
          minLength={creating ? 8 : undefined}
          required
        />
        {creating && <small>At least 8 characters.</small>}
      </label>
      {error && (
        <p className="add__error" role="alert">
          {error}
        </p>
      )}
      <button type="submit" className="btn btn--big" disabled={busy}>
        {busy ? 'One moment' : creating ? 'Create account' : 'Sign in'}
      </button>
    </form>
  )
}
