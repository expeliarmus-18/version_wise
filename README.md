# VersionWise

VersionWise is an AI-powered Java/Maven dependency-upgrade intelligence application designed to help developers understand upgrade risks, compatibility issues, and potential breaking changes before upgrading dependencies.

## Planned Architecture

- **Frontend:** React, JavaScript, Vite, and CSS.
- **Backend:** Java 21, Spring Boot, Spring Security, JWT, Spring Data JPA, and Maven.
- **AI service:** Python, FastAPI, Pydantic, Pandas, NumPy, and Scikit-learn.
- **Database:** PostgreSQL for application data.
- **Retrieval:** Persistent local ChromaDB for document embeddings.
- **GenAI:** Hosted LLM API, with LangChain and embeddings where useful.

## Planned Analysis

Users will analyze Maven dependency upgrades using deterministic rules, optional historical ML predictions, sourced documentation evidence, and explainable reports.

## Development Phases

- **Days 1–2:** Development environment, repository setup, backend foundation, and PostgreSQL connectivity.
- **Day 3:** Project CRUD REST APIs, JWT authentication, and project authorization.
- **Day 4:** React frontend, registration and login UI, authenticated API integration, and session handling.
- Completed

Backend foundation: Java 21, Spring Boot, Maven, and PostgreSQL.

Authentication and authorization: registration, login, BCrypt password hashing, JWT-based stateless authentication, and user-scoped project access.

Frontend authentication: React registration and login flow, authenticated session handling, and logout.

Project management: authenticated project listing, creation, detail viewing, editing, and deletion.

Dashboard UX: loading, empty, success, and error states; form validation; delete confirmation; responsive project cards.
- **DevOps:** Deferred until the MVP is stable, starting Day 16 or later.

Current MVP Progress

Completed

Backend foundation: Java 21, Spring Boot, Maven, and PostgreSQL.

Authentication and authorization: registration, login, BCrypt password hashing, JWT-based stateless authentication, and user-scoped project access.

Frontend authentication: React registration and login flow, authenticated session handling, and logout.

Project management: authenticated project listing, creation, detail viewing, editing, and deletion.

Dashboard UX: loading, empty, success, and error states; form validation; delete confirmation; responsive project cards.
### Authentication

- User registration through `POST /api/auth/register`.
- Login through `POST /api/auth/login`.
- BCrypt password hashing handled by the backend.
- Signed, expiring JWT access tokens.
- Stateless Spring Security authentication.
- The frontend sends JWT access tokens in the `Authorization: Bearer <token>` header for protected requests.
- Frontend session handling and logout behavior implemented.

### Authorization

- Project endpoints require authentication.
- Project access is scoped to the authenticated user's identity.
- Access to another user's project returns `404 Not Found`.
- Project creation, listing, retrieval, updating, and deletion use the authenticated user's authorization context.

### API Endpoints

**Public endpoints:**

- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`

**Protected project endpoints:**

- `POST /api/projects` — create a project.
- `GET /api/projects` — list the authenticated user's projects.
- `GET /api/projects/{id}` — retrieve a project.
- `PUT /api/projects/{id}` — update a project.
- `DELETE /api/projects/{id}` — delete a project.

All project endpoints require a valid JWT Bearer token.

### Configuration and Secrets

- PostgreSQL credentials are supplied through environment variables.
- The JWT signing secret is supplied through environment-based configuration.
- Frontend API configuration is provided through `frontend/.env.example`.
- The frontend defaults to the local backend at `http://localhost:8080`.
- Backend CORS currently permits the local Vite development origin `http://localhost:5173`.
- Never commit database credentials, JWT secrets, API keys, or other sensitive values.

### Verification

- Backend verification previously completed successfully with `mvnw.cmd clean verify`: 8 tests, 0 failures, 0 errors, and 0 skipped.
- Manual Postman checks for the backend were reported as successful.
- Frontend production build completed successfully.
- Frontend lint completed with zero warnings and errors.
- Backend compilation completed successfully using `mvnw.cmd -DskipTests compile`.
- Manual frontend integration checks covered multiple users, invalid login credentials, authenticated project API requests, and expected user-specific project data.

A backend compilation check with tests skipped does not replace a full test run after subsequent changes. Run the planned final verification before considering the current milestone fully closed.

## Repository Structure

```text
VersionWise/
├── backend/          # Spring Boot REST API and security
├── frontend/         # React + Vite web application
├── docs/
│   └── project-journal.md
├── README.md
└── .gitignore
```

The Python AI service, retrieval components, and dependency-analysis pipeline are planned future components and may not yet exist in the repository.

## Backend Setup

### Requirements

- Java 21
- Maven Wrapper included in the repository
- PostgreSQL

### Configuration

Configure the following environment variables in the backend run configuration:

- `DB_URL`
- `DB_USERNAME`
- `DB_PASSWORD`
- The JWT signing secret required by the backend configuration, `app.security.jwt-secret`

Use a sufficiently strong JWT signing secret that satisfies the backend's minimum-length validation. Keep all secrets outside version control.

### Run the Backend

From the repository root, run:

```bat
cd backend
mvnw.cmd spring-boot:run
```

Alternatively, open the repository in IntelliJ IDEA and run:

`com.versionwise.backend.BackendApplication`

Ensure PostgreSQL is running and the required environment variables are configured first.

### Health Check

