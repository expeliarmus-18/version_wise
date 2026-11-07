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

Dependency Analysis (Python FastAPI)
VersionWise includes an independent Python FastAPI analysis service under ai-service/.
Current capabilities
- Parse Maven pom.xml dependency declarations into structured Pydantic models.
- Compare a dependency's current version with a proposed target version using a bounded version comparator.
- Calculate an explainable deterministic upgrade-risk score using explicit rules.
- Return risk factors, score/category, warnings, and recommendations through the analysis API.
API endpoints
Method	Endpoint	Purpose
GET	/health	Check Python service health
POST	/api/v1/parse-pom	Parse Maven POM dependency declarations
POST	/api/v1/analyze-upgrade	Analyze a proposed dependency upgrade


Interactive API documentation is available at /docs while the service is running locally.
Run the analysis service
From the repository's ai-service directory, activate the existing virtual environment and start Uvicorn:
.versionwise\Scripts\activate
python -m uvicorn app.main:app --reload
The local service is available at http://127.0.0.1:8000; Swagger UI is at http://127.0.0.1:8000/docs.

Run the Python tests from ai-service:
pytest
Risk-score interpretation and current limitations
The current risk engine is deterministic and rule-based. Its score is a heuristic, not a probability of upgrade failure and not yet an ML prediction. The comparator supports a bounded set of version formats; ambiguous or unsupported formats return unknown.

The Maven parser is not a full Maven effective-POM resolver. Parent inheritance, imported BOM resolution, transitive dependencies, profile activation, Maven settings, and environment-specific resolution are outside its current scope.

Machine learning, historical outcome data, RAG-based evidence retrieval, and LLM explanations are planned future capabilities and are not represented as completed features.


# VersionWise ML Dataset Preparation

This module provides the initial dataset preparation foundation for
historical dependency-upgrade outcome analysis.

## Current capabilities

- Normalize and validate labeled upgrade records.
- Preserve label evidence and source metadata.
- Reject unsupported labels instead of guessing.
- Remove duplicate upgrade observations.
- Split records into train, validation, and test partitions.
- Keep records sharing a split group in the same partition.
- Produce prepared CSV files and a JSON summary.

## Input

The input is a CSV file containing the fields required by
`app.ml.dataset.normalize_record`.

The dataset must contain verified labels and a meaningful `split_group`.
The group should reflect the intended generalization goal and must be
chosen before model evaluation.

## Run

From the `ai-service` directory:

```cmd
.versionwise\Scripts\python.exe -m app.ml.prepare --input data\raw\upgrades.csv --output data\processed
```

The output directory contains:

- `train.csv`
- `validation.csv`
- `test.csv`
- `summary.json`

## Current ML status

Dataset preparation is implemented, but model training is not yet
considered feasible until a real dataset has been obtained and assessed.

No model metrics or failure-prediction claims should be reported based
on synthetic test fixtures.
