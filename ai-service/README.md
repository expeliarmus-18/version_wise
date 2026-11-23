# VersionWise AI Service

The VersionWise AI service is a FastAPI application that parses Maven POM declarations, performs deterministic dependency-upgrade analysis, retrieves technical documentation through hybrid search, and supports locally hosted LLM assessment through Ollama.

## Requirements

- Python 3.10+
- Dependencies from `requirements.txt`
- Ollama for local assessment generation
- The documentation corpus ingested into the local ChromaDB store for retrieval

## Setup on Windows PowerShell

Run from the repository root:

```powershell
cd ai-service
py -3.10 -m venv .versionwise
.\.versionwise\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the service

```powershell
python -m uvicorn app.main:app --reload
```

- Health: `http://127.0.0.1:8000/health`
- Swagger UI: `http://127.0.0.1:8000/docs`
- POM parser: `POST /api/v1/parse-pom`
- Upgrade analysis: `POST /api/v1/analyze-upgrade`

## Tests

From the `ai-service` directory, with the virtual environment active:

```powershell
python -m pytest tests -q
```

## Core modules

| Module | Responsibility |
|---|---|
| `app/analysis/maven_parser.py` | Secure XML parsing and supported local Maven property substitution |
| `app/analysis/version_comparator.py` | Conservative, bounded version ordering |
| `app/analysis/rule_engine.py` | Deterministic heuristic risk findings |
| `app/api/routes/` | Health, POM parsing, and upgrade-analysis endpoints |
| `app/models/` | Request/response schemas and structured assessment contracts |
| `app/rag/sources.py` | Registry of approved technical documentation sources |
| `app/rag/loader.py` | HTTP retrieval and HTML-to-text extraction |
| `app/rag/chunker.py` | Section-aware document splitting and metadata |
| `app/rag/embeddings.py` | Local embedding configuration for documentation retrieval |
| `app/rag/vector_store.py` | Persistent ChromaDB storage, deduplication, and similarity search |
| `app/rag/ingest.py` | End-to-end documentation ingestion |
| `app/rag/bm25_retriever.py` | Cached BM25 keyword retrieval over persisted chunks |
| `app/rag/fusion.py` | Reciprocal Rank Fusion and stable chunk deduplication |
| `app/rag/hybrid_search.py` | Dense and BM25 retrieval combined into a ranked evidence set |
| Assessment modules | Prompt construction, Ollama invocation, structured assessment, and evidence-aware output |

## Documentation ingestion

VersionWise maintains a small, approved documentation registry containing:

1. Apache Maven POM Reference
2. Spring Boot 3.0 Migration Guide
3. Hibernate ORM 6.0 Migration Guide

The ingestion workflow:

1. Retrieves approved documentation using HTTPX.
2. Extracts readable HTML content using BeautifulSoup.
3. Converts content into LangChain `Document` objects.
4. Splits content using heading-aware and recursive character splitters.
5. Generates normalized local embeddings.
6. Stores chunks and metadata in a persistent ChromaDB collection.

### Configuration

| Setting | Value |
|---|---|
| Embedding model | `BAAI/bge-small-en-v1.5` |
| Embedding execution | Local CPU |
| Vector database | ChromaDB |
| Collection | `versionwise_documentation` |
| Target chunk size | 1,200 characters |
| Chunk overlap | 150 characters |
| Persistent storage | `ai-service/data/chroma/` |

### Run ingestion

From the `ai-service` directory:

```powershell
python -m app.rag.ingest
```

The command prints a JSON report with source outcomes, chunk counts, storage statistics, and collection details.

Repeated ingestion is supported. Existing chunks are checked using stable identifiers and content hashes so unchanged content can be skipped. Obsolete chunks associated with successfully processed documents can be removed.

## Hybrid retrieval

The application-facing retrieval entry point is:

```text
app.rag.hybrid_search.hybrid_search
```

The pipeline:

1. Retrieves semantically relevant chunks from ChromaDB.
2. Retrieves keyword matches using a cached BM25 index over persisted chunks.
3. Combines the rankings using Reciprocal Rank Fusion.
4. Deduplicates by stable chunk identity.
5. Returns ranked documents with original source metadata and retrieval information.

Default retrieval configuration:

| Setting | Default |
|---|---:|
| Final results | 5 |
| Candidates per retriever | 10 |
| RRF constant | 60 |

The BM25 index is cached in memory. Call `refresh_bm25_index()` after ingestion if the collection changes while the process is running.

See [`../docs/rag/architecture.md`](../docs/rag/architecture.md) for the architecture and implementation details.

## Local LLM assessment

Assessment generation uses Ollama, so a hosted LLM API key is not required for local generation.

Pull the configured models:

```powershell
ollama pull phi4-mini
ollama pull nomic-embed-text
```

Ensure Ollama is running:

```powershell
ollama serve
```

### Environment configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `phi4-mini` | Assessment generation model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_NUM_CTX` | `4096` | Context-window configuration |
| `OLLAMA_NUM_PREDICT` | `512` | Maximum generated tokens |
| `OLLAMA_TIMEOUT_SECONDS` | `120` | Request timeout |

Use local environment configuration for overrides. Do not commit credentials or machine-specific settings.

## Optional Maven project context

The upgrade-assessment workflow supports an optional `pom.xml` upload.

When supplied, the service parses available project information and passes bounded context to the assessment workflow. Extracted information may include:

- Project coordinates
- Parent project coordinates
- Declared direct dependencies
- Dependency-management information
- Parsing warnings

The POM is optional. Users can provide dependency coordinates and versions manually.

### POM context limitations

The uploaded POM is used as project context, not technical evidence. The service does not currently:

- Resolve the effective Maven POM
- Execute Maven
- Automatically resolve transitive dependencies
- Guarantee that every dependency version can be extracted
- Use project context as proof of compatibility or breaking changes

Compatibility, breaking changes, security findings, and migration recommendations must be grounded in retrieved technical documentation. Deterministic risk scoring is independent of uploaded POM context.

## Analysis limitations

- The parser does not fully resolve parent inheritance, imported BOMs, active profiles, Maven settings, transitive dependencies, or environment-specific properties.
- Version comparison is not a complete implementation of Maven's `ComparableVersion`.
- Risk scores are deterministic heuristics, not calibrated failure probabilities.
- Retrieval and assessment depend on corpus coverage and evidence quality. An assessment may report insufficient evidence rather than make an unsupported claim.
- No trained ML model or ML prediction runtime is part of the active service.
