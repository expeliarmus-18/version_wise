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