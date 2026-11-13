# VersionWise AI Service

Independent FastAPI service for Maven POM declaration parsing and deterministic dependency-upgrade analysis.

## Requirements

- Python 3.10+
- Dependencies from `requirements.txt`

## Windows CMD setup

From the repository root:

```bat
cd ai-service
py -3.10 -m venv .versionwise
.versionwise\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```bat
python -m uvicorn app.main:app --reload
```

- Health: `GET http://127.0.0.1:8000/health`
- POM parser: `POST http://127.0.0.1:8000/api/v1/parse-pom`
- Upgrade analysis: `POST http://127.0.0.1:8000/api/v1/analyze-upgrade`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Tests

```bat
pytest
```

## Current modules

- `app/analysis/maven_parser.py`: secure XML parsing and local Maven property substitution.
- `app/analysis/version_comparator.py`: bounded conservative version ordering.
- `app/analysis/rule_engine.py`: deterministic heuristic risk findings.
- `app/api/routes/`: health, parser and analysis endpoints.
- `app/models/`: request/response models and the future structured upgrade-assessment contract.

The `app/core/`, `app/parser/`, `app/rag/` and `app/llm/` packages are reserved architectural boundaries, not implemented capabilities. The current parser stays under `app/analysis/` to preserve the working implementation.

## Limitations

This service does not resolve Maven effective POMs, parent inheritance, imported BOMs, transitive dependencies, active profiles, Maven settings or environment-specific properties. The version comparator is not Apache Maven's complete `ComparableVersion`. Risk scores are deterministic heuristics, not calibrated failure probabilities.

RAG ingestion/retrieval, LLM calls, external model credentials and Spring Boot integration are not implemented in this milestone. No ML code or ML runtime dependencies are part of the active service.
