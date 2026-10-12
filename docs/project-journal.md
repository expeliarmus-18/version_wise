# VersionWise Project Journal

## Snapshot

Date: 2026-10-12
Current phase: Day 1 - Architecture, prerequisites and repository foundation

## Approved decisions

- Frontend: React, JavaScript, Vite and CSS.
- Backend: Java 21, Spring Boot, Spring Security, JWT, Spring Data JPA and Maven.
- AI service: Python and FastAPI with the planned data-science libraries.
- PostgreSQL is owned by the Spring Boot application.
- ChromaDB provides persistent local vector storage.
- The repository is named VersionWise.
- Development is Windows-based and uses CMD.
- DevOps is deferred until after MVP stability.

## Verified environment

- Windows 11, build 26200.9457.
- Git 2.55.0.windows.2.
- Java 21.0.11 LTS.
- Maven 3.9.16.
- Node.js 24.18.0 and npm 11.16.0.
- Python 3.10.11 and pip 26.2.1.
- PostgreSQL client psql 18.6.
- JAVA_HOME is not set in the inspected CMD session.
- IntelliJ IDEA and VS Code are available, as confirmed by the developer.

## Pending verification

- PostgreSQL server installation, service status and database connectivity.
- Repository initialization and file creation.
- Frontend and Python framework compatibility when those phases begin.

## Architecture safeguards

- Rule-engine scores are heuristics, not failure probabilities.
- ML predicts supported historical failure categories, not arbitrary upgrade failure probabilities.
- Evidence must retain authentic provenance and URLs.
- Missing evidence and unsupported version formats remain visible.
- Secrets belong in environment variables.

## Implementation status

No application source code or framework projects have been created yet.
