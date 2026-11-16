
"""End-to-end documentation ingestion for VersionWise RAG."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from app.rag.chunker import chunk_document
from app.rag.loader import fetch_all_documents
from app.rag.sources import get_documentation_sources
from app.rag.vector_store import (
    get_collection_count,
    upsert_chunks,
)


def run_ingestion() -> dict:
    """Fetch, chunk, embed and persist approved documentation sources."""

    sources = get_documentation_sources()

    report = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "attempted_sources": len(sources),
        "successful_sources": [],
        "failed_sources": [],
        "documents_fetched": 0,
        "chunks_created": 0,
        "storage": {},
        "total_chunks_in_collection": 0,
    }

    # Stage 1: Fetch documentation.
    documents, fetch_failures = fetch_all_documents()

    report["documents_fetched"] = len(documents)
    report["failed_sources"].extend(fetch_failures)



    # Stage 2: Chunk each document independently.
    all_chunks = []
    successfully_processed_ids = []

    for document in documents:
        document_id = document.metadata["document_id"]

        try:
            chunks = chunk_document(document)

            if not chunks:
                raise ValueError(
                    "Document extraction produced no usable chunks."
                )

            all_chunks.extend(chunks)
            successfully_processed_ids.append(document_id)

            report["successful_sources"].append(
                {
                    "source_id": document.metadata["source_id"],
                    "title": document.metadata["source_title"],
                    "chunks_created": len(chunks),
                }
            )

        except Exception as exc:
            report["failed_sources"].append(
                {
                    "source_id": document_id,
                    "source_url": document.metadata["source_url"],
                    "error": f"Chunking failed: {exc}",
                }
            )

    report["chunks_created"] = len(all_chunks)

    # Stage 3: Embed and persist chunks.
    # Do not invoke storage when every source failed processing.
    if all_chunks:
        storage_result = upsert_chunks(
            chunks=all_chunks,
            document_ids=successfully_processed_ids,
        )
        report["storage"] = storage_result

    report["successful_source_count"] = len(
        report["successful_sources"]
    )
    report["failed_source_count"] = len(
        report["failed_sources"]
    )

    # Stage 4: Read final persistent collection count.
    if all_chunks:
        report["total_chunks_in_collection"] = get_collection_count()
    report["completed_at"] = datetime.now(timezone.utc).isoformat()

    return report


def main() -> None:
    """Command-line entry point."""
    report = run_ingestion()

    print(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        )
    )

    if report["failed_source_count"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
