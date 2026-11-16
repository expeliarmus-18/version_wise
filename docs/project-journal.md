# \# VersionWise Project Journal

#

# \## 1. Project Snapshot

#

# \- \*\*Project:\*\* VersionWise

# \- \*\*Date:\*\* 2026-10-12

# \- \*\*Current phase:\*\* Day 1 â€” Architecture, Prerequisites and Repository Foundation

# \- \*\*Repository path:\*\* `C:\\Users\\tanma\\Learning\\PROJECT\\VersionWise`

# \- \*\*Git branch:\*\* `master`

# \- \*\*Latest verified commit:\*\* `f5455ab` â€” `chore: establish VersionWise project foundation`

# \- \*\*Current implementation status:\*\* Project foundation established; application development has not started.

#

# \## 2. Approved Technology Decisions

#

# \### Frontend

# \- React

# \- JavaScript

# \- Vite

# \- CSS

#

# \### Main Backend

# \- Java 21

# \- Spring Boot

# \- Spring Web

# \- Spring Security

# \- JWT authentication

# \- Spring Data JPA

# \- Hibernate

# \- Maven

#

# \### AI Service

# \- Python

# \- FastAPI

# \- Pydantic

# \- Pandas

# \- NumPy

# \- Scikit-learn

#

# \### Data and Retrieval

# \- PostgreSQL is the primary application database, owned and managed by the Spring Boot backend.

# \- ChromaDB provides persistent local vector storage.

# \- The Python AI service does not own the application's PostgreSQL database.

#

# \### GenAI

# \- A hosted LLM API will be used.

# \- LangChain and embeddings may be used where they provide practical value.

#

# \### Development Environment

# \- Operating system: Windows 11

# \- Terminal: Windows Command Prompt (CMD) only

# \- IDEs: IntelliJ IDEA and VS Code

# \- Repository name: `VersionWise`

#

# \### Delivery Strategy

# \- Build the MVP incrementally.

# \- Verify prerequisites before relying on them.

# \- Keep implementation decisions and verification results documented.

# \- Defer DevOps work until the MVP is stable, starting on Day 16 or later.

#

# \## 3. Verified Environment Inventory

#

# The following versions and environment details were observed during Day 1.

#

# | Component | Verified result |

# |---|---|

# | Windows | Windows 11, build 26200.9457 |

# | Git | 2.55.0.windows.2 |

# | Java | 21.0.11 LTS |

# | Maven | 3.9.16 |

# | Node.js | 24.18.0 |

# | npm | 11.16.0 |

# | Python | 3.10.11 |

# | pip | 26.2.1 |

# | PostgreSQL client | `psql` 18.6 |

# | PostgreSQL server | 18.6; version query succeeded |

# | PostgreSQL Windows service | `postgresql-x64-18` |

# | Java environment variable | `JAVA\_HOME` was unset in the inspected CMD session |

# | IDEs | IntelliJ IDEA and VS Code are available, as confirmed by the developer |

#

# \### PostgreSQL Verification

#

# \- The PostgreSQL server executable exists at `C:\\Program Files\\PostgreSQL\\18\\bin\\postgres.exe`.

# \- The Windows service `postgresql-x64-18` was confirmed to be running.

# \- A local connection using `psql -U postgres -h localhost -p 5432 -d postgres -c "SELECT version();"` succeeded.

# \- The query returned PostgreSQL 18.6 on 64-bit Windows.

# \- This verifies local database connectivity using the `postgres` account. Application-specific database creation, credentials, and Spring Boot connectivity have not yet been configured or verified.

#

# \## 4. Repository Foundation

#

# \### Repository Structure

#

# The following initial structure was created:

#

# ```text

# VersionWise/

# â”œâ”€â”€ .gitignore

# â”œâ”€â”€ README.md

# â”œâ”€â”€ frontend/

# â”œâ”€â”€ backend/

# â”œâ”€â”€ ai-service/

# â”œâ”€â”€ samples/

# â””â”€â”€ docs/

# &#x20;   â””â”€â”€ project-journal.md

# ```

#

# The `frontend`, `backend`, `ai-service`, and `samples` directories are currently placeholders for future implementation.

#

# \### Initial Files

#

# \- `.gitignore`: excludes secrets, local environment files, Java build output, Node.js dependencies, Python caches and virtual environments, IDE files, local databases, vector-store data, and logs.

# \- `README.md`: records the project purpose, planned architecture, development phases, and current status.

# \- `docs/project-journal.md`: records project decisions, environment verification, architecture safeguards, and implementation progress.

#

# \### Git Status

#

# \- Repository initialization: completed.

# \- Initial commit: completed.

# \- Commit: `f5455ab`.

# \- Commit message: `chore: establish VersionWise project foundation`.

# \- The working tree was verified clean immediately after the initial commit.

# \- The journal's latest documentation update and any subsequent commit must be recorded after their completion.

#

# \## 5. Architecture Safeguards

#

# The implementation must follow these principles:

#

# 1\. \*\*Explainable rule-engine results:\*\* Rule-engine scores are heuristics, not calibrated probabilities of upgrade failure.

