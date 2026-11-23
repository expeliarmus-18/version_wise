# VersionWise

VersionWise is a full-stack application for assessing Java/Maven dependency upgrades. It combines deterministic dependency analysis with documentation-grounded AI assessment to help developers understand upgrade risks, relevant migration guidance, and potential compatibility concerns.

## Features

- **Dependency upgrade analysis:** compare a dependency's current and target versions.
- **Deterministic risk analysis:** rule-based findings and risk scoring provide a consistent baseline.
- **Documentation-grounded assessment:** retrieve relevant Maven and framework documentation using hybrid retrieval.
- **Local LLM assessment:** use Ollama for locally hosted assessment generation.
- **Optional Maven project context:** upload a `pom.xml` to provide project coordinates, dependency declarations, parent information, and dependency-management context.
- **Project management:** authenticated users can create and manage projects.
- **Evidence-aware output:** assessments are expected to distinguish supported findings from insufficient evidence rather than treating project context as technical proof.

## Architecture

```text
React + Vite frontend
        |
        v
Spring Boot backend
  - Authentication
  - User-scoped project management
  - Analysis workflow / AI-service integration
        |
        v
FastAPI AI service
  - Maven POM parsing
  - Deterministic analysis
  - Documentation ingestion
  - Dense + BM25 hybrid retrieval
  - Local Ollama assessment
        |
        +---- ChromaDB documentation store
        |
        +---- Ollama local models
```

### Technology stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | Java 21, Spring Boot |
| Persistence | PostgreSQL |
| AI service | Python, FastAPI, Pydantic |
| Documentation retrieval | LangChain, ChromaDB, dense semantic retrieval, BM25, Reciprocal Rank Fusion |
| Local model runtime | Ollama |

## Repository structure

```text
VersionWise/
├── backend/              # Spring Boot application
├── frontend/             # React + Vite application
├── ai-service/           # FastAPI analysis and AI service
├── docs/
│   └── rag/
│       └── architecture.md
└── README.md
```

Personal development journal and local generated data are intentionally not part of the public repository.

## Prerequisites

- Java 21
- Node.js and npm
- Python 3.10+
- PostgreSQL
- Ollama, for local LLM assessment

## Running locally

The services run independently. Configure each service using its local environment configuration and the examples provided in the corresponding directories.

### 1. Backend

From `backend/`, configure the database and required application environment variables. The backend uses PostgreSQL and provides authentication, project management, and the application analysis workflow.

On Windows PowerShell:

```powershell
cd backend
.\mvnw.cmd spring-boot:run
```

### 2. Frontend

From `frontend/`:

```powershell
npm install
npm run dev
```

Use the frontend's environment example to configure the backend URL for local development.

### 3. AI service

From `ai-service/`, create and activate a Python virtual environment, install dependencies, and start FastAPI:

```powershell
cd ai-service
py -3.10 -m venv .versionwise
.\.versionwise\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`.

### 4. Local model runtime

Install Ollama and pull the configured models:

```powershell
ollama pull phi4-mini
ollama pull nomic-embed-text
ollama serve
```

The AI service can be configured through the `OLLAMA_*` environment variables documented in `ai-service/README.md`.

### 5. Documentation ingestion

The AI service's documentation corpus must be ingested before retrieval can use the local documentation store. From the `ai-service/` directory, with the Python environment active:

```powershell
python -m app.rag.ingest
```

The ingestion command reports source processing results, chunk counts, and storage information.

## Testing

### Frontend

```powershell
cd frontend
npm run lint
npm run build
```

### Backend

From `backend/`:

```powershell
.\mvnw.cmd test
```

### AI service

From `ai-service/`, with the Python environment active:

```powershell
python -m pytest tests -q
```

The finalization test run completed successfully:

- Frontend build: passed
- Frontend lint: 0 errors; one non-blocking warning
- Backend: 8 tests passed
- AI service: 100 tests passed

## Important limitations

- Maven parsing is not equivalent to resolving a Maven effective POM. Parent inheritance, imported BOM resolution, active profiles, Maven settings, transitive dependencies, and environment-specific properties are not fully resolved.
- Version comparison is conservative and bounded; it is not a complete implementation of Maven's `ComparableVersion`.
- Deterministic risk findings are heuristic signals, not calibrated probabilities of upgrade failure.
- An uploaded POM is optional project context. It is not technical evidence and does not independently establish compatibility, breaking changes, or security findings.
- Documentation retrieval and assessment quality depend on the available corpus and retrieved evidence. The service may return an insufficient-evidence result when it cannot establish a defensible answer.
- No trained ML model is part of the active application.

## Documentation

- [AI service README](ai-service/README.md) — setup, configuration, API, analysis modules, RAG, local assessment, and POM context.
- [RAG architecture](docs/rag/architecture.md) — ingestion, hybrid retrieval, assessment flow, design decisions, and limitations.

## Security and local data

Do not commit secrets, `.env` files, local databases, generated vector stores, model files, or personal notes. Keep local configuration in ignored files and use `.env.example` files for safe configuration templates.
