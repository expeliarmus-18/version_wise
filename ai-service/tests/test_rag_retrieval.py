
from unittest.mock import patch

import pytest
from langchain_core.documents import Document

from app.rag.bm25_retriever import BM25Retriever, tokenize
from app.rag.fusion import reciprocal_rank_fusion
from app.rag.hybrid_search import hybrid_search


def make_document(chunk_id: str, content: str) -> Document:
    return Document(
        page_content=content,
        metadata={"chunk_id": chunk_id, "source_title": "Test documentation"},
    )


# ---------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------

def test_tokenize_preserves_technical_identifiers():
    tokens = tokenize(
        "org.springframework.boot:spring-boot-starter-web:3.0.0 "
        "jakarta.persistence"
    )

    assert "org.springframework.boot:spring-boot-starter-web:3.0.0" in tokens
    assert "jakarta.persistence" in tokens
    assert "springframework" in tokens
    assert "starter" in tokens
    assert "3" in tokens
    assert "0" in tokens


def test_tokenize_is_case_insensitive():
    assert tokenize("SpringBoot") == tokenize("springboot")


def test_tokenize_handles_empty_input():
    assert tokenize("") == []
    assert tokenize("   ") == []


# ---------------------------------------------------------------------
# BM25 retrieval
# ---------------------------------------------------------------------

def test_bm25_finds_relevant_document():
    documents = [
        make_document(
            "spring-1",
            "Spring Boot 3 migration introduces Jakarta persistence APIs.",
        ),
        make_document(
            "hibernate-1",
            "Hibernate ORM changes SQL type mappings.",
        ),
    ]

    retriever = BM25Retriever(documents)
    results = retriever.search("jakarta.persistence", top_k=5)

    assert results
    assert results[0].metadata["chunk_id"] == "spring-1"


def test_bm25_matches_version_identifiers():
    documents = [
        make_document("version-1", "Migration guide for version 6.0.0."),
        make_document("version-2", "Migration guide for version 5.0.0."),
    ]

    retriever = BM25Retriever(documents)
    results = retriever.search("6.0.0", top_k=5)

    assert results
    assert results[0].metadata["chunk_id"] == "version-1"


def test_bm25_returns_empty_for_unmatched_query():
    documents = [
        make_document("chunk-1", "Maven dependency management configuration."),
    ]

    retriever = BM25Retriever(documents)

    assert retriever.search("unrelated-identifier", top_k=5) == []


def test_bm25_handles_empty_corpus():
    retriever = BM25Retriever([])

    assert retriever.search("spring boot migration") == []


def test_bm25_rejects_empty_query():
    retriever = BM25Retriever([])

    with pytest.raises(ValueError):
        retriever.search("")


def test_bm25_rejects_invalid_top_k():
    retriever = BM25Retriever([])

    with pytest.raises(ValueError):
        retriever.search("spring boot", top_k=0)


# ---------------------------------------------------------------------
# Reciprocal Rank Fusion
# ---------------------------------------------------------------------

def test_rrf_combines_dense_and_bm25_rankings():
    document_a = make_document("a", "Spring Boot migration.")
    document_b = make_document("b", "Hibernate migration.")

    results = reciprocal_rank_fusion(
        dense_results=[document_a, document_b],
        bm25_results=[document_b, document_a],
        top_k=5,
    )

    assert len(results) == 2

    scores = {
        document.metadata["chunk_id"]: document.metadata["rrf_score"]
        for document in results
    }

    expected_a = (1 / 61) + (1 / 62)
    expected_b = (1 / 62) + (1 / 61)

    assert scores["a"] == pytest.approx(expected_a)
    assert scores["b"] == pytest.approx(expected_b)


def test_rrf_does_not_double_count_duplicate_documents():
    document_a = make_document("a", "Spring Boot migration.")

    results = reciprocal_rank_fusion(
        dense_results=[document_a, document_a],
        bm25_results=[],
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].metadata["rrf_score"] == pytest.approx(1 / 61)


def test_rrf_supports_dense_only_results():
    document = make_document("dense-1", "Dense retrieval result.")

    results = reciprocal_rank_fusion(
        dense_results=[document],
        bm25_results=[],
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].metadata["dense_rank"] == 1
    assert results[0].metadata["bm25_rank"] is None


def test_rrf_supports_bm25_only_results():
    document = make_document("bm25-1", "Keyword retrieval result.")

    results = reciprocal_rank_fusion(
        dense_results=[],
        bm25_results=[document],
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].metadata["dense_rank"] is None
    assert results[0].metadata["bm25_rank"] == 1


def test_rrf_preserves_original_metadata():
    document = make_document("metadata-1", "Spring Boot migration.")

    results = reciprocal_rank_fusion(
        dense_results=[document],
        bm25_results=[],
    )

    assert results[0].metadata["source_title"] == "Test documentation"
    assert results[0].metadata["chunk_id"] == "metadata-1"
    assert "rrf_score" in results[0].metadata


def test_rrf_respects_top_k():
    documents = [
        make_document("a", "First document."),
        make_document("b", "Second document."),
        make_document("c", "Third document."),
    ]

    results = reciprocal_rank_fusion(
        dense_results=documents,
        bm25_results=[],
        top_k=2,
    )

    assert len(results) == 2


def test_rrf_rejects_invalid_top_k():
    with pytest.raises(ValueError):
        reciprocal_rank_fusion([], [], top_k=0)


def test_rrf_rejects_invalid_rrf_k():
    with pytest.raises(ValueError):
        reciprocal_rank_fusion([], [], rrf_k=0)


# ---------------------------------------------------------------------
# Hybrid retrieval orchestration
# ---------------------------------------------------------------------

def test_hybrid_search_combines_both_retrievers():
    dense_document = make_document("dense-1", "Dense result.")
    keyword_document = make_document("keyword-1", "Keyword result.")

    with (
        patch(
            "app.rag.hybrid_search.similarity_search",
            return_value=[dense_document],
        ) as dense_mock,
        patch(
            "app.rag.hybrid_search.bm25_search",
            return_value=[keyword_document],
        ) as bm25_mock,
    ):
        results = hybrid_search(
            "spring boot migration",
            top_k=5,
            retrieval_candidates=10,
        )

    dense_mock.assert_called_once_with(
        query="spring boot migration",
        k=10,
    )
    bm25_mock.assert_called_once_with(
        query="spring boot migration",
        top_k=10,
    )

    assert len(results) == 2


def test_hybrid_search_rejects_empty_query():
    with pytest.raises(ValueError):
        hybrid_search("")


def test_hybrid_search_rejects_invalid_top_k():
    with pytest.raises(ValueError):
        hybrid_search("spring boot", top_k=0)


def test_hybrid_search_rejects_invalid_candidate_count():
    with pytest.raises(ValueError):
        hybrid_search("spring boot", retrieval_candidates=0)