# 2\. \*\*Responsible ML predictions:\*\* Machine learning should predict supported failure categories based on historical data rather than claim arbitrary upgrade-failure probabilities.

# 3\. \*\*Authentic evidence:\*\* Documentation evidence must preserve genuine provenance and source URLs.

# 4\. \*\*Transparent uncertainty:\*\* Missing evidence, unsupported version formats, and insufficient data must remain visible rather than being silently treated as safe.

# 5\. \*\*Secret management:\*\* Credentials and API keys must be kept in environment variables or suitable local configuration and must never be committed to Git.

# 6\. \*\*Clear service ownership:\*\* Spring Boot owns application persistence in PostgreSQL; the Python service provides AI-related functionality.

# 7\. \*\*Incremental verification:\*\* Each phase must verify its output before later phases depend on it.

# 8\. \*\*Non-destructive changes:\*\* Avoid overwriting existing work, deleting project data, or changing system configuration without a clear reason.

#

# \## 6. Pending Verification and Future Work

#

# \### Day 1 Documentation Closeout

# \- \[ ] Replace this journal with the finalized Day 1 record.

# \- \[ ] Commit the updated journal.

# \- \[ ] Verify the latest commit and clean Git working tree.

# \- \[ ] Record the final Day 1 handoff in the Master Chat.

#

# \### Day 2 â€” Backend Foundation

# \- \[ ] Review the existing environment and repository without repeating unnecessary checks.

# \- \[ ] Establish the Spring Boot backend foundation.

# \- \[ ] Configure PostgreSQL application connectivity using appropriate local configuration and environment variables.

# \- \[ ] Verify the backend build and database connection.

# \- \[ ] Record commands, results, decisions, and blockers.

#

# \### Later Development Phases

# \- \[ ] Verify frontend framework compatibility when frontend setup begins.

# \- \[ ] Verify Python and AI-library compatibility when the AI service is established.

# \- \[ ] Create and verify application-specific PostgreSQL configuration.

# \- \[ ] Implement backend APIs, persistence, the AI service, the analysis pipeline, and frontend integration incrementally.

# \- \[ ] Introduce DevOps only after MVP stability, starting Day 16 or later.

#

# \## 7. Implementation Status

#

# \*\*Completed during Day 1\*\*

# \- Inspected the Windows development environment and recorded installed tool versions.

# \- Confirmed Git, Java, Maven, Node.js, npm, Python, pip, and the PostgreSQL client are available.

# \- Confirmed the PostgreSQL 18 service is running.

# \- Verified a successful local PostgreSQL connection and version query.

# \- Created the initial repository directory structure.

# \- Created `.gitignore`, `README.md`, and this project journal.

# \- Initialized Git and created the initial foundation commit.

#

# \*\*Not yet implemented\*\*

# \- Spring Boot application and backend APIs.

# \- Application-specific PostgreSQL database, schema, and credentials.

# \- React/Vite frontend application.

# \- Python/FastAPI AI service.

# \- ChromaDB integration.

# \- LLM integration, dependency analysis, and ML pipeline.

# \- Authentication and authorization.

# \- Automated tests and end-to-end integration.

#

# \*\*Current conclusion:\*\* The Day 1 environment inspection and repository foundation are complete. PostgreSQL local connectivity is verified. The journal closeout commit remains pending until this finalized version is saved and committed. Application development should begin with the Day 2 backend foundation, without assuming application-level database integration already exists.




## Day 2 â€” Spring Boot Foundation and PostgreSQL Connectivity

**Date:** 2026-10-16
**Status:** IN PROGRESS â€” final documentation and Git review pending
**Repository:** `C:\Users\tanma\Learning\PROJECT\VersionWise`

### Implemented

- Generated the backend using IntelliJ IDEA and Spring Initializr.
- Configured Java 21 and Spring Boot 3.5.16.
- Added Spring Web, Spring Data JPA, PostgreSQL JDBC, and Spring Boot Test dependencies.
- Configured `application.yml` to read database settings from environment variables.
- Added a health endpoint at `GET /api/health` (confirm the response separately if not already observed).

### Verification evidence

- Application startup logs show Spring Boot 3.5.16 running on Java 21.0.11.
- Embedded Tomcat started on port 8080.
- HikariCP successfully obtained a PostgreSQL connection and completed pool startup.
- Hibernate initialized the JPA EntityManagerFactory.
- PostgreSQL server version reported by Hibernate: 18.6.
- Maven verification result: `BUILD SUCCESS`.

### Security and database notes

- Database username and password were configured through IntelliJ Run/Debug environment variables; no password is recorded here.
- Confirm that local credentials and configuration are not committed.
- The database name and application account privileges should be confirmed before claiming least-privilege configuration.
- No application entities or schema migrations were implemented. Hibernate schema generation is configured as `none`.

### Remaining closeout

- Verify the HTTP health response.
- Review changed files and Git status.
- Confirm secrets and generated build outputs are not staged.
- Update the root README with concise backend setup instructions if needed.

### Next step

After closeout, begin Day 3 according to the Master Chat plan. Preserve the existing architecture and avoid adding authentication or unrelated features before the next planned milestone.


