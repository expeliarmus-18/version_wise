import { useState } from 'react'
import { apiRequest, getApiErrorMessage } from './api/client.js'
import { clearSession, getSession, saveSession } from './auth/session.js'
import './App.css'

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Brand() {
  return <div className="brand"><span className="brand-mark">V</span><span>versionwise<span className="green">.</span></span></div>
}

function AuthPage({ onLogin }) {
  const [mode, setMode] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [busy, setBusy] = useState(false)
  const [notice, setNotice] = useState(null)
  const [errors, setErrors] = useState({})
  const registering = mode === 'register'

  function validate() {
    const next = {}
    if (!email.trim() || !EMAIL_PATTERN.test(email.trim()) || email.trim().length > 254) next.email = 'Enter a valid email address.'
    if (!password) next.password = 'Enter your password.'
    else if (registering && password.length < 12) next.password = 'Use at least 12 characters.'
    else if (password.length > 72) next.password = 'Password must be no more than 72 characters.'
    setErrors(next)
    return Object.keys(next).length === 0
  }

  async function submit(event) {
    event.preventDefault()
    setNotice(null)
    if (!validate()) return
    setBusy(true)
    try {
      if (registering) {
        await apiRequest('/api/auth/register', { method: 'POST', body: { email: email.trim(), password } })
        setMode('login')
        setPassword('')
        setNotice({ type: 'success', text: 'Account created. Sign in with your new credentials.' })
      } else {
        const result = await apiRequest('/api/auth/login', { method: 'POST', body: { email: email.trim(), password } })
        if (!result?.accessToken || !result?.user || result?.tokenType?.toLowerCase() !== 'bearer') throw new Error('The server returned an unexpected login response.')
        saveSession(result)
        onLogin()
      }
    } catch (error) {
      setNotice({ type: 'error', text: getApiErrorMessage(error) })
    } finally {
      setBusy(false)
    }
  }

  return <main className="auth-layout">
    <aside className="hero-panel">
      <div className="hero-top"><Brand /><span className="preview-pill"><i /> MVP PREVIEW</span></div>
      <div className="hero-copy"><p className="eyebrow">DEPENDENCY INTELLIGENCE</p><h1>Upgrade with<br /><span>confidence.</span></h1><p className="hero-description">Understand what changes, what breaks, and what to do next before your dependencies move forward.</p>
        <div className="feature"><span>↗</span><div><strong>Make informed upgrades</strong><p>Turn dependency changes into clearer decisions.</p></div></div>
        <div className="feature"><span>⌘</span><div><strong>Built for developers</strong><p>Designed around the tools and workflows you use.</p></div></div>
      </div>
      <p className="hero-footer">● EARLY ACCESS <span>/</span> BUILT FOR JAVA TEAMS</p>
    </aside>
    <section className="form-panel"><div className="mobile-brand"><Brand /></div><div className="form-wrap">
      <p className="form-kicker">{registering ? 'GET STARTED' : 'WELCOME BACK'}</p><h2>{registering ? 'Create your account' : 'Sign in to VersionWise'}</h2><p className="form-intro">{registering ? 'Start making more confident dependency decisions.' : 'Your next upgrade decision starts here.'}</p>
      <div className="tabs"><button type="button" className={!registering ? 'active' : ''} onClick={() => { setMode('login'); setNotice(null); setErrors({}) }}>Sign in</button><button type="button" className={registering ? 'active' : ''} onClick={() => { setMode('register'); setNotice(null); setErrors({}) }}>Create account</button></div>
      <form onSubmit={submit} noValidate>
        <label htmlFor="email">Email address</label><div className={`input-wrap ${errors.email ? 'invalid' : ''}`}><span>@</span><input id="email" type="email" autoComplete="email" placeholder="you@company.com" maxLength={254} value={email} onChange={e => { setEmail(e.target.value); setErrors(p => ({ ...p, email: undefined })); setNotice(null) }} /></div>{errors.email && <p className="field-error">{errors.email}</p>}
        <div className="password-label"><label htmlFor="password">Password</label>{registering && <span>12+ characters</span>}</div><div className={`input-wrap ${errors.password ? 'invalid' : ''}`}><span>◇</span><input id="password" type={showPassword ? 'text' : 'password'} autoComplete={registering ? 'new-password' : 'current-password'} placeholder={registering ? 'Create a strong password' : 'Enter your password'} maxLength={72} value={password} onChange={e => { setPassword(e.target.value); setErrors(p => ({ ...p, password: undefined })); setNotice(null) }} /><button className="show-password" type="button" onClick={() => setShowPassword(v => !v)}>{showPassword ? 'Hide' : 'Show'}</button></div>{errors.password && <p className="field-error">{errors.password}</p>}
        {notice && <div className={`notice ${notice.type}`} role={notice.type === 'error' ? 'alert' : 'status'}>{notice.text}</div>}
        <button className="primary-button" type="submit" disabled={busy}>{busy ? <><span className="spinner" /> {registering ? 'Creating account…' : 'Signing in…'}</> : <>{registering ? 'Create account' : 'Sign in'} <span>→</span></>}</button>
      </form>
      <p className="switch-copy">{registering ? 'Already have an account?' : 'New to VersionWise?'} <button type="button" onClick={() => { setMode(registering ? 'login' : 'register'); setNotice(null); setErrors({}) }}>{registering ? 'Sign in' : 'Create an account'}</button></p>
      <p className="security-note">▣ Your password is never stored by this frontend.</p>
    </div><footer className="form-footer"><span>© 2026 VersionWise</span><span>DEPENDENCY UPGRADE INTELLIGENCE</span></footer></section>
  </main>
}

