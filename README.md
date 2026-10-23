# VersionWise

VersionWise is an AI-powered Java/Maven dependency-upgrade intelligence application.

## Planned architecture

- Frontend: React, JavaScript, Vite and CSS.
- Backend: Java 21, Spring Boot, Spring Security, JWT, Spring Data JPA and Maven.
- AI service: Python, FastAPI, Pydantic, Pandas, NumPy and Scikit-learn.
- Database: PostgreSQL for application data.
- Retrieval: persistent local ChromaDB for document embeddings.
- GenAI: hosted LLM API, with LangChain and embeddings where useful.

## Planned analysis

Users will analyze Maven dependency upgrades using deterministic rules, optional historical ML predictions, sourced documentation evidence and explainable reports.

## Development phases

- Days 1-2: Environment, repository and backend foundation.
- Following MVP phase: Backend APIs, persistence, AI service, analysis pipeline and frontend integration.
- DevOps: Deferred until the MVP is stable, starting Day 16 or later.



## Current status

Day 1: Environment inspection completed. Repository foundation is being established. Application components have not yet been implemented.

### Backend

The backend uses Java 21, Spring Boot 3.5.16, Maven,
Spring Web, Spring Data JPA, and PostgreSQL.

Open the repository in IntelliJ IDEA and run
`com.versionwise.backend.BackendApplication`.

Configure `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD`
in the run configuration before starting the application.

Health endpoint: `http://localhost:8080/api/health`

## Backend API — Projects

Base path: `/api/projects`

| Method | Endpoint | Purpose | Success status |
|---|---|---|---|
| POST | `/api/projects` | Create a project | `201 Created` |
| GET | `/api/projects` | List development-user projects | `200 OK` |
| GET | `/api/projects/{id}` | Retrieve a project | `200 OK` |
| PUT | `/api/projects/{id}` | Update a project | `200 OK` |
| DELETE | `/api/projects/{id}` | Delete a project | `204 No Content` |

### Create or update a project

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

Missing projects return `404 Not Found`. Invalid request bodies should return `400 Bad Request`.

### Development-only limitation

The current implementation associates projects with a fixed development user (`dev@versionwise.local`). This is temporary scaffolding for local development. Authentication, registration, and secure per-user authorization are not implemented by this endpoint design yet. Do not deploy it as a production API.