## Day 3 â€” Project Entities, Persistence and CRUD API

**Date:** 2026-10-23
**Status:** Completed â€” implementation, verification and Git commit completed
**Commit:** `4fdac5f feat(backend): implement project CRUD API`

### Implemented

- Added `User` and `Project` JPA entities with UUID identifiers.
- Added `UserRepository` and `ProjectRepository`.
- Added project request and response DTOs.
- Implemented `ProjectService` for project creation, listing, retrieval, updating and deletion.
- Implemented `ProjectController` with REST endpoints under `/api/projects`.
- Added request validation using Spring Boot validation.
- Configured Hibernate schema updates for local development.
- Updated the root README with API documentation and development-only limitations.

### API endpoints

- `GET /api/health` â€” health check.
- `POST /api/projects` â€” create a project.
- `GET /api/projects` â€” list projects for the development user.
- `GET /api/projects/{id}` â€” retrieve a project.
- `PUT /api/projects/{id}` â€” update a project.
- `DELETE /api/projects/{id}` â€” delete a project.

### Verification

- `mvnw.cmd clean compile` completed successfully.
- Spring Boot started successfully and connected to PostgreSQL 18.6.
- Manual Postman checks reportedly passed for health, project CRUD, validation errors, and retrieval of a deleted project.
- `mvnw.cmd test` completed successfully: 1 test run, 0 failures, 0 errors, 0 skipped.
- Database checks were reported as successful.
- `git diff --check` reported no whitespace errors.
- Git working tree was verified clean after commit `4fdac5f`.

### Design decisions and limitations

- A fixed development user, `dev@versionwise.local`, is used to associate projects with an owner.
- Registration, authentication, and secure per-user authorization have not been implemented.
- Hibernate `ddl-auto: update` is for local development; production schema management needs a migration strategy.
- Automated tests currently do not provide comprehensive coverage of individual project CRUD operations.
- No database password or other secret should be recorded in this journal.

### Next steps

- Update the project snapshot and pending-work checklist to reflect the completed backend CRUD milestone.
- Continue with the next milestone specified by the VersionWise Master Chat plan.
- Preserve the existing architecture and database data; avoid unrelated changes.



### Day 3 Completion Addendum â€” Authentication and Authorization

**Status:** Implementation and verification completed
**Date:** 2026-10-26

#### Implemented
- Added Spring Security and OAuth2 Resource Server JWT support.
- Added password hashing with BCrypt.
- Added registration and login endpoints.
- Added signed JWT access tokens with a one-hour expiry.
- Configured stateless authentication.
- Kept the health endpoint and authentication endpoints public.
- Protected project endpoints with Bearer-token authentication.
- Removed the fixed development-user identity from the backend.
- Scoped project operations to the authenticated user's ID.
- Added integration tests for authentication, validation, token rejection, and project ownership.

#### Verification
- Command: `mvnw.cmd clean verify`
- Result: `BUILD SUCCESS`
- Tests run: 8
- Failures: 0
- Errors: 0
- Skipped: 0
- Manual Postman checks: reported successful for health, registration, login, project CRUD, and cross-user access restrictions.

#### Configuration and safety
- JWT signing secret is supplied through the `JWT_SECRET` environment variable.
- Database connection settings are supplied through environment variables.
- The development database was used during integration tests and contained no data that needed to be preserved.
- No Git commit was created as part of this work.

#### Next milestone
Continue with the next milestone in the VersionWise Master Chat project plan.



## Day 4 â€” Frontend and Authentication Integration

**Status:** Core implementation and manual integration checks completed.

### Work completed

- Set up the React + Vite frontend in `frontend/`.
- Implemented a custom VersionWise sign-in and account-registration interface.
- Added a frontend API client for communicating with the Spring Boot backend.
- Integrated login and registration with the existing authentication endpoints.
- Added JWT-based authenticated requests using the Bearer authorization header.
- Added frontend session handling, authenticated workspace UI, and logout behavior.
- Configured backend CORS to allow the local Vite development origin at `http://localhost:5173`.
- Added a protected-projects API check to verify authenticated frontend requests.

### Authentication and authorization

The backend uses stateless JWT authentication. Passwords are handled by the backend authentication service, and the frontend uses the returned access token for protected API requests. Spring Security protects project endpoints, while project authorization restricts access according to the authenticated user.

### Verification performed

- Confirmed the custom VersionWise interface renders in the browser.
- Frontend production build completed successfully.
- Frontend lint completed with zero warnings and errors.
- Backend compilation completed successfully using `mvnw.cmd -DskipTests compile`.
- Manually tested registration and login using multiple users.
- Tested invalid login credentials and confirmed they were rejected.
- Confirmed the frontend could call the protected projects endpoint with an authenticated request.
- Checked that different users received the expected user-specific project data.

### Notes and remaining work

- The backend compile command skipped tests; it was a compilation check, not the full backend test suite.
- Manual integration checks passed. Complete the planned final verification after the remaining Day 4 documentation and repository cleanup.
- The frontend currently targets the local development backend by default. Production deployment configuration and production-grade token-storage/security review remain future work.
- Temporary frontend source-bundle files should not be committed; the maintained application source belongs in `frontend/`.

