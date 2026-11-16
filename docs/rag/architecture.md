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


## 9. Hybrid retrieval architecture

Day 13 extends the Day 12 semantic retrieval foundation with BM25 keyword retrieval and Reciprocal Rank Fusion (RRF).

The hybrid retrieval implementation is maintained in:

- `ai-service/app/rag/bm25_retriever.py`
- `ai-service/app/rag/fusion.py`
- `ai-service/app/rag/hybrid_search.py`

The retrieval flow is:

```text
                    User Query
                        |
                +-------+-------+
                |               |
                v               v
          Dense Retrieval   BM25 Retrieval
                |               |
                |         Persisted Chroma
                |         chunks loaded into
                |         cached BM25 index
                |               |
                +-------+-------+
                        |
                        v
              Reciprocal Rank Fusion
                        |
                        v
                 Ranked Evidence
```

### Dense retrieval

Dense retrieval continues to use the existing LangChain Chroma vector store and the same local embedding model used during ingestion.

It retrieves semantically related documentation chunks from the `versionwise_documentation` collection.

### BM25 keyword retrieval

BM25 uses `rank-bm25` and indexes the existing persisted documentation chunks.

The index is built from ChromaDB documents and metadata. It does not independently fetch documentation, re-ingest sources or generate embeddings.

The tokenizer preserves complete technical identifiers while also indexing their components. This supports searches involving identifiers such as:

- `jakarta.persistence`
- `spring-boot`
- `org.springframework.boot:spring-boot-starter-web:3.0.0`

The in-memory BM25 index is cached to avoid rebuilding it for every query.

`refresh_bm25_index()` is available to rebuild the cached index after documentation ingestion when ingestion and retrieval share a running process.

### Reciprocal Rank Fusion

Dense and BM25 rankings are combined using Reciprocal Rank Fusion.

The contribution of a result at rank \(r\) is:

\[
\frac{1}{k+r}
\]

The contributions from both retrieval rankings are added for each unique chunk.

Configuration:

| Setting | Default |
|---|---:|
| RRF constant (`rrf_k`) | 60 |
| Final result count (`top_k`) | 5 |
| Candidates per retriever | 10 |

The implementation:

- Uses one-based ranks.
- Deduplicates chunks using stable chunk identifiers.
- Does not combine raw vector similarity and BM25 scores.
- Preserves original document content and metadata.
- Adds `rrf_score`, `dense_rank` and `bm25_rank` to returned metadata.
- Supports results present in only one retrieval ranking.

### Retrieval interface

The application-facing entry point is:

`hybrid_search(query, top_k=5, retrieval_candidates=10, rrf_k=60)`

It returns LangChain `Document` objects containing ranked evidence and retrieval metadata.

This is a retrieval capability only. It does not generate LLM responses or assessments.

## 10. Verification and qualitative evaluation

### Corpus verification

The existing persisted collection was inspected before implementing hybrid retrieval.

| Source | Stored chunks |
|---|---:|
| Apache Maven POM Reference | 124 |
| Spring Boot 3.0 Migration Guide | 78 |
| Hibernate ORM 6.0 Migration Guide | 78 |
| **Total** | **280** |

All 280 stored chunks had content and stable chunk identifiers. The inspected corpus also retained the expected source and section metadata.

### Automated tests

The new retrieval test module covers:

- Technical identifier tokenization.
- BM25 relevance and version matching.
- Empty corpus and unmatched queries.
- Invalid retrieval arguments.
- RRF score calculation and deduplication.
- Dense-only and BM25-only results.
- Metadata preservation.
- Hybrid retrieval orchestration.

Verification results:

- Existing regression tests: 42 passed.
- New retrieval tests: 21 passed.
- Complete test suite: **63 passed**.

### Qualitative retrieval evaluation

Five representative queries were evaluated against the actual persisted documentation corpus.

The evaluation compared dense retrieval, BM25 retrieval and fused hybrid results.

Observed findings:

- Spring Boot migration queries retrieved complementary evidence from dependency review, Spring Security, configuration properties and Jakarta EE sections.
- Hibernate SQL and type-mapping retrieval exposed a limitation: some fused results ranked less relevant material, such as an hbm.xml migration section, above the strongest dense result.
- Maven dependency-management and exclusion queries benefited from complementary keyword and semantic matches.
- Jakarta migration queries retrieved relevant Jakarta EE and Jakarta Persistence sections.
- Exact technical-identifier queries benefited from preserving complete identifiers and their components in BM25 tokenization.

Candidate-pool sizes of 5, 10 and 20 were also inspected for selected queries. Increasing the candidate pool did not consistently improve the top results.

The default candidate count remains 10, and the RRF constant remains 60. These are configurable implementation defaults, not experimentally established optimal values.

This evaluation is qualitative. No precision, recall, MRR, NDCG or other quantitative retrieval benchmark is claimed.

## 11. Current limitations

The current implementation provides:

- Approved documentation ingestion.
- Section-aware chunking.
- Local embedding generation.
- Persistent ChromaDB storage.
- Dense semantic retrieval.
- BM25 keyword retrieval.
- Reciprocal Rank Fusion.
- Ranked evidence with source and retrieval metadata.

It does not provide:

- LLM generation or assessment.
- Reranking models.
- Query expansion.
- Agent workflows or LangGraph.
- Backend or frontend integration.
- Quantitative retrieval benchmarks.
- Guaranteed ranking superiority over dense-only retrieval.

The BM25 index is cached in memory. If the persisted collection changes while the same process remains active, the index must be refreshed.

The corpus still consists of exactly the three approved documentation sources. Its coverage is not a guarantee of every linked page or every library version.

## 12. Planned evolution

The next planned milestone is the next stage of the VersionWise AI-service roadmap.

Day 13 completes the hybrid retrieval foundation. Subsequent work must follow the finalized project schedule and assessment contract.

LLM assessment, prompt execution and application integration remain separate capabilities and must not be treated as implemented by this retrieval milestone.
