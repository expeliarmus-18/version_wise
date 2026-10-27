const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080').replace(/\/+$/, '')

export class ApiError extends Error {
  constructor(message, status = 0) { super(message); this.name = 'ApiError'; this.status = status }
}

export async function apiRequest(path, { method = 'GET', body, token, headers = {} } = {}) {
  const requestHeaders = new Headers(headers)
  requestHeaders.set('Accept', 'application/json')
  if (body !== undefined) requestHeaders.set('Content-Type', 'application/json')
  if (token) requestHeaders.set('Authorization', `Bearer ${token}`)
  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { method, headers: requestHeaders, body: body === undefined ? undefined : JSON.stringify(body) })
  } catch {
    throw new ApiError(`Could not reach the VersionWise API at ${API_BASE_URL}. Check that the backend is running and the API URL is correct.`)
  }
  if (response.status === 204) return null
  const contentType = response.headers.get('content-type') || ''
  let payload = null
  if (contentType.includes('application/json')) {
    try { payload = await response.json() } catch { payload = null }
  } else {
    const text = await response.text()
    payload = text ? { message: text } : null
  }
  if (!response.ok) throw new ApiError(payload?.detail || payload?.message || payload?.error || `Request failed with HTTP ${response.status}.`, response.status)
  return payload
}

export function getApiErrorMessage(error) {
  return error instanceof Error ? error.message : 'Something went wrong. Please try again.'
}