## Day 5 â€” Authenticated Project Dashboard and CRUD

### Objective
Connect the React frontend to the existing authenticated project API and replace the temporary API-check dashboard with functional project management.

### Implementation
- Preserved the existing frontend registration, login, session, and logout flow.
- Integrated the dashboard with the protected `/api/projects` endpoints using the existing API client and JWT Bearer token.
- Implemented project listing, creation, detail viewing, editing, and deletion.
- Added project form validation aligned with backend constraints: name is required and limited to 100 characters; description is optional and limited to 1,000 characters.
- Added loading, empty, success, and error states, along with delete confirmation and responsive project-management UI.
- Used the existing backend authorization and ownership rules; no new authentication mechanism was introduced.
- Kept dependency analysis outside the Day 5 scope.

### Verification
- Manually verified all eight dashboard workflow checks:
  1. Sign in and load projects.
  2. Create a project.
  3. View project details.
  4. Edit a project.
  5. Delete a project after confirmation.
  6. Refresh and confirm the deleted project remains deleted.
  7. Sign out.
  8. Sign back in and confirm session and project-list behavior.
- All eight checks passed in the user's environment.
- `git diff --check` completed without reporting whitespace errors. Git displayed LF-to-CRLF line-ending warnings.
- Frontend lint/build results were not included in the recorded verification output.

### Outcome
The authenticated frontend supports project CRUD through the existing backend API. Day 5 is ready for documentation review and version control.

# Day 6 â€” Python FastAPI Foundation and Maven Dependency Parsing

## Objective

Establish the independent Python analysis service and implement a reusable Maven POM dependency parser.

## Implementation

- Established a Python 3.10.11 virtual environment at `ai-service/.versionwise`.
- Configured FastAPI, Pydantic and Uvicorn.
- Implemented `GET /health`.
- Implemented a reusable Maven POM parser using secure XML parsing.
- Extracted project and parent coordinates.
- Extracted direct dependencies and dependency-management entries separately.
- Implemented local Maven property substitution, including nested properties.
- Preserved unresolved expressions and reported parsing warnings.
- Implemented structured Pydantic response models.
- Exposed the parser through `POST /api/v1/parse-pom`.
- Added automated parser and API tests.

## Verification

Actual pytest output:

- 21 tests collected.
- 21 tests passed.
- 0 failures.
- 1 Starlette deprecation warning.
- Execution time: 3.92 seconds.

The health endpoint returned HTTP 200.

The POM parsing endpoint returned structured dependency information through the FastAPI API.

## Limitations

The parser is not a complete Maven effective-POM resolver.

It does not resolve parent inheritance, imported BOMs, transitive dependencies, activated profiles, Maven settings or environment-specific properties.
The service is intended for controlled internal development use and is not configured for direct public exposure.
Day 7 â€” Deterministic Dependency-Upgrade Risk Engine
Status: Implementation and verification completed.
Objective
Build a deterministic, explainable baseline for evaluating Maven dependency upgrades. The engine compares a current dependency version with a proposed target version, applies explicit risk rules, and returns a structured analysis through the Python FastAPI service.
Implementation
- Added a bounded Maven version comparison utility in ai-service/app/analysis/version_comparator.py.
- Added deterministic risk scoring rules in ai-service/app/analysis/rule_engine.py.
- Added structured risk-analysis models in ai-service/app/models/risk.py.
- Added the risk-analysis endpoint in ai-service/app/api/routes/analysis.py.
- Registered the analysis router in ai-service/app/main.py.
- Added tests for version comparison, rule scoring, and the analysis API.
- Updated ai-service/pytest.ini with pythonpath = . so pytest can import the app package from the service root.
The analysis endpoint is:

POST /api/v1/analyze-upgrade

