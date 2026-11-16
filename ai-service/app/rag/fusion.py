
"""Reciprocal Rank Fusion for VersionWise hybrid retrieval."""

from __future__ import annotations

from langchain_core.documents import Document


DEFAULT_RRF_K = 60


def reciprocal_rank_fusion(
    dense_results: list[Document],
    bm25_results: list[Document],
    top_k: int = 5,
    rrf_k: int = DEFAULT_RRF_K,
) -> list[Document]:
    """
    Combine dense and BM25 rankings using Reciprocal Rank Fusion.

    RRF score = sum(1 / (rrf_k + rank))

    Ranks are one-based. Raw similarity and BM25 scores are never
    combined directly.
    """
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if rrf_k < 1:
        raise ValueError("rrf_k must be at least 1.")

    scores: dict[str, float] = {}
    documents: dict[str, Document] = {}
    ranks: dict[str, dict[str, int | None]] = {}

    rankings = (
        ("dense", dense_results),
        ("bm25", bm25_results),
    )

    for retrieval_method, results in rankings:
        seen_in_ranking: set[str] = set()

        for rank, document in enumerate(results, start=1):
            chunk_id = document.metadata.get("chunk_id") or document.id

            if not chunk_id:
                raise ValueError(
                    "Every retrieved document must have a stable chunk ID."
                )

            chunk_id = str(chunk_id)

            # Count a chunk only once per retrieval ranking.
            if chunk_id in seen_in_ranking:
                continue

            seen_in_ranking.add(chunk_id)

            if chunk_id not in scores:
                scores[chunk_id] = 0.0
                documents[chunk_id] = document
                ranks[chunk_id] = {
                    "dense": None,
                    "bm25": None,
                }

            scores[chunk_id] += 1.0 / (rrf_k + rank)
            ranks[chunk_id][retrieval_method] = rank

    # Stable sorting preserves insertion order for equal scores.
    ranked_ids = sorted(
        scores,
        key=lambda chunk_id: scores[chunk_id],
        reverse=True,
    )

    fused_results = []

    for chunk_id in ranked_ids[:top_k]:
        original = documents[chunk_id]

        metadata = {
            **original.metadata,
            "rrf_score": scores[chunk_id],
            "dense_rank": ranks[chunk_id]["dense"],
            "bm25_rank": ranks[chunk_id]["bm25"],
        }

        fused_results.append(
            Document(
                page_content=original.page_content,
                metadata=metadata,
                id=original.id,
            )
        )

    return fused_results
