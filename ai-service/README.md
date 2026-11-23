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
- `app/models/`: request/response models and the structured upgrade-assessment contract.
- `app/rag/sources.py`: registry of approved technical documentation sources.
- `app/rag/loader.py`: HTTP retrieval and HTML-to-text extraction.
- `app/rag/chunker.py`: section-aware document splitting and chunk metadata.
- `app/rag/embeddings.py`: local Hugging Face embedding model configuration.
- `app/rag/vector_store.py`: persistent ChromaDB storage, deduplication and similarity search.
- `app/rag/ingest.py`: end-to-end documentation ingestion workflow.
- `app/rag/bm25_retriever.py`: cached BM25 keyword index over persisted documentation chunks.
- `app/rag/fusion.py`: Reciprocal Rank Fusion with stable chunk-ID deduplication and retrieval metadata.
- `app/rag/hybrid_search.py`: combines dense semantic and BM25 retrieval into ranked evidence.

## RAG documentation ingestion

The service now implements a local documentation-ingestion pipeline using LangChain and ChromaDB.

### Approved documentation sources

The initial ingestion registry contains exactly three sources:

1. Apache Maven POM Reference.
2. Spring Boot 3.0 Migration Guide.
3. Hibernate ORM 6.0 Migration Guide.

### Pipeline

1. Retrieve approved documentation using HTTPX.
2. Extract readable content from HTML using BeautifulSoup.
3. Represent extracted documents using LangChain `Document` objects.
4. Split documents using Markdown heading-aware and recursive character splitters.
5. Generate normalized embeddings using `BAAI/bge-small-en-v1.5`.
6. Store document chunks and metadata in a persistent ChromaDB collection.

### Configuration

- Embedding model: `BAAI/bge-small-en-v1.5`
- Embedding execution: local CPU
- Vector database: ChromaDB
- Collection: `versionwise_documentation`
- Target chunk size: 1,200 characters
- Chunk overlap: 150 characters
- Persistent storage: `ai-service/data/chroma/`

### Run ingestion

From the `ai-service` directory, with the `.versionwise` environment activated:

```bat
python -m app.rag.ingest
```

The ingestion command prints a JSON report containing source successes and failures, chunk counts, storage statistics and collection information.

Repeated ingestion is supported. Existing chunks are checked against their identifiers and content hashes so unchanged content is skipped. Obsolete chunks belonging to successfully processed documents can be removed.

### Retrieval

The service supports hybrid retrieval over the persistent documentation collection.

The retrieval pipeline:

1. Retrieves semantically relevant chunks using the existing ChromaDB vector store.
2. Retrieves keyword matches using a cached BM25 index built from persisted chunks.
3. Combines both rankings using Reciprocal Rank Fusion.
4. Returns ranked LangChain documents with original source metadata and retrieval-ranking information.

Default configuration:

- Final results: 5
- Candidates per retriever: 10
- RRF constant: 60

The application-facing entry point is `app.rag.hybrid_search.hybrid_search`.

The BM25 index is cached in memory. Call `refresh_bm25_index()` after ingestion if the persisted collection changes within the same running process.

The retrieval implementation does not generate LLM assessments.

See `docs/rag/architecture.md` for implementation details and qualitative evaluation.

## Limitations

The Maven parser does not resolve Maven effective POMs, parent inheritance, imported BOMs, transitive dependencies, active profiles, Maven settings or environment-specific properties.

The version comparator is not Apache Maven's complete `ComparableVersion`. Risk scores are deterministic heuristics, not calibrated failure probabilities.

RAG ingestion, persistent vector storage, dense semantic retrieval, BM25 keyword retrieval and hybrid retrieval are implemented. LLM calls, prompt execution, LLM-generated assessment and integration with the Spring Boot backend are not yet implemented.

The assessment model remains a structured output contract; its existence does not mean that an LLM assessment has been generated.

No ML training or ML prediction runtime is part of the active service.
### Local LLM Configuration

VersionWise AI uses Ollama for locally hosted assessment generation.

#### Required Models

Pull the required models:

```bash
ollama pull phi4-mini
ollama pull nomic-embed-text
```

Ensure Ollama is running locally:

```bash
ollama serve
```

#### Configuration

The AI service supports the following environment variables:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `phi4-mini` | Assessment generation model |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_NUM_CTX` | `4096` | Model context window configuration |
| `OLLAMA_NUM_PREDICT` | `512` | Maximum generated tokens |
| `OLLAMA_TIMEOUT_SECONDS` | `120` | Request timeout |

The assessment model runs locally through Ollama. Documentation embeddings continue to use the configured embedding model and existing persistent Chroma vector store.

No external LLM API key is required for local assessment generation.

### Optional Maven Project Context

VersionWise supports optional Maven `pom.xml` upload during dependency upgrade assessment.

When a POM is provided, VersionWise parses available project information and passes bounded project context to the AI assessment service. This context may improve the relevance of documentation retrieval and generated assessments.

The extracted context may include:

- Project coordinates
- Parent project coordinates
- Declared direct dependencies
- Dependency management information
- Parsing warnings

The POM is optional. Dependency coordinates and versions can still be entered manually without uploading a project file.

#### Important Limitations

The uploaded POM is used as project context only. It is not treated as technical evidence.

VersionWise does not currently:

- Resolve the effective Maven POM
- Execute Maven
- Automatically resolve transitive dependencies
- Guarantee that every dependency version can be extracted
- Use project context as proof of compatibility or breaking changes

Compatibility, breaking changes, security findings, and migration recommendations must remain grounded in retrieved technical documentation.

The deterministic risk score is independent of the uploaded POM context.

