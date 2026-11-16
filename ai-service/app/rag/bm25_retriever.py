
"""BM25 keyword retrieval over persisted VersionWise documentation chunks."""

from __future__ import annotations

import re
from functools import lru_cache

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from app.rag.vector_store import get_vector_store


# Preserve complete technical identifiers before extracting components.
TOKEN_PATTERN = re.compile(
    r"[a-zA-Z0-9]+(?:[._:/+-][a-zA-Z0-9]+)*"
)


def tokenize(text: str) -> list[str]:
    """
    Tokenize technical documentation.

    Preserve complete identifiers while also indexing their components.

    Examples:
        spring-boot -> spring-boot, spring, boot
        jakarta.persistence -> jakarta.persistence, jakarta, persistence
        3.0.0 -> 3.0.0, 3, 0, 0
        org.springframework.boot:spring-boot-starter-web:3.0.0
    """
    tokens: list[str] = []

    for token in TOKEN_PATTERN.findall(text):
        normalized = token.lower()

        # Preserve the complete technical identifier.
        tokens.append(normalized)

        # Also index meaningful identifier components.
        components = re.split(r"[._:/+-]+", normalized)

        tokens.extend(
            component
            for component in components
            if component
        )

    return tokens


class BM25Retriever:
    """In-memory BM25 index built from persisted ChromaDB chunks."""

    def __init__(self, documents: list[Document]) -> None:
        self.documents = documents

        self.tokenized_documents = [
            tokenize(document.page_content)
            for document in documents
        ]

        if documents:
            self.index = (
                BM25Okapi(self.tokenized_documents)
                if any(self.tokenized_documents)
                else None
            )
        else:
            self.index = None

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[Document]:
        """Return the highest-ranked keyword matches."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query_tokens = tokenize(query)

        if self.index is None or not query_tokens:
            return []

        scores = self.index.get_scores(query_tokens)

        # Sort by BM25 score descending.
        # Original document position breaks ties deterministically.
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: (-scores[index], index),
        )

        results: list[Document] = []
        query_token_set = set(query_tokens)

        for index in ranked_indices:
            document_tokens = set(self.tokenized_documents[index])

            # Require at least one exact token overlap.
            # Do not discard matches merely because BM25 scores
            # are zero or negative.
            if not query_token_set.intersection(document_tokens):
                continue

            results.append(self.documents[index])

            if len(results) >= top_k:
                break

        return results


@lru_cache(maxsize=1)
def get_bm25_retriever() -> BM25Retriever:
    """
    Load existing ChromaDB chunks and cache the BM25 index.

    No documentation fetching, re-ingestion or embedding generation
    occurs during this operation.
    """
    collection = get_vector_store()._collection

    stored = collection.get(
        include=["documents", "metadatas"]
    )

    documents: list[Document] = []

    for chunk_id, content, metadata in zip(
        stored["ids"],
        stored["documents"] or [],
        stored["metadatas"] or [],
    ):
        if not content:
            continue

        chunk_metadata = dict(metadata or {})
        chunk_metadata["chunk_id"] = chunk_id

        documents.append(
            Document(
                page_content=content,
                metadata=chunk_metadata,
            )
        )

    return BM25Retriever(documents)


def bm25_search(
    query: str,
    top_k: int = 5,
) -> list[Document]:
    """Application-facing BM25 retrieval function."""
    return get_bm25_retriever().search(query, top_k)


def refresh_bm25_index() -> BM25Retriever:
    """Rebuild the index after successful documentation ingestion."""
    get_bm25_retriever.cache_clear()
    return get_bm25_retriever()
