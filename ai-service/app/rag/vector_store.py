
"""Persistent ChromaDB storage for VersionWise documentation chunks."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.rag.embeddings import get_embeddings


COLLECTION_NAME = "versionwise_documentation"

# Resolves to ai-service/data/chroma regardless of the working directory.
PERSIST_DIRECTORY = (
    Path(__file__).resolve().parents[2] / "data" / "chroma"
)


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    """
    Initialize the persistent vector store once per process.

    Chroma creates the persistence directory when necessary.
    Existing stored documents are retained.
    """
    PERSIST_DIRECTORY.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(PERSIST_DIRECTORY),
    )


def upsert_chunks(
    chunks: list[Document],
    document_ids: list[str] | None = None,
) -> dict[str, int]:
    """
    Store new or changed chunks and remove obsolete chunks.

    Identical chunks are skipped using their stable chunk IDs and hashes.
    Obsolete chunks are removed only for successfully fetched documents
    supplied through document_ids.

    Call this function only after fetching and chunking have completed.
    """
    store = get_vector_store()
    collection = store._collection

    existing = collection.get(
        include=["metadatas"],
    )

    existing_metadata = {
        chunk_id: metadata or {}
        for chunk_id, metadata in zip(
            existing["ids"],
            existing["metadatas"] or [],
        )
    }

    # Prevent duplicate IDs in the same ingestion batch.
    unique_chunks: dict[str, Document] = {}

    for chunk in chunks:
        chunk_id = chunk.metadata.get("chunk_id")
        chunk_hash = chunk.metadata.get("chunk_hash")
        parent_id = chunk.metadata.get("document_id")

        if not chunk_id or not chunk_hash or not parent_id:
            raise ValueError(
                "Every chunk must contain chunk_id, chunk_hash "
                "and document_id metadata."
            )

        unique_chunks[chunk_id] = chunk

    chunks_to_store: list[Document] = []
    ids_to_store: list[str] = []

    skipped = 0

    for chunk_id, chunk in unique_chunks.items():
        old_metadata = existing_metadata.get(chunk_id)

        if (
            old_metadata is not None
            and old_metadata.get("chunk_hash")
            == chunk.metadata["chunk_hash"]
        ):
            skipped += 1
            continue

        chunks_to_store.append(chunk)
        ids_to_store.append(chunk_id)

    # Store new or changed chunks before removing any previous chunks.
    if chunks_to_store:
        store.add_documents(
            documents=chunks_to_store,
            ids=ids_to_store,
        )

    # Remove obsolete chunks only for successfully processed documents.
    processed_document_ids = set(document_ids or [])

    if not processed_document_ids:
        processed_document_ids = {
            chunk.metadata["document_id"]
            for chunk in unique_chunks.values()
        }

    current_ids_by_document: dict[str, set[str]] = {}

    for chunk_id, chunk in unique_chunks.items():
        current_ids_by_document.setdefault(
            chunk.metadata["document_id"], set()
        ).add(chunk_id)

    stale_ids: list[str] = []

    for old_id, metadata in existing_metadata.items():
        old_document_id = metadata.get("document_id")

        if old_document_id not in processed_document_ids:
            continue

        current_ids = current_ids_by_document.get(
            old_document_id, set()
        )

        if old_id not in current_ids:
            stale_ids.append(old_id)

    if stale_ids:
        collection.delete(ids=stale_ids)

    return {
        "chunks_received": len(chunks),
        "unique_chunks": len(unique_chunks),
        "chunks_added_or_updated": len(chunks_to_store),
        "chunks_skipped": skipped,
        "obsolete_chunks_removed": len(stale_ids),
    }


def similarity_search(
    query: str,
    k: int = 5,
    filter: dict | None = None,
) -> list[Document]:
    """
    Perform basic dense-vector similarity retrieval.

    Hybrid retrieval and reranking are intentionally deferred.
    """
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if k < 1:
        raise ValueError("k must be at least 1.")

    store = get_vector_store()

    return store.similarity_search(
        query=query,
        k=k,
        filter=filter,
    )


def get_collection_count() -> int:
    """Return the number of chunks currently persisted in ChromaDB."""
    return get_vector_store()._collection.count()