`http://localhost:8080/api/health`

## Frontend Setup

### Requirements

- Node.js
- npm

### Install Dependencies

From the repository root:

```bat
cd frontend
npm install
```

### Configure the API URL

The frontend includes `.env.example` with the development API URL:

```dotenv
VITE_API_BASE_URL=http://localhost:8080
```

For the default local configuration, copy the example file:

```bat
copy .env.example .env
```

Vite environment variables are exposed to client-side code. Never place passwords, signing secrets, or private API keys in frontend environment variables.

### Run the Frontend

```bat
npm run dev
```

Open `http://localhost:5173/` in your browser.

### Frontend Checks

Run these commands from the `frontend` directory:

```bat
npm run lint
npm run build
```

The backend and PostgreSQL must be running for full end-to-end API functionality.

## Backend API — Projects

Base path: `/api/projects`

| Method | Endpoint | Purpose | Success status |
|---|---|---|---|
| POST | `/api/projects` | Create a project | `201 Created` |
| GET | `/api/projects` | List the authenticated user's projects | `200 OK` |
| GET | `/api/projects/{id}` | Retrieve a project | `200 OK` |
| PUT | `/api/projects/{id}` | Update a project | `200 OK` |
| DELETE | `/api/projects/{id}` | Delete a project | `204 No Content` |

All endpoints require a valid JWT Bearer token.

### Create or Update a Project

Example JSON request:

```json
{
  "name": "My first project",
  "description": "A sample project for VersionWise"
}
```

Validation rules:

- `name` is required, must not be blank, and must contain at most 100 characters.
- `description` is optional and may contain at most 1000 characters.
- Project IDs are UUIDs.
- Missing projects return `404 Not Found`.
- Invalid request bodies should return `400 Bad Request`.

### Authentication API

#### Register

`POST /api/auth/register`

Example request:

```json
{
  "email": "alice@example.com",
  "password": "a-long-development-password"
}
```

The password must satisfy the backend's configured validation rules. Registration returns the created user's public information; it does not return the user's password.

#### Login

`POST /api/auth/login`

Example request:

```json
{
  "email": "alice@example.com",
  "password": "a-long-development-password"
}
```

Successful login returns an access token, token type, expiration information, and public user information. Use the returned token to access protected endpoints:

```http
Authorization: Bearer <access-token>
```

Invalid credentials are rejected by the backend.

## Security Notes and Limitations

- The frontend is currently configured for local development.
- The development CORS configuration allows `http://localhost:5173`; production deployment requires an explicitly configured frontend origin.
- Browser-side token storage has security trade-offs. Review token storage, XSS protections, HTTPS, and session expiration behavior before production deployment.
- JWT signing secrets and database credentials must be managed securely outside source control.
- The Python AI service, retrieval infrastructure, hosted LLM integration, and complete dependency-analysis pipeline remain planned work until implemented and verified.
Current Architecture

Frontend: React, JavaScript, Vite.

Backend: Java, Spring Boot, Spring Security, JWT, Spring Data JPA.

Database: PostgreSQL.

API authentication: protected requests use the JWT Bearer token.

Roadmap

The next milestone is the Python FastAPI foundation and Maven dependency parsing. Deterministic dependency-upgrade risk analysis, historical failure-category ML, documentation retrieval, and LLM-generated reports remain future milestones.

The MVP is being developed incrementally. Features listed as roadmap items should not be considered implemented until their milestones are completed and verified.


## Python AI Service

VersionWise includes an independent Python analysis service built with FastAPI. The service is responsible for Maven dependency parsing and will support future dependency-upgrade risk analysis.

### Technology

- Python 3.10.11
- FastAPI
- Pydantic
- Uvicorn
- defusedxml
- pytest
- HTTPX

### Environment Setup

The Python service uses a dedicated virtual environment located at `ai-service/.versionwise`.

From the repository root, run:

```cmd
cd ai-service

python -m venv .versionwise

.versionwise\Scripts\activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

### Start the Service

From the `ai-service` directory, with the virtual environment activated:

```cmd
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Health Endpoint

`GET /health`

Returns the service status.

### Maven POM Parsing

`POST /api/v1/parse-pom`

Accepts Maven POM XML through a JSON request:

```json
{
  "pom_xml": "<project><groupId>com.example</groupId><artifactId>demo</artifactId><version>1.0</version></project>"
}
```

The response includes:

- Project coordinates
- Parent coordinates
- Direct dependencies
- Dependency-management entries
- Resolved and unresolved version expressions
- Dependency scope, type, classifier and optional metadata
- Parsing warnings

### Parser Capabilities and Limitations

The parser supports Maven XML namespaces, direct dependencies, dependency-management declarations, local property substitution, nested property references and parent coordinate extraction.

Unresolved property expressions are preserved and flagged.

The parser does not implement complete Maven effective-POM resolution. Parent inheritance, imported BOM resolution, transitive dependencies, activated profiles, Maven settings and environment-specific properties are not resolved.

The service does not currently persist uploaded POM files or require PostgreSQL.

### Automated Testing

From `ai-service`, run:

```cmd
python -m pytest -v
```

Day 6 verification result: 21 tests passed, 0 failures, with one Starlette deprecation warning.

### Next Milestone

Day 7 will introduce a deterministic dependency-upgrade risk engine using the structured Maven dependency information produced by this service.