The response includes dependency coordinates, current and target versions, comparison status, risk score and category, evaluated factors, warnings, recommendations, and scoreIsProbability: false.
Risk-scoring behavior
The engine uses explicit rules and returns the contribution and explanation for evaluated factors. The score is a deterministic heuristic; it is not a trained ML prediction and is not a probability of failure.
The version comparator is a bounded implementation and is not a complete implementation of Apache Maven's ComparableVersion. Unsupported or ambiguous version formats produce an unknown comparison instead of asserting an unreliable version order.
Verification
Automated tests
The final local pytest run reported:
- 39 tests collected.
- 39 passed.
- 0 failures.
- 0 errors.
- 1 Starlette/httpx deprecation warning.
- Runtime: 0.60 seconds.
Test files included:
- tests/test_analysis_api.py â€” 3 passed.
- tests/test_maven_parser.py â€” 17 passed.
- tests/test_parser_api.py â€” 4 passed.
- tests/test_rule_engine.py â€” 8 passed.
- tests/test_version_comparator.py â€” 7 passed.
Live HTTP checks
- Major upgrade 1.2.3 â†’ 2.0.0: HTTP 200, comparison upgrade, score 40, category HIGH, and the MAJOR_CHANGE factor was returned.
- Missing targetVersion: HTTP 422 with a validation error.
- Unsupported version 1.0.0-custom â†’ 1.1.0: HTTP 200 with comparison unknown and a structured uncertainty factor.
- Existing health and Maven parser APIs were reported as working after the analysis router was registered.
- git diff --check completed without reporting whitespace errors.
Limitations and follow-up
- Maven parsing remains a partial POM parser, not a full effective-POM resolver; Day 6 limitations still apply.
- Version comparison supports a bounded set of formats. Maven's full version ordering semantics are not implemented.
- Risk scores are rule-based heuristics and have not been trained or calibrated against a historical upgrade-outcome dataset.
- Historical data collection, label definition, ML evaluation, retrieval-augmented evidence, and LLM-generated explanations remain future work.
- The Starlette/httpx deprecation warning did not fail the tests and is deferred for dependency compatibility cleanup.
Outcome
The Python service now has a tested deterministic dependency-upgrade risk-analysis endpoint alongside the existing Maven parser API. Day 7 implementation and local verification are complete. No Git commit or push was made as part of this milestone.
Next milestone â€” Day 8
Research historical dependency-upgrade datasets and define the data strategy for future ML work. Investigate available sources, licensing and usage constraints, label definitions, candidate features, dataset quality, and an evaluation approach. Do not begin model training until the dataset and target outcome are sufficiently defined.

## Day 8 â€” ML Dataset and Feasibility Research

**Status: RESEARCH COMPLETED; DOCUMENTATION UPDATE IN PROGRESS**

### Objective

Research historical dependency-upgrade datasets and determine whether VersionWise can reasonably proceed toward ML-based dependency-upgrade risk analysis.

### Completed Research

- Reviewed BUMP as a source of reproducible breaking dependency updates.
- Identified its usefulness for failure-category research and its limitation as a failure-focused dataset.
- Established that a general risk model needs representative successful-upgrade evidence as well as failure records.
- Defined candidate labels, label-evidence considerations, feature candidates, and a normalized dataset schema.
- Identified risks of label uncertainty, causal overclaiming, and data leakage.
- Proposed time-aware and project-aware evaluation, including comparison with the Day 7 deterministic baseline.
- Planned training around the development laptop: Ryzen 7 4800H, 16 GB RAM, RTX 3050 4 GB VRAM, and approximately 200 GB free SSD.
- Decided against downloading the complete BUMP Docker archive or beginning large-model training.

### Day 8 Decision

No model training is performed on Day 8.

Day 9 training will proceed only if the selected dataset has sufficient quality, provenance, and label evidence for the intended prediction task. Otherwise, data collection and labeling will take priority.

### Documentation

Research details are maintained in:

`docs/ml/dataset-feasibility.md`


# Day 9 â€” ML Dataset Preparation Foundation

**Status:** IMPLEMENTATION COMPLETED â€” REAL DATASET AND MODEL TRAINING PENDING

## Objective

Build the initial dataset preparation foundation for evaluating machine-learning-assisted dependency-upgrade analysis in VersionWise, based on the Day 8 feasibility research.

## Work Completed

### Dataset validation and normalization
- Added an ML dataset module.
- Defined supported dependency-upgrade outcome labels.
- Implemented record normalization and required-field validation.
- Preserved label evidence and source metadata.
- Added label confidence validation.
- Implemented duplicate upgrade record handling.
- Added dataset summaries and label counts.
- Added CSV loading.

### Group-aware dataset splitting
- Implemented train, validation, and test partitions.
- Added deterministic splitting with a configurable random seed.
- Ensured records sharing a split group remain in the same partition.
- Added validation for split ratios and insufficient group counts.

### Dataset preparation workflow
- Added a dataset preparation CLI.
- Added output generation for prepared datasets and a JSON summary.
- Documented the preparation workflow and current ML status.

## Testing

- Focused ML tests: **13 passed**
- Full Python test suite: **52 passed, 0 failed**
- One Starlette deprecation warning related to `httpx` was reported; it did not affect test results.

The preparation CLI has not yet been independently verified against a real source dataset.

## ML Feasibility Status

The implementation establishes a foundation for future ML experiments. A suitable real, labeled dataset has not yet been acquired, and no model has been trained.

Remaining work includes:
- Acquiring a suitable historical dataset.
- Verifying labels, provenance, and licensing.
- Assessing dataset size and class distribution.
- Selecting an evaluation split appropriate to the intended generalization goal.
- Training and evaluating a baseline model.
- Comparing model performance against the existing deterministic risk engine.

No model metrics or calibrated failure-probability claims are made.

## Outcome

VersionWise retains its deterministic dependency-upgrade risk engine as the current analysis foundation. ML remains an experimental future capability.

Day 9 is complete from an implementation-foundation perspective. Real-data acquisition and model training remain future work.

## Next

Day 10 â€” Research and document official evidence sources for dependency-upgrade analysis, including reliability, access, limitations, and integration feasibility.
.


## Day 10 â€” AI Service Audit, ML Removal and RAG/LLM Readiness

