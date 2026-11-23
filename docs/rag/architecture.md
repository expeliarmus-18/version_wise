# VersionWise Documentation Retrieval and Assessment Architecture

## Overview

VersionWise uses a local documentation-retrieval pipeline to provide technical context for Java/Maven dependency upgrades. The system combines dense semantic retrieval and BM25 keyword retrieval, fuses their rankings, and supplies retrieved evidence to a locally hosted assessment model.

The deterministic dependency-analysis baseline remains separate from the LLM assessment. Project context extracted from an optional Maven POM may improve relevance, but it is not treated as evidence of compatibility or breaking changes.

## System flow

```text
Upgrade request
  - dependency coordinates
  - current version
  - target version
  - optional pom.xml project context
        |
        v
Deterministic analysis
  - supported version comparison
  - heuristic risk findings
        |
        v
Evidence retrieval query
        |
        +------------------------------+
        |                              |
        v                              v
Dense semantic retrieval          BM25 keyword retrieval
ChromaDB                          Persisted corpus
        |                              |
        +---------------+--------------+
                        |
                        v
              Reciprocal Rank Fusion
              - rank combination
              - stable deduplication
                        |
                        v
                Ranked evidence chunks
                        |
                        v
               Local Ollama assessment
                        |
                        v
             Structured assessment output
```

## Approved documentation sources

The initial documentation registry contains three approved sources:

1. Apache Maven POM Reference
2. Spring Boot 3.0 Migration Guide
3. Hibernate ORM 6.0 Migration Guide

The corpus is intentionally limited. Retrieval quality and assessment coverage depend on the material available in these sources.

## Ingestion pipeline

The ingestion workflow is implemented in `app.rag.ingest`.

1. Retrieve approved documentation using HTTPX.
2. Extract readable HTML using BeautifulSoup.
3. Convert extracted content into LangChain `Document` objects.
4. Split documents using heading-aware and recursive character splitters.
5. Generate normalized embeddings locally.
6. Persist chunks and metadata in ChromaDB.

### Chunking configuration

| Setting | Value |
|---|---:|
| Target chunk size | 1,200 characters |
| Chunk overlap | 150 characters |

Chunks retain source metadata so retrieved evidence can be traced back to its documentation source.

### Embedding and storage

| Component | Configuration |
|---|---|
| Embedding model | `BAAI/bge-small-en-v1.5` |
| Embedding execution | Local CPU |
| Vector database | ChromaDB |
| Collection | `versionwise_documentation` |
| Persistent directory | `ai-service/data/chroma/` |

Repeated ingestion is supported. Stable chunk identifiers and content hashes allow unchanged content to be skipped. Obsolete chunks associated with successfully processed documents can be removed.

## Hybrid retrieval

The application-facing entry point is:

```text
app.rag.hybrid_search.hybrid_search
```

### Dense semantic retrieval

Dense retrieval uses the persisted ChromaDB vector store to identify chunks semantically related to the query. This can retrieve relevant content even when the query and documentation use different wording.

### BM25 keyword retrieval

BM25 retrieves chunks based on lexical overlap. Its index is built from persisted documentation chunks and cached in memory.

The BM25 index can be refreshed after the corpus changes:

```python
refresh_bm25_index()
```

### Reciprocal Rank Fusion

The dense and BM25 rankings are combined using Reciprocal Rank Fusion (RRF). RRF combines ranking positions rather than directly comparing scores from different retrieval methods.

The fusion implementation:

- Combines the dense and BM25 candidate rankings.
- Uses a configurable RRF constant.
- Deduplicates using stable chunk identifiers.
- Preserves source metadata and retrieval-ranking information.

### Default retrieval settings

| Setting | Default |
|---|---:|
| Final results | 5 |
| Candidates per retriever | 10 |
| RRF constant | 60 |

## Assessment generation

The assessment workflow uses Ollama for local LLM generation. The configured model is `phi4-mini` by default.

Retrieved technical documentation is supplied as evidence context for structured assessment generation. The assessment contract is intended to separate evidence-supported conclusions from uncertainty or insufficient evidence.

The assessment service is configured through environment variables:

| Variable | Default |
|---|---|
| `OLLAMA_MODEL` | `phi4-mini` |
| `OLLAMA_BASE_URL` | `http://localhost:11434` |
| `OLLAMA_NUM_CTX` | `4096` |
| `OLLAMA_NUM_PREDICT` | `512` |
| `OLLAMA_TIMEOUT_SECONDS` | `120` |

Local generation does not require a hosted LLM API key.

## Optional Maven project context

An optional uploaded `pom.xml` can provide bounded project context to the assessment workflow.

Extracted context may include:

- Project coordinates
- Parent coordinates
- Declared direct dependencies
- Dependency-management information
- Parsing warnings

This context may help identify which retrieved documentation is relevant to the user's project.

The POM is **not technical evidence**. It must not independently support claims about compatibility, breaking changes, security findings, or migration requirements.

The deterministic risk score is independent of uploaded POM context.

## Deterministic analysis boundary

The deterministic analysis remains a separate baseline. It uses supported Maven declaration parsing, conservative version comparison, and rule-based findings.

The implementation does not fully resolve:

- Maven effective POMs
- Parent inheritance
- Imported BOMs
- Active profiles
- Maven settings
- Transitive dependencies
- Environment-specific properties

The version comparator is not a complete implementation of Apache Maven's `ComparableVersion`. Deterministic risk scores are heuristics and are not calibrated probabilities of upgrade failure.

## Evidence and quality limitations

The corpus is small and focused on the approved documentation sources. Retrieval can miss relevant material when a topic is absent from the corpus or when source content is insufficiently specific.

The assessment may return an insufficient-evidence result. This is preferable to presenting unsupported technical conclusions, but it also means that useful assessments are not guaranteed for every dependency/version pair.

Assessment quality has not been established through a comprehensive benchmark across dependency upgrades. The current implementation should be considered a documentation-grounded assistance workflow, not a validated compatibility prediction system.

## Persistence and local data

The ChromaDB collection is persisted under:

```text
ai-service/data/chroma/
```

This directory contains generated local retrieval data and should not be committed to Git.

## Key design principles

- **Deterministic baseline:** rule-based analysis remains independent from LLM output.
- **Hybrid retrieval:** semantic and keyword retrieval complement each other.
- **Evidence grounding:** retrieved technical documentation is the basis for technical assessment claims.
- **Context is not evidence:** an uploaded POM helps contextualize the request but does not prove compatibility.
- **Conservative uncertainty:** insufficient evidence is an acceptable assessment outcome.
- **Local-first inference:** assessment generation runs through Ollama rather than requiring a hosted LLM API.