function Dashboard({ session, onLogout }) {
  const [result, setResult] = useState({ status: 'idle', text: '' })
  async function checkApi() {
    setResult({ status: 'loading', text: '' })
    try {
      const projects = await apiRequest('/api/projects', { token: session.accessToken })
      setResult({ status: 'success', text: `Authenticated request succeeded. Projects returned: ${Array.isArray(projects) ? projects.length : 'response received'}.` })
    } catch (error) {
      setResult({ status: 'error', text: getApiErrorMessage(error) })
    }
  }
  return <main className="dashboard"><header className="dashboard-header"><Brand /><button className="logout" onClick={onLogout}>Sign out ↗</button></header><section className="dashboard-main"><p className="eyebrow dark">YOUR WORKSPACE</p><h1>You're signed in<span className="green">.</span></h1><p className="dashboard-intro">Welcome to VersionWise. Your authenticated session is ready.</p>
    <div className="user-card"><div className="avatar">{(session.user?.email || 'U').charAt(0).toUpperCase()}</div><div><p className="card-label">SIGNED IN AS</p><strong>{session.user?.email}</strong><p className="user-id">Account ID: {session.user?.id || 'Unavailable'}</p></div><span className="active-pill">● SESSION ACTIVE</span></div>
    <div className="api-card"><p className="form-kicker">API CONNECTION</p><h2>Authenticated projects endpoint</h2><p>Check the protected projects endpoint to verify the frontend sends your JWT as a Bearer token.</p><button className="primary-button check-button" onClick={checkApi} disabled={result.status === 'loading'}>{result.status === 'loading' ? 'Checking endpoint…' : 'Check authenticated API'} <span>→</span></button>{result.status !== 'idle' && result.status !== 'loading' && <div className={`api-result ${result.status}`} role={result.status === 'error' ? 'alert' : 'status'}>{result.text}</div>}</div>
    <p className="scope-note"><strong>Day 4 MVP foundation</strong><br />Project creation, dependency analysis, results, and history are planned for the next milestone.</p>
  </section><footer className="dashboard-footer">VERSIONWISE <span>•</span> DEPENDENCY UPGRADE INTELLIGENCE</footer></main>
}

export default function App() {
  const [session, setSession] = useState(() => getSession())
  function logout() { clearSession(); setSession(null) }
  if (session) return <Dashboard session={session} onLogout={logout} />
  return <AuthPage onLogin={() => setSession(getSession())} />
}
