# VersionWise Frontend

React + Vite frontend for VersionWise authentication and the Day 4 MVP foundation.

## Setup (Windows CMD)

```bat
cd frontend
npm install
copy .env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` in `.env` if the backend uses another base URL. Vite environment variables are public client configuration; never put secrets in them.

## Commands

```bat
npm run dev
npm run build
npm run lint
```

## Authentication

- Registration calls `POST /api/auth/register` with `email` and `password`.
- Login calls `POST /api/auth/login` with `email` and `password`.
- The JWT is stored in tab-scoped `sessionStorage` until logout, expiry, or the tab session ends.
- The protected projects check calls `GET /api/projects` with `Authorization: Bearer <token>`.
- Logout clears local session state. It does not revoke the server-issued JWT; the backend currently has expiring access tokens without refresh-token support.

## Token storage limitation

`sessionStorage` is accessible to same-origin JavaScript. An XSS vulnerability could expose the token. Avoid unsafe HTML injection, keep dependencies current, and do not log tokens or put them in URLs. A future HttpOnly cookie approach requires a deliberate backend and CSRF design. Backend authorization remains the security boundary; frontend state is not.
