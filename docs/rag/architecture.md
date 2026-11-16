# VersionWise RAG Architecture

## 1. Purpose

This document describes the documentation-ingestion and vector-storage architecture implemented during Day 12.

The objective is to establish a repeatable local pipeline that makes authoritative dependency and framework documentation available for later retrieval and upgrade assessment.

The current implementation provides ingestion, chunking, embedding, persistent vector storage and semantic similarity search.

It does not yet implement hybrid retrieval or LLM-generated assessments.

## 2. High-level architecture

```text
Approved Documentation Sources
             |
             v
       HTTPX Retrieval
             |
             v
   BeautifulSoup Extraction
             |
             v
   LangChain Documents
             |
             v
   Section-aware Chunking
             |
             v
     Local Embeddings
             |
             v
       ChromaDB Store
             |
             v
    Semantic Similarity Search
```

## 3. Approved documentation sources

The source registry is maintained in:

`ai-service/app/rag/sources.py`

The initial registry contains exactly three sources.

| Source ID | Documentation |
|---|---|
| `apache-maven-pom` | Apache Maven POM Reference |
| `spring-boot-3-migration` | Spring Boot 3.0 Migration Guide |
| `hibernate-orm-6-migration` | Hibernate ORM 6.0 Migration Guide |

The source registry stores source identity, title, URL, authority, library name, document type and relevant scope.

Sources are centrally registered so the ingestion pipeline does not rely on scattered hardcoded URLs.

## 4. Document retrieval and extraction

Implementation:

`ai-service/app/rag/loader.py`

HTTPX retrieves the registered documentation pages.

The loader:

1. Sends HTTP requests with a configured timeout and user agent.
2. Follows redirects.
3. Detects unsuccessful responses.
4. Parses HTML with BeautifulSoup.
5. Removes non-content elements such as scripts, styles, navigation and page chrome.
6. Extracts headings, paragraphs, lists, code blocks and blockquotes.
7. Preserves heading structure in Markdown-style text.
8. Creates LangChain `Document` objects.

Failures are recorded per source so one unavailable source does not automatically prevent attempts to process the others.

### Document metadata

Extracted documents retain metadata including:

- `document_id`
- `source_id`
- `source_title`
- `source_url`
- `authority`
- `library_name`
- `document_type`
- `relevant_scope`
- `retrieved_at`
- `content_hash`

This metadata supports source traceability and later evidence attribution.

## 5. Chunking strategy

Implementation:

`ai-service/app/rag/chunker.py`

The pipeline uses:

- `MarkdownHeaderTextSplitter` for heading-aware segmentation.
- `RecursiveCharacterTextSplitter` for bounded chunk sizes.

Configuration:

| Setting | Value |
|---|---:|
| Target chunk size | 1,200 characters |
| Chunk overlap | 150 characters |
| Header levels | H1 through H6 |
| Start index | Preserved in chunk metadata |

Chunks retain document and source metadata and include section information and content hashes.

The section heading is preserved to make later retrieval results easier to interpret.

Chunking is designed to balance contextual continuity with retrieval granularity.

## 6. Embedding model

Implementation:

`ai-service/app/rag/embeddings.py`

Model:

`BAAI/bge-small-en-v1.5`

The embedding implementation uses LangChain's Hugging Face embeddings integration.

Configuration:

- Local model execution.
- CPU device.
- Normalized embeddings.
- Cached embedding instance to avoid unnecessary repeated initialization.

No hosted embedding API or paid embedding credentials are required.

## 7. Vector storage

Implementation:

`ai-service/app/rag/vector_store.py`

Technology: ChromaDB through LangChain's Chroma integration.

Collection:

`versionwise_documentation`

Persistent directory:

`ai-service/data/chroma/`

The vector store is local to the AI service. Its generated database files are excluded from Git.

### Storage behavior

The storage layer:

- Uses chunk identifiers.
- Retains chunk content and metadata.
- Checks existing identifiers and content hashes.
- Skips unchanged chunks.
- Adds or updates changed chunks.
- Removes obsolete chunks for successfully processed documents.

The ingestion pipeline passes successfully processed document IDs to the storage layer so failed source retrievals do not cause their previously stored chunks to be removed.

## 8. Ingestion orchestration

Implementation:

`ai-service/app/rag/ingest.py`

Run from the `ai-service` directory:

```bat
python -m app.rag.ingest
```

The ingestion workflow:

1. Loads the approved source registry.
2. Attempts retrieval for every registered source.
3. Records source-specific failures.
4. Chunks successfully extracted documents.
5. Sends successful chunks to persistent storage.
6. Reports ingestion and storage statistics.

The command returns a JSON report and uses a non-zero process exit status when source ingestion failures occur.

## 9. Retrieval interface

The vector-store module exposes semantic similarity search.

The retrieval path uses the same embedding model as ingestion and searches the persistent ChromaDB collection.

The initial representative retrieval query was:

`What breaking changes should developers consider when migrating to Spring Boot 3?`

The returned results included relevant sections from the Spring Boot migration guide.

This is an initial functional check, not a benchmark or a comprehensive retrieval-quality evaluation.

## 10. Verification evidence

Initial ingestion:

- 3 sources attempted.
- 3 sources successfully processed.
- 280 chunks created and stored.

Repeat ingestion:

- 280 chunks received.
- 280 unchanged chunks skipped.
- 0 additional chunks added.
- Collection remained at 280 chunks.

Additional checks:

- Dependency consistency check passed.
- Python compilation check passed.
- Existing pytest suite: 42 passed.
- Representative semantic retrieval returned relevant Spring Boot migration-guide sections.

The existing 42 tests are regression tests for the existing application and assessment contract; they should not be interpreted as 42 RAG-specific tests.

## 11. Current limitations

The current implementation is an ingestion and vector-retrieval foundation.

It does not yet provide:

- BM25 keyword retrieval.
- Hybrid retrieval.
- Reciprocal-rank fusion.
- Retrieval evaluation or ranking benchmarks.
- LLM integration.
- Prompt construction and execution.
- Structured LLM assessment generation.
- Spring Boot or frontend integration.

The extracted content is based on the registered HTML pages. The pipeline does not currently claim complete coverage of every linked page or every version of each library's documentation.

## 12. Planned evolution

The next planned milestone is hybrid retrieval.

The intended retrieval flow is:

```text
              User Query
                  |
          +-------+-------+
          |               |
          v               v
    Vector Search     BM25 Search
          |               |
          +-------+-------+
                  |
                  v
       Reciprocal-Rank Fusion
                  |
                  v
          Ranked Evidence
```

Subsequent milestones will introduce LLM assessment and connect the resulting capability to the wider VersionWise application.

These are planned capabilities, not part of the current Day 12 implementation.