**Date:** 2026-11-13
**Status:** Implementation prepared; final verification in the developer's Windows environment and Git review remain pending.
**Git branch at start of Day 10 work:** `master`
**Working tree at start of Day 10 work:** clean (`git status --short` returned no entries).

### Architecture decision

The active VersionWise implementation will not use machine learning. Days 8â€“9 ML feasibility research and dataset-preparation work are retained as historical project records, but the ML implementation is removed from the active Python service. No model training, prediction endpoint or ML runtime dependency is part of the product plan.

The target analysis flow is:

`Maven POM â†’ structured dependency declarations â†’ deterministic analysis â†’ RAG evidence retrieval â†’ LLM assessment â†’ structured upgrade report`

The Python service remains independent from Spring Boot during this milestone. No cross-service calls, authentication integration, database integration or frontend changes are included.

### Files and components reviewed

The supplied `ai-service.zip` was inspected, including:

- FastAPI application entry point and health, parser and analysis routes.
- Maven POM parser, version comparator and deterministic rule engine.
- Pydantic dependency and risk request/response models.
- Python requirements and pytest configuration.
- Parser, API, comparator and rule-engine tests.
- ML dataset normalization, group splitting, preparation CLI and ML-only tests.
- Stale Day 7 patch instructions and generated Python bytecode included in the archive.

The supplied root README and project journal were also reviewed. The repository owner separately confirmed that the current branch is `master`, the working tree is clean, and the root `.gitignore` exists. The `.gitignore` contents were not supplied for inspection and were not changed.

### Cleanup prepared

Removed from the cleaned AI-service package:

- `app/ml/dataset.py`
- `app/ml/split.py`
- `app/ml/prepare.py`
- `app/ml/__init__.py`
- `tests/ml/test_dataset.py`
- `tests/ml/test_split.py`
- Generated `__pycache__` directories and `.pyc`/`.pyo` files found in the supplied ZIP.
- Stale `PATCH-INSTRUCTIONS.txt`.

Added `defusedxml` to `requirements.txt` because the Maven parser imports it for secure XML parsing but the supplied dependency file did not declare it.

Retained the Maven parser, version comparator, deterministic rule engine, FastAPI routes, existing Pydantic models, pytest configuration and all non-ML tests.

### RAG/LLM boundary preparation

Added reserved package boundaries under `app/` for `core`, `parser`, `rag` and `llm`. These are architectural placeholders only; no RAG ingestion, vector database, embeddings, retrieval, LLM client or prompt execution is implemented.

The existing parser remains at `app/analysis/maven_parser.py` to avoid a disruptive move of working code.

Added `app/models/assessment.py` as a future report data contract. It defines:

- `RECOMMENDED`, `NOT_RECOMMENDED` and `INSUFFICIENT_EVIDENCE` assessment statuses.
- Structured compatibility, breaking-change, migration and security finding groups.
- Evidence source title, source URI, excerpt and optional retrieval timestamp.
- Limitations/uncertainty fields.

This model is not connected to an API route or LLM. It does not establish that evidence has been retrieved or validated.

### Documentation prepared

- Replaced the AI-service README with setup instructions, endpoint documentation, current limitations and future boundaries.
- Prepared an updated root README describing the current stack, implemented capabilities, removed ML direction, parser/risk limitations and Days 11â€“15 roadmap.
- Preserved the historical Days 8â€“9 journal entries and appended this Day 10 record.

### Verification performed during preparation

The supplied archive initially had 52 tests, including 13 ML-specific tests. After removing ML tests and adding three tests for the future assessment contract, the consolidated test run reported:

- **42 passed**
- **0 failed**
- **0 errors**

The tests were run in the available inspection Python environment, not in the developer's Windows `.versionwise` environment. This is not yet the final Windows verification. The assessment-contract test initially exposed that Pydantic `min_length` accepts whitespace-only strings; a non-whitespace summary validator was added and the final test run passed.

The test run emitted no pytest warning in its final output. No claim is made here that a clean Windows dependency installation, Uvicorn process startup or manual HTTP checks have been performed.

### Remaining verification and closeout

- [ ] Apply/review the prepared AI-service changes in the actual repository.
- [ ] Install requirements in the developer's Windows `.versionwise` environment and verify `defusedxml` is installed from the declared requirements.
- [ ] Run `python -m compileall app`.
- [ ] Run the complete `pytest` suite from `ai-service`.
- [ ] Start Uvicorn and manually verify `/health`, `/api/v1/parse-pom` and `/api/v1/analyze-upgrade`.
- [ ] Review the complete Git diff, including root README and this journal.
- [ ] Confirm no ML imports or active ML references remain in the AI service.
- [ ] Confirm no Spring Boot integration was introduced.
- [ ] Commit/push only after explicit developer approval.

**Day 10 outcome:** The cleaned implementation and documentation are prepared for review. The available test run passes, but Day 10 must not be marked fully closed until the developer performs the Windows-environment verification and reviews the repository diff.


## Day 12 — LangChain RAG Documentation Ingestion Foundation

**Status:** Implementation, verification and documentation completed; final repository review and Git closeout pending.

### Objective

