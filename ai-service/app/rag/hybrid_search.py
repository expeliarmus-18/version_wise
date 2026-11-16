
"""Hybrid semantic and keyword retrieval for VersionWise."""

from __future__ import annotations

from langchain_core.documents import Document

from app.rag.bm25_retriever import bm25_search
from app.rag.fusion import (
    DEFAULT_RRF_K,
    reciprocal_rank_fusion,
)
from app.rag.vector_store import similarity_search


DEFAULT_TOP_K = 5
DEFAULT_RETRIEVAL_CANDIDATES = 10


def hybrid_search(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    retrieval_candidates: int = DEFAULT_RETRIEVAL_CANDIDATES,
    rrf_k: int = DEFAULT_RRF_K,
) -> list[Document]:
    """
    Retrieve documentation using dense and BM25 search,
    then combine both rankings through Reciprocal Rank Fusion.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if retrieval_candidates < 1:
        raise ValueError("retrieval_candidates must be at least 1.")

    if rrf_k < 1:
        raise ValueError("rrf_k must be at least 1.")

    dense_results = similarity_search(
        query=query,
        k=retrieval_candidates,
    )

    keyword_results = bm25_search(
        query=query,
        top_k=retrieval_candidates,
    )

    return reciprocal_rank_fusion(
        dense_results=dense_results,
        bm25_results=keyword_results,
        top_k=top_k,
        rrf_k=rrf_k,
    )
