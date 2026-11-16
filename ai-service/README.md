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

The vector-store module exposes semantic similarity search over the persistent documentation collection.

This is the initial vector-retrieval foundation. Hybrid retrieval, BM25, reciprocal-rank fusion, and LLM-generated assessments are not part of Day 12.

See `docs/rag/architecture.md` for the detailed design.

## Limitations

The Maven parser does not resolve Maven effective POMs, parent inheritance, imported BOMs, transitive dependencies, active profiles, Maven settings or environment-specific properties.

The version comparator is not Apache Maven's complete `ComparableVersion`. Risk scores are deterministic heuristics, not calibrated failure probabilities.

RAG ingestion and persistent vector storage are implemented, but hybrid retrieval, LLM calls, prompt execution, and integration with the Spring Boot backend are not yet implemented.

The assessment model remains a structured output contract; its existence does not mean that an LLM assessment has been generated.

No ML training or ML prediction runtime is part of the active service.
