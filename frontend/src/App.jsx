import {  useCallback, useEffect, useState} from 'react'
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
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [deletingId, setDeletingId] = useState(null)
  const [formOpen, setFormOpen] = useState(false)
  const [editingProject, setEditingProject] = useState(null)
  const [selectedProject, setSelectedProject] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [formError, setFormError] = useState('')
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  const handleError = useCallback((err) => {
    if (err?.status === 401) {
      clearSession()
      onLogout()
      return 'Your session has expired. Please sign in again.'
    }
    if (err?.status === 403) {
      return 'You are not authorized to perform this action.'
    }
    return getApiErrorMessage(err)
  }, [onLogout])

  const loadProjects = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const data = await apiRequest('/api/projects', {
        token: session.accessToken,
      })
      setProjects(Array.isArray(data) ? data : [])
    } catch (err) {
      setError(handleError(err))
    } finally {
      setLoading(false)
    }
  }, [session.accessToken, handleError])

  useEffect(() => {
    loadProjects()
  }, [loadProjects])

  function openCreateForm() {
    setEditingProject(null)
    setName('')
    setDescription('')
    setFormError('')
    setFormOpen(true)
  }

  function openEditForm(project) {
    setEditingProject(project)
    setName(project.name || '')
    setDescription(project.description || '')
    setFormError('')
    setSelectedProject(null)
    setFormOpen(true)
  }

  function closeForm() {
    if (saving) return
    setFormOpen(false)
    setEditingProject(null)
    setFormError('')
  }

  async function submitProject(event) {
    event.preventDefault()
    setFormError('')
    setNotice('')

    const cleanName = name.trim()
    const cleanDescription = description.trim()

    if (!cleanName) {
      setFormError('Project name is required.')
      return
    }
    if (cleanName.length > 100) {
      setFormError('Project name must not exceed 100 characters.')
      return
    }
    if (cleanDescription.length > 1000) {
      setFormError('Description must not exceed 1,000 characters.')
      return
    }

    setSaving(true)
    try {
      const updating = Boolean(editingProject)
      const path = updating
        ? `/api/projects/${editingProject.id}`
        : '/api/projects'

      await apiRequest(path, {
        method: updating ? 'PUT' : 'POST',
        token: session.accessToken,
        body: {
          name: cleanName,
          description: cleanDescription || null,
        },
      })

      setFormOpen(false)
      setEditingProject(null)
      setName('')
      setDescription('')
      setNotice(updating ? 'Project updated successfully.' : 'Project created successfully.')
      await loadProjects()
    } catch (err) {
      setFormError(handleError(err))
    } finally {
      setSaving(false)
    }
  }

  async function viewProject(project) {
    setDetailLoading(true)
    setSelectedProject(null)
    setError('')
    setNotice('')
    try {
      const data = await apiRequest(`/api/projects/${project.id}`, {
        token: session.accessToken,
      })
      setSelectedProject(data)
    } catch (err) {
      setError(handleError(err))
    } finally {
      setDetailLoading(false)
    }
  }

  async function deleteProject(project) {
    const confirmed = window.confirm(
      `Delete "${project.name}"? This action cannot be undone.`,
    )
    if (!confirmed) return

    setDeletingId(project.id)
    setError('')
    setNotice('')

    try {
      await apiRequest(`/api/projects/${project.id}`, {
        method: 'DELETE',
        token: session.accessToken,
      })
      setProjects(current => current.filter(item => item.id !== project.id))
      setSelectedProject(current => current?.id === project.id ? null : current)
      setNotice(`"${project.name}" was deleted.`)
    } catch (err) {
      setError(handleError(err))
    } finally {
      setDeletingId(null)
    }
  }

  function formatDate(value) {
    if (!value) return 'Date unavailable'
    const date = new Date(value)
    return Number.isNaN(date.getTime())
      ? 'Date unavailable'
      : date.toLocaleDateString(undefined, {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
        })
  }

  return (
    <main className="dashboard">
      <header className="dashboard-header">
        <Brand />
        <div className="dashboard-header-actions">
          <span className="signed-in-email">{session.user?.email}</span>
          <button className="logout" onClick={onLogout} type="button">
            Sign out
          </button>
        </div>
      </header>

      <section className="dashboard-main">
        <div className="projects-heading">
          <div>
            <p className="eyebrow dark">YOUR WORKSPACE</p>
            <h1>Your projects<span className="green">.</span></h1>
            <p className="dashboard-intro">
              Organize your Java projects and prepare them for dependency analysis.
            </p>
          </div>
          <button className="primary-button create-project-button" onClick={openCreateForm} type="button">
            <span>+</span> New project
          </button>
        </div>

        <div className="user-card">
          <div className="avatar">
            {(session.user?.email || 'U').charAt(0).toUpperCase()}
          </div>
          <div className="account-info">
            <p className="card-label">SIGNED IN AS</p>
            <strong>{session.user?.email}</strong>
            <p className="user-id">Account ID: {session.user?.id || 'Unavailable'}</p>
          </div>
          <span className="active-pill">SESSION ACTIVE</span>
        </div>

        {notice && <div className="notice success" role="status">{notice}</div>}
        {error && <div className="notice error" role="alert">{error}</div>}

        <section className="projects-section">
          <div className="section-heading">
            <div>
              <h2>All projects</h2>
              <p>{projects.length} {projects.length === 1 ? 'project' : 'projects'} in your workspace</p>
            </div>
            <button className="secondary-button" type="button" onClick={loadProjects} disabled={loading}>
              {loading ? 'Refreshing…' : 'Refresh'}
            </button>
          </div>

          {loading ? (
            <div className="projects-state">
              <span className="spinner" /> Loading your projects…
            </div>
          ) : error && projects.length === 0 ? (
            <div className="projects-state">
              <p>We couldn't load your projects.</p>
              <button className="secondary-button" type="button" onClick={loadProjects}>
                Try again
              </button>
            </div>
          ) : projects.length === 0 ? (
            <div className="empty-projects">
              <div className="empty-project-icon">V</div>
              <h3>Your workspace starts here</h3>
              <p>Create your first project to begin organizing your dependency-upgrade work.</p>
              <button className="primary-button" type="button" onClick={openCreateForm}>
                Create your first project
              </button>
            </div>
          ) : (
            <div className="project-grid">
              {projects.map(project => (
                <article className="project-card" key={project.id}>
                  <div className="project-card-top">
                    <span className="project-icon">V</span>
                    <span className="project-status">Project</span>
                  </div>
                  <h3>{project.name}</h3>
                  <p className="project-description">
                    {project.description || 'No description added yet.'}
                  </p>
                  <p className="project-date">Created {formatDate(project.createdAt)}</p>
                  <div className="project-card-actions">
                    <button type="button" className="secondary-button" onClick={() => viewProject(project)}>
                      View
                    </button>
                    <button type="button" className="secondary-button" onClick={() => openEditForm(project)}>
                      Edit
                    </button>
                    <button
                      type="button"
                      className="danger-button"
                      onClick={() => deleteProject(project)}
                      disabled={deletingId === project.id}
                    >
                      {deletingId === project.id ? 'Deleting…' : 'Delete'}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {detailLoading && <div className="detail-panel">Loading project details…</div>}

        {selectedProject && (
          <section className="detail-panel">
            <div className="section-heading">
              <div>
                <p className="form-kicker">PROJECT DETAILS</p>
                <h2>{selectedProject.name}</h2>
              </div>
              <button className="secondary-button" type="button" onClick={() => setSelectedProject(null)}>
                Close
              </button>
            </div>
            <p className="detail-description">
              {selectedProject.description || 'No description provided.'}
            </p>
            <dl className="project-metadata">
              <div>
                <dt>Project ID</dt>
                <dd>{selectedProject.id}</dd>
              </div>
              <div>
                <dt>Owner ID</dt>
                <dd>{selectedProject.ownerId || 'Unavailable'}</dd>
              </div>
              <div>
                <dt>Created</dt>
                <dd>{formatDate(selectedProject.createdAt)}</dd>
              </div>
            </dl>
            <button className="primary-button" type="button" onClick={() => openEditForm(selectedProject)}>
              Edit project
            </button>
          </section>
        )}

        {formOpen && (
          <div className="project-modal-backdrop" onMouseDown={event => {
            if (event.target === event.currentTarget) closeForm()
          }}>
            <section className="project-modal" role="dialog" aria-modal="true" aria-labelledby="project-form-title">
              <div className="section-heading">
                <div>
                  <p className="form-kicker">{editingProject ? 'UPDATE WORKSPACE' : 'GET STARTED'}</p>
                  <h2 id="project-form-title">{editingProject ? 'Edit project' : 'Create a project'}</h2>
                </div>
                <button className="modal-close" type="button" onClick={closeForm} aria-label="Close form">×</button>
              </div>

              <form onSubmit={submitProject} noValidate>
                <label htmlFor="project-name">Project name</label>
                <input
                  id="project-name"
                  className="project-form-input"
                  value={name}
                  onChange={event => setName(event.target.value)}
                  placeholder="e.g. Payment Service"
                  maxLength={100}
                  required
                  autoFocus
                />
                <div className="character-count">{name.length}/100 characters</div>

                <label htmlFor="project-description">Description <span className="optional-label">(optional)</span></label>
                <textarea
                  id="project-description"
                  className="project-form-input project-form-textarea"
                  value={description}
                  onChange={event => setDescription(event.target.value)}
                  placeholder="What does this project do?"
                  maxLength={1000}
                  rows={4}
                />
                <div className="character-count">{description.length}/1000 characters</div>

                {formError && <div className="notice error" role="alert">{formError}</div>}

                <div className="project-form-actions">
                  <button className="secondary-button" type="button" onClick={closeForm} disabled={saving}>
                    Cancel
                  </button>
                  <button className="primary-button" type="submit" disabled={saving}>
                    {saving ? 'Saving…' : editingProject ? 'Save changes' : 'Create project'}
                  </button>
                </div>
              </form>
            </section>
          </div>
        )}

        <p className="scope-note">
          <strong>Day 5 milestone</strong><br />
          Project management is connected to your authenticated backend. Dependency analysis will be added in a later milestone.
        </p>
      </section>

      <footer className="dashboard-footer">
        VERSIONWISE <span>•</span> DEPENDENCY UPGRADE INTELLIGENCE
      </footer>
    </main>
  )
}


export default function App() {
  const [session, setSession] = useState(() => getSession())

  function logout() {
    clearSession()
    setSession(null)
  }

  if (session) return <Dashboard session={session} onLogout={logout} />
  return <AuthPage onLogin={() => setSession(getSession())} />
}
