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
        <div className="feature"><span>â†—</span><div><strong>Make informed upgrades</strong><p>Turn dependency changes into clearer decisions.</p></div></div>
        <div className="feature"><span>âŒ˜</span><div><strong>Built for developers</strong><p>Designed around the tools and workflows you use.</p></div></div>
      </div>
      <p className="hero-footer">â— EARLY ACCESS <span>/</span> BUILT FOR JAVA TEAMS</p>
    </aside>
    <section className="form-panel"><div className="mobile-brand"><Brand /></div><div className="form-wrap">
      <p className="form-kicker">{registering ? 'GET STARTED' : 'WELCOME BACK'}</p><h2>{registering ? 'Create your account' : 'Sign in to VersionWise'}</h2><p className="form-intro">{registering ? 'Start making more confident dependency decisions.' : 'Your next upgrade decision starts here.'}</p>
      <div className="tabs"><button type="button" className={!registering ? 'active' : ''} onClick={() => { setMode('login'); setNotice(null); setErrors({}) }}>Sign in</button><button type="button" className={registering ? 'active' : ''} onClick={() => { setMode('register'); setNotice(null); setErrors({}) }}>Create account</button></div>
      <form onSubmit={submit} noValidate>
        <label htmlFor="email">Email address</label><div className={`input-wrap ${errors.email ? 'invalid' : ''}`}><span>@</span><input id="email" type="email" autoComplete="email" placeholder="you@company.com" maxLength={254} value={email} onChange={e => { setEmail(e.target.value); setErrors(p => ({ ...p, email: undefined })); setNotice(null) }} /></div>{errors.email && <p className="field-error">{errors.email}</p>}
        <div className="password-label"><label htmlFor="password">Password</label>{registering && <span>12+ characters</span>}</div><div className={`input-wrap ${errors.password ? 'invalid' : ''}`}><span>â—‡</span><input id="password" type={showPassword ? 'text' : 'password'} autoComplete={registering ? 'new-password' : 'current-password'} placeholder={registering ? 'Create a strong password' : 'Enter your password'} maxLength={72} value={password} onChange={e => { setPassword(e.target.value); setErrors(p => ({ ...p, password: undefined })); setNotice(null) }} /><button className="show-password" type="button" onClick={() => setShowPassword(v => !v)}>{showPassword ? 'Hide' : 'Show'}</button></div>{errors.password && <p className="field-error">{errors.password}</p>}
        {notice && <div className={`notice ${notice.type}`} role={notice.type === 'error' ? 'alert' : 'status'}>{notice.text}</div>}
        <button className="primary-button" type="submit" disabled={busy}>{busy ? <><span className="spinner" /> {registering ? 'Creating accountâ€¦' : 'Signing inâ€¦'}</> : <>{registering ? 'Create account' : 'Sign in'} <span>â†’</span></>}</button>
      </form>
      <p className="switch-copy">{registering ? 'Already have an account?' : 'New to VersionWise?'} <button type="button" onClick={() => { setMode(registering ? 'login' : 'register'); setNotice(null); setErrors({}) }}>{registering ? 'Sign in' : 'Create an account'}</button></p>
      <p className="security-note">â–£ Your password is never stored by this frontend.</p>
    </div><footer className="form-footer"><span>Â© 2026 VersionWise</span><span>DEPENDENCY UPGRADE INTELLIGENCE</span></footer></section>
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
  const [dependency, setDependency] = useState({ groupId: '', artifactId: '', currentVersion: '', targetVersion: '' })
  const [analysisBusy, setAnalysisBusy] = useState(false)
  const [analysisError, setAnalysisError] = useState('')
  const [analysisResults, setAnalysisResults] = useState(null)
  const [pomFile, setPomFile] = useState(null)

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
    setAnalysisResults(null)
    setAnalysisError('')
    setPomFile(null)
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

  async function submitDependencyAnalysis(event) {
    event.preventDefault()
    setAnalysisError('')
    setAnalysisResults(null)

    const clean = Object.fromEntries(Object.entries(dependency).map(([key, value]) => [key, value.trim()]))
    if (Object.values(clean).some(value => !value)) {
      setAnalysisError('Complete all four dependency fields before analyzing.')
      return
    }
    if (!selectedProject?.id) {
      setAnalysisError('Select a project before analyzing a dependency.')
      return
    }

    const requestBody = {
      group_id: clean.groupId,
      artifact_id: clean.artifactId,
      current_version: clean.currentVersion,
      target_version: clean.targetVersion,
    }

    if (pomFile && pomFile.size > 2_000_000) {
      setAnalysisError('pom.xml must be 2 MB or smaller.')
      return
    }

    setAnalysisBusy(true)
    try {
      const basePath = `/api/projects/${selectedProject.id}/analysis`
      let projectContext = null
      if (pomFile) {
        const pomXml = await pomFile.text()
        projectContext = await apiRequest(`${basePath}/parse-pom`, {
          method: 'POST', token: session.accessToken, body: { pom_xml: pomXml },
        })
      }
      const riskAnalysis = await apiRequest(`${basePath}/analyze-upgrade`, {
        method: 'POST', token: session.accessToken, body: requestBody,
      })
      const assessment = await apiRequest(`${basePath}/assess-upgrade`, {
        method: 'POST', token: session.accessToken, body: { ...requestBody, project_context: projectContext },
      })
      setAnalysisResults({ riskAnalysis, assessment })
    } catch (err) {
      setAnalysisError(handleError(err))
    } finally {
      setAnalysisBusy(false)
    }
  }

  function renderStringList(items, emptyText = 'No items reported.') {
    if (!Array.isArray(items) || items.length === 0) return <p className="analysis-empty">{emptyText}</p>
    return <ul className="analysis-list">{items.map((item, index) => <li key={index}>{item}</li>)}</ul>
  }

  function renderFindings(items, emptyText = 'No findings reported.') {
    if (!Array.isArray(items) || items.length === 0) return <p className="analysis-empty">{emptyText}</p>
    return <div className="finding-list">{items.map((finding, index) => <article className="finding" key={`${finding.title || 'finding'}-${index}`}>
      <div className="finding-heading"><strong>{finding.title || 'Finding'}</strong>{finding.severity && <span className={`severity severity-${finding.severity.toLowerCase()}`}>{finding.severity}</span>}</div>
      <p>{finding.description || 'No description provided.'}</p>
      {Array.isArray(finding.evidenceIds) && finding.evidenceIds.length > 0 && <p className="evidence-ids">Evidence IDs: {finding.evidenceIds.join(', ')}</p>}
    </article>)}</div>
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
              {loading ? 'Refreshingâ€¦' : 'Refresh'}
            </button>
          </div>

          {loading ? (
            <div className="projects-state">
              <span className="spinner" /> Loading your projectsâ€¦
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
                      {deletingId === project.id ? 'Deletingâ€¦' : 'Delete'}
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {detailLoading && <div className="detail-panel">Loading project detailsâ€¦</div>}

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
            <section className="analysis-card">
              <div className="analysis-card-heading">
                <p className="form-kicker">DEPENDENCY ANALYSIS</p>
                <h3>Analyze an upgrade</h3>
                <p>Enter the dependency coordinates and compare the current version with your target version.</p>
              </div>
              <form className="dependency-form" onSubmit={submitDependencyAnalysis} noValidate>
                <div className="dependency-fields">
                  <div><label htmlFor="dependency-group">Group ID</label><input id="dependency-group" value={dependency.groupId} onChange={e => setDependency(p => ({ ...p, groupId: e.target.value }))} placeholder="org.springframework" maxLength={300} /></div>
                  <div><label htmlFor="dependency-artifact">Artifact ID</label><input id="dependency-artifact" value={dependency.artifactId} onChange={e => setDependency(p => ({ ...p, artifactId: e.target.value }))} placeholder="spring-core" maxLength={300} /></div>
                  <div><label htmlFor="dependency-current">Current version</label><input id="dependency-current" value={dependency.currentVersion} onChange={e => setDependency(p => ({ ...p, currentVersion: e.target.value }))} placeholder="6.2.0" maxLength={200} /></div>
                  <div><label htmlFor="dependency-target">Target version</label><input id="dependency-target" value={dependency.targetVersion} onChange={e => setDependency(p => ({ ...p, targetVersion: e.target.value }))} placeholder="6.2.1" maxLength={200} /></div>
                </div>
                <div className="pom-upload-field">
                  <label htmlFor="project-pom">Project POM <span className="optional-label">(optional, improves contextual assessment)</span></label>
                  <input id="project-pom" type="file" accept=".xml" onChange={event => { setPomFile(event.target.files?.[0] || null); setAnalysisError(''); setAnalysisResults(null) }} />
                  {pomFile && <p className="pom-file-selected">Selected: {pomFile.name}</p>}
                  <p className="pom-help">VersionWise parses the POM and sends structured project context to the AI. The file is not stored by this frontend.</p>
                </div>
                {analysisError && <div className="notice error" role="alert">{analysisError}</div>}
                <button className="primary-button analysis-submit" type="submit" disabled={analysisBusy}>{analysisBusy ? <><span className="spinner" /> Running analysis…</> : <>Analyze upgrade <span>→</span></>}</button>
              </form>

              {analysisResults && <div className="analysis-results">
                <section className="risk-summary">
                  <div><p className="card-label">DETERMINISTIC RISK SCORE</p><strong className="risk-score">{analysisResults.riskAnalysis.riskScore}<span>/100</span></strong></div>
                  <span className={`risk-category risk-${String(analysisResults.riskAnalysis.riskCategory || '').toLowerCase()}`}>{analysisResults.riskAnalysis.riskCategory || 'Uncategorized'}</span>
                  <p>{analysisResults.riskAnalysis.comparison || 'Version comparison unavailable.'}</p>
                  <p className="score-disclaimer">This score is a heuristic risk score, not a probability.</p>
                </section>
                <div className="analysis-section"><h4>Risk factors</h4>{Array.isArray(analysisResults.riskAnalysis.factors) && analysisResults.riskAnalysis.factors.length ? <div className="finding-list">{analysisResults.riskAnalysis.factors.map((factor, index) => <article className="finding" key={`${factor.ruleId || factor.name}-${index}`}><div className="finding-heading"><strong>{factor.name || factor.ruleId || 'Risk factor'}</strong><span className="factor-contribution">+{factor.contribution}</span></div><p>{factor.explanation}</p><p className="evidence-ids">{factor.evaluated ? 'Evaluated' : 'Not evaluated'}{factor.evidenceSource ? ` · ${factor.evidenceSource}` : ''}</p></article>)}</div> : <p className="analysis-empty">No risk factors returned.</p>}</div>
                <div className="analysis-section"><h4>Warnings</h4>{renderStringList(analysisResults.riskAnalysis.warnings)}</div>
                <div className="analysis-section"><h4>Recommendations</h4>{renderStringList(analysisResults.riskAnalysis.recommendations)}</div>
                <section className="assessment-summary"><p className="card-label">AI ASSESSMENT · {analysisResults.assessment.status || 'STATUS UNAVAILABLE'}</p><p>{analysisResults.assessment.summary || 'No summary returned.'}</p></section>
                <div className="analysis-section"><h4>Compatibility findings</h4>{renderFindings(analysisResults.assessment.compatibilityFindings)}</div>
                <div className="analysis-section"><h4>Breaking changes</h4>{renderFindings(analysisResults.assessment.breakingChanges)}</div>
                <div className="analysis-section"><h4>Migration concerns</h4>{renderFindings(analysisResults.assessment.migrationConcerns)}</div>
                <div className="analysis-section"><h4>Security findings</h4>{renderFindings(analysisResults.assessment.securityFindings)}</div>
                <div className="analysis-section"><h4>Evidence</h4>{Array.isArray(analysisResults.assessment.evidence) && analysisResults.assessment.evidence.length ? <div className="evidence-list">{analysisResults.assessment.evidence.map((item, index) => <article className="evidence-item" key={`${item.sourceUri || item.sourceTitle}-${index}`}><strong>{item.sourceTitle || 'Source'}</strong>{item.sourceUri && <a href={item.sourceUri} target="_blank" rel="noreferrer">Open source ↗</a>}<p>{item.excerpt || 'No excerpt provided.'}</p>{item.retrievalTimestamp && <span>{item.retrievalTimestamp}</span>}</article>)}</div> : <p className="analysis-empty">No evidence returned.</p>}</div>
                <div className="analysis-section"><h4>Limitations</h4>{renderStringList(analysisResults.assessment.limitations)}</div>
              </div>}
            </section>
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
                <button className="modal-close" type="button" onClick={closeForm} aria-label="Close form">Ã—</button>
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
                    {saving ? 'Savingâ€¦' : editingProject ? 'Save changes' : 'Create project'}
                  </button>
                </div>
              </form>
            </section>
          </div>
        )}

        <p className="scope-note">
          <strong>Dependency analysis milestone</strong><br />
          Upgrade risk analysis and evidence-grounded AI assessment are now available from a project’s details.
        </p>
      </section>

      <footer className="dashboard-footer">
        VERSIONWISE <span>â€¢</span> DEPENDENCY UPGRADE INTELLIGENCE
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