Implement the first RAG milestone for VersionWise: a repeatable documentation-ingestion pipeline that retrieves approved technical documentation, extracts and chunks its content, generates local embeddings, and persists the resulting vectors in ChromaDB.

### Architecture decisions

- Use LangChain for document representation, text splitting, embeddings integration and vector-store integration.
- Use HTTPX for documentation retrieval.
- Use BeautifulSoup for HTML content extraction.
- Use `BAAI/bge-small-en-v1.5` as the local embedding model.
- Run embeddings locally on CPU; no paid embedding API is required.
- Use persistent ChromaDB storage.
- Preserve source provenance and document metadata through the ingestion pipeline.
- Use content hashes and chunk identifiers to support repeatable ingestion and deduplication.
- Keep the RAG implementation under `ai-service/app/rag/`.
- Preserve the existing Maven parser and deterministic analysis implementation.

### Approved documentation sources

The initial source registry contains exactly three sources:

1. Apache Maven POM Reference
   `https://maven.apache.org/pom.html`

2. Spring Boot 3.0 Migration Guide
   `https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide`

3. Hibernate ORM 6.0 Migration Guide
   `https://docs.hibernate.org/orm/6.0/migration-guide/migration-guide/`

No additional documentation sources were introduced during this milestone.

### Implementation

Added the following modules:

- `app/rag/sources.py` — approved source registry and source metadata.
- `app/rag/loader.py` — HTTP retrieval, HTML extraction and LangChain document creation.
- `app/rag/chunker.py` — heading-aware and recursive text splitting, section metadata and content hashing.
- `app/rag/embeddings.py` — cached local Hugging Face embedding configuration.
- `app/rag/vector_store.py` — persistent ChromaDB collection, deduplication, obsolete-chunk cleanup and semantic similarity search.
- `app/rag/ingest.py` — ingestion orchestration and JSON execution report.

### RAG configuration

- Embedding model: `BAAI/bge-small-en-v1.5`
- Execution device: CPU
- Vector store: ChromaDB
- Collection name: `versionwise_documentation`
- Target chunk size: 1,200 characters
- Chunk overlap: 150 characters
- Persistent storage: `ai-service/data/chroma/`
- Local vector-store data is excluded from Git.

### Dependencies

Added and installed the LangChain, ChromaDB, embedding and HTML-extraction dependencies.

The principal pinned versions are:

- `langchain-core==0.3.86`
- `langchain-text-splitters==0.3.11`
- `langchain-chroma==0.2.6`
- `langchain-huggingface==0.3.1`
- `chromadb==1.5.9`
- `sentence-transformers==5.1.2`
- `beautifulsoup4==4.15.0`

HTTPX remains declared as an HTTP dependency.

### Verification

**Initial ingestion**

- Sources attempted: 3
- Sources successfully ingested: 3
- Sources failed: 0
- Maven chunks: 124
- Spring Boot chunks: 78
- Hibernate chunks: 78
- Total chunks created: 280
- Chunks added to storage: 280
- Initial collection count: 280

**Repeat ingestion**

- Sources successfully ingested: 3
- Chunks received: 280
- Unique chunks: 280
- Chunks added or updated: 0
- Unchanged chunks skipped: 280
- Obsolete chunks removed: 0
- Collection count remained: 280

This confirms that a repeated ingestion of unchanged source content did not create duplicate stored chunks.

**Semantic retrieval**

Executed a representative query:

`What breaking changes should developers consider when migrating to Spring Boot 3?`

The top five results were retrieved from the Spring Boot 3.0 Migration Guide and included relevant sections such as dependency review, migration, configuration properties and Spring Security changes.

This verifies a representative semantic retrieval path; it is not a comprehensive retrieval-quality evaluation.

**Environment and regression checks**

- `pip check`: no broken requirements.
- `python -m compileall -q app`: successful.
- Complete existing pytest suite: **42 passed**.
- `git diff --check`: no whitespace errors; Git displayed an LF-to-CRLF line-ending warning.

The 42 tests cover the existing application functionality and assessment contract. They are not 42 RAG-specific automated tests.

### Scope boundaries

Completed in Day 12:

- Approved documentation registry.
- Document retrieval and extraction.
- Section-aware chunking.
- Local embedding configuration.
- Persistent ChromaDB storage.
- Repeatable ingestion and deduplication.
- Initial semantic similarity search.

Explicitly deferred:

- BM25 keyword retrieval.
- Hybrid retrieval and reciprocal-rank fusion.
- LLM integration and prompt execution.
- Structured LLM assessment generation.
- Spring Boot integration.
- Frontend integration.

These remain part of the subsequent planned milestones.

### Files changed

Modified:

- `ai-service/requirements.txt`
- `ai-service/.gitignore`

Added:

- `ai-service/app/rag/sources.py`
- `ai-service/app/rag/loader.py`
- `ai-service/app/rag/chunker.py`
- `ai-service/app/rag/embeddings.py`
- `ai-service/app/rag/vector_store.py`
- `ai-service/app/rag/ingest.py`

No existing parser, deterministic analysis, API route or assessment-model implementation was intentionally changed.
Documentation updated or added:

