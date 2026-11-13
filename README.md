# VersionWise

VersionWise is an AI-assisted Java/Maven dependency-upgrade analysis platform. It helps developers inspect declared dependencies, understand deterministic upgrade-risk signals, and—after the planned RAG and LLM milestones—review evidence-grounded upgrade recommendations.

## Current architecture

- **Frontend:** React, JavaScript, Vite, CSS.
- **Backend:** Java 21, Spring Boot 3.5.16, Spring Security, JWT, Spring Data JPA.
- **Application database:** PostgreSQL, owned by the Spring Boot backend.
- **AI service:** Python 3.10+, FastAPI and Pydantic.
- **Current dependency analysis:** Maven POM declaration parsing and a deterministic, rule-based upgrade-risk baseline.
- **Planned evidence retrieval:** official technical documentation indexed for retrieval; ChromaDB is a candidate local vector store.
- **Planned generation:** a hosted LLM that assesses structured dependency information and retrieved evidence.

The Python AI service runs independently. It is not currently connected to Spring Boot.

## Current implementation status

### Implemented

- JWT-based user registration, login and stateless backend authentication.
- User-scoped project CRUD through the Spring Boot API.
- React authentication and authenticated project dashboard.
- Independent FastAPI service with health, POM parsing and upgrade-analysis endpoints.
- Maven POM declaration parsing, including direct dependencies, dependency-management declarations, common scopes, optional flags and locally declared property substitution.
- Conservative version comparison for a bounded set of common release and qualifier formats.
- Explainable deterministic risk scoring.

### Not implemented yet

- Full Maven effective-POM resolution.
- Parent POM inheritance, imported BOM resolution, transitive dependency resolution, profile activation, Maven settings or environment-specific property resolution.
- RAG document ingestion, embedding generation, vector storage or retrieval.
- LLM calls or generated upgrade assessments.
- Spring Boot ↔ FastAPI integration and end-to-end dependency-analysis workflow.
- Any ML model or active ML dataset-preparation pipeline.

Machine learning was evaluated during Days 8–9 and rejected for the active implementation because a sufficiently representative, reliable labeled dataset was not available. The historical feasibility research is retained under `docs/ml/`; it is not an active product dependency.

## Repository structure

```text
VersionWise/
├── backend/                 # Spring Boot API, security and persistence
├── frontend/                # React + Vite application
├── ai-service/              # Independent Python analysis service
│   ├── app/
│   │   ├── analysis/        # Maven parser, comparator and rule engine
│   │   ├── api/routes/      # FastAPI endpoints
│   │   ├── core/            # Reserved for shared configuration
│   │   ├── llm/             # Reserved for Day 13 implementation
│   │   ├── models/          # API and future assessment contracts
│   │   ├── parser/          # Reserved for future parser separation if needed
│   │   └── rag/             # Reserved for Days 11–12 implementation
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── docs/
│   ├── ml/                  # Historical ML feasibility research
│   └── project-journal.md
├── README.md
└── .gitignore
```

Reserved `core`, `parser`, `rag` and `llm` packages are architectural boundaries only. They do not imply that RAG or LLM functionality has been implemented. The working Maven parser remains in `app/analysis/maven_parser.py` to avoid unnecessary churn.

## Backend setup

### Requirements

- Java 21
- Maven Wrapper (included)
- PostgreSQL

Configure the backend's environment variables before startup:

- `DB_URL`
- `DB_USERNAME`
- `DB_PASSWORD`
- `JWT_SECRET`

Run from the repository root:

```bat
cd backend
mvnw.cmd spring-boot:run
```

The backend health endpoint is `http://localhost:8080/api/health`.

### Backend API

Public endpoints:

- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`

Protected project endpoints (JWT Bearer token required):

- `POST /api/projects`
- `GET /api/projects`
- `GET /api/projects/{id}`
- `PUT /api/projects/{id}`
- `DELETE /api/projects/{id}`

Database credentials and JWT signing secrets must remain outside version control.

## Frontend setup

Requirements: Node.js and npm.

```bat
cd frontend
npm install
copy .env.example .env
npm run dev
```

The default local frontend origin is `http://localhost:5173`; the backend's development CORS configuration currently allows that origin. Frontend checks:

```bat
npm run lint
npm run build
```

Never put private API keys, database credentials or signing secrets in Vite environment variables.

## Python AI service setup

Requirements: Python 3.10 or later.

From the repository root:

```bat
cd ai-service
py -3.10 -m venv .versionwise
.versionwise\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the independent service:

```bat
python -m uvicorn app.main:app --reload
```

Local base URL: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

### AI-service endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/api/v1/parse-pom` | Parse Maven POM declarations |
| POST | `/api/v1/analyze-upgrade` | Calculate deterministic upgrade-risk signals |

Run the service tests from `ai-service/`:

```bat
pytest
```

### Parser behavior and limitations

The parser handles Maven XML namespaces and extracts project/parent coordinates, direct dependencies and dependency-management declarations separately. It captures dependency scope, type, classifier and optional status. It resolves locally declared properties, including nested references, and preserves unresolved expressions with warnings. Unsafe XML is rejected.

It is a POM declaration parser, not Maven's effective-POM engine. It does not resolve parent inheritance, imported BOMs, transitive dependencies, active profiles, Maven settings, external properties or environment-specific Maven model behavior. A dependency without a local version may receive its version from Maven dependency management or inheritance, but this service does not compute that effective version.

### Deterministic analysis behavior and limitations

The upgrade analyzer uses explicit rules and returns a score, category, evaluated factors, warnings and recommendations. The score is a heuristic signal, not a trained-model prediction, calibrated probability or guarantee of compatibility.

The version comparator intentionally supports a bounded set of common numeric versions and qualifiers. Unsupported or ambiguous formats return `unknown`; it is not a complete implementation of Apache Maven's `ComparableVersion`.

The future LLM must consider parser uncertainty and deterministic findings alongside retrieved evidence. It must be able to return `INSUFFICIENT_EVIDENCE` rather than infer compatibility from missing information.

## Planned RAG and LLM flow

```text
Maven POM
   |
   v
POM declaration parser
   |
   v
Structured dependency data
   |
   v
Deterministic upgrade analysis
   |
   +-------------------------------+
   |                               |
   v                               v
Structured analysis          RAG retrieval
signals                       (Days 11–12)
   |                               |
   +---------------+---------------+
                   |
                   v
             LLM assessment
                (Day 13)
                   |
                   v
       Structured, evidence-grounded report
```

The future report contract is defined in `app/models/assessment.py`. It includes `RECOMMENDED`, `NOT_RECOMMENDED` and `INSUFFICIENT_EVIDENCE` statuses, structured finding groups, evidence references and limitations. This is a data contract only; no retrieval or generation is active yet.

## Development roadmap

- **Days 1–5:** repository, backend, authentication and frontend project management — completed.
- **Days 6–7:** independent FastAPI service, Maven parser and deterministic analysis — completed.
- **Days 8–9:** ML feasibility research and experimental dataset preparation foundation — historical work; ML removed from active implementation on Day 10.
- **Day 10:** AI-service audit, ML cleanup and RAG/LLM boundary preparation.
- **Days 11–12:** evidence-source ingestion and RAG retrieval.
- **Day 13:** evidence-grounded LLM assessment and structured reporting.
- **Days 14–15:** Spring Boot integration and end-to-end workflow.
- **Day 16 onward:** DevOps after MVP stability.

See `docs/project-journal.md` for implementation history and verification records.
