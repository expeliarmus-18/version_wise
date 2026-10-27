const SESSION_KEY = 'versionwise.session'

export function saveSession({ accessToken, tokenType, expiresIn, user }) {
  const session = { accessToken, tokenType: tokenType || 'Bearer', expiresAt: Date.now() + (Number(expiresIn) || 3600) * 1000, user }
  // sessionStorage is tab-scoped but readable by same-origin JavaScript. Never store passwords or log this value.
  window.sessionStorage.setItem(SESSION_KEY, JSON.stringify(session))
  return session
}

export function getSession() {
  try {
    const raw = window.sessionStorage.getItem(SESSION_KEY)
    if (!raw) return null
    const session = JSON.parse(raw)
    if (!session?.accessToken || !session?.user || !session?.expiresAt || Date.now() >= session.expiresAt) { clearSession(); return null }
    return session
  } catch { clearSession(); return null }
}

export function clearSession() { window.sessionStorage.removeItem(SESSION_KEY) }