- `ai-service/README.md`
- `docs/project-journal.md`
- `docs/rag/architecture.md`

### Outcome

Day 12 establishes a working local RAG ingestion and vector-storage foundation using the three approved documentation sources.

The ingestion pipeline successfully processed all three sources, persisted 280 chunks, skipped all 280 unchanged chunks on repeat ingestion, and returned relevant results for a representative semantic query.

Existing application regression tests passed.

No Git commit or push was made as part of this milestone. Repository review and explicit developer approval are required before committing.

### Next milestone

Day 13 — Implement hybrid retrieval by combining vector similarity retrieval with keyword retrieval, followed by reciprocal-rank fusion.

Preserve the Day 12 ingestion foundation and existing application functionality.


## Day 13 — Hybrid Documentation Retrieval

### Objective

Implement hybrid retrieval by combining the existing ChromaDB dense semantic retrieval with BM25 keyword retrieval and Reciprocal Rank Fusion.

Preserve the Day 12 ingestion pipeline, approved source registry and existing application functionality.

### Implementation

Added:

- `ai-service/app/rag/bm25_retriever.py`
- `ai-service/app/rag/fusion.py`
- `ai-service/app/rag/hybrid_search.py`
- `ai-service/tests/test_rag_retrieval.py`

Modified:

- `ai-service/requirements.txt`

Added the pinned dependency:

- `rank-bm25==0.2.2`

BM25 indexes the existing persisted ChromaDB documentation chunks. Technical identifiers are preserved as complete tokens and split into searchable components.

The index is cached in memory. An explicit refresh function is available for rebuilding it after ingestion.

Dense and keyword rankings are combined using Reciprocal Rank Fusion.

Configuration:

- RRF constant: 60
- Final results: 5
- Candidates per retriever: 10

The fused results retain original document content and metadata, along with RRF score and individual retrieval ranks.

### Corpus verification

The persisted `versionwise_documentation` collection was inspected.

- Apache Maven POM Reference: 124 chunks.
- Spring Boot 3.0 Migration Guide: 78 chunks.
- Hibernate ORM 6.0 Migration Guide: 78 chunks.
- Total: 280 chunks.

All 280 chunks had content and stable chunk identifiers.

### Qualitative evaluation

Five representative queries were evaluated against the actual persisted corpus.

The queries covered:

1. Spring Boot 3 migration breaking changes.
2. Hibernate ORM 6 SQL and type-mapping changes.
3. Maven dependency management and exclusions.
4. Jakarta migration from javax APIs.
5. Exact Spring Boot and Jakarta technical identifiers.

The evaluation showed that dense and keyword retrieval can provide complementary results.

Maven exclusion and Jakarta migration queries showed useful combined evidence. However, the Hibernate SQL and type-mapping query exposed a ranking limitation: some less relevant migration sections appeared above the strongest dense result.

Candidate-pool sizes of 5, 10 and 20 were inspected for selected queries. A larger candidate pool did not consistently improve the final ranking.

The defaults remain RRF k=60 and 10 candidates per retriever. No claim is made that these values are optimal.

This was a qualitative evaluation, not a quantitative retrieval benchmark. No precision, recall, MRR or NDCG values are claimed.

### Automated verification

- New retrieval tests: 21 passed.
- Existing application regression tests: 42 passed.
- Complete test suite: **63 passed**.

### Limitations and scope boundaries

Completed:

- Existing Day 12 ingestion and persistent vector-storage foundation preserved.
- BM25 keyword retrieval.
- Technical identifier-aware tokenization.
- Reciprocal Rank Fusion.
- Stable chunk-ID deduplication.
- Retrieval metadata preservation.
- Hybrid retrieval orchestration.
- Retrieval unit tests.
- Qualitative evaluation against the persisted corpus.

Not implemented:

- LLM integration.
- Prompt execution.
- LLM-generated assessments.
- Reranking.
- Agent workflows.
- Backend or frontend integration.
- Quantitative retrieval benchmarks.

The BM25 index is cached. If ingestion modifies the collection within the same running process, the index must be refreshed.

### Files changed

Added:

- `ai-service/app/rag/bm25_retriever.py`
- `ai-service/app/rag/fusion.py`
- `ai-service/app/rag/hybrid_search.py`
- `ai-service/tests/test_rag_retrieval.py`

Modified:

- `ai-service/requirements.txt`
- `ai-service/README.md`
- `docs/rag/architecture.md`
- `docs/project-journal.md`

### Outcome

Day 13 implements the hybrid retrieval foundation using the existing 280-chunk documentation corpus.

The implementation combines semantic and keyword retrieval through Reciprocal Rank Fusion, preserves evidence metadata and passes the complete 63-test suite.

The evaluation identifies both complementary retrieval behavior and ranking limitations. Hybrid retrieval is implemented, but its superiority over dense-only retrieval has not been established quantitatively.

No Git commit or push has been made. Repository review and explicit approval are required before committing.

### Next milestone

Continue with the finalized Day 14–16 schedule. Preserve the completed Day 12 ingestion and Day 13 hybrid retrieval foundations.
