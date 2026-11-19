
import pytest
from langchain_core.documents import Document

from app.rag.evidence import (
    EvidencePackageError,
    build_evidence_package,
)


def make_document(
    chunk_id="chunk-1",
    content="The configuration property changed.",
    **metadata_overrides,
):
    metadata = {
        "chunk_id": chunk_id,
        "document_id": "spring-boot-3-migration",
        "source_title": "Spring Boot Migration Guide",
        "source_url": "https://example.org/migration",
        "retrieved_at": "2026-11-18T10:00:00+00:00",
        "section_heading": "Migration > Configuration",
    }
    metadata.update(metadata_overrides)

    return Document(page_content=content, metadata=metadata)


def test_builds_traceable_evidence_item():
    package = build_evidence_package([make_document()])

    assert len(package.items) == 1

    item = package.items[0]
    assert item.evidence_id == "ev-chunk-1"
    assert item.chunk_id == "chunk-1"
    assert item.document_id == "spring-boot-3-migration"
    assert item.source_title == "Spring Boot Migration Guide"
    assert item.source_uri == "https://example.org/migration"
    assert item.excerpt == "The configuration property changed."
    assert item.section_heading == "Migration > Configuration"


def test_duplicate_chunks_are_deduplicated():
    package = build_evidence_package([
        make_document(),
        make_document(),
    ])

    assert len(package.items) == 1


def test_empty_retrieval_returns_insufficient_evidence():
    package = build_evidence_package([])

    assert package.items == ()
    assert package.is_sufficient is False
    assert package.limitations


def test_evidence_ids_resolve_to_original_items():
    package = build_evidence_package([make_document()])

    item = package.get_by_id("ev-chunk-1")

    assert item is not None
    assert item.chunk_id == "chunk-1"
    assert package.get_by_id("invented-id") is None


@pytest.mark.parametrize(
    "source_url",
    [
        "http://example.org/migration",
        "javascript:alert(1)",
        "",
        None,
    ],
)
def test_rejects_invalid_source_urls(source_url):
    document = make_document(source_url=source_url)

    with pytest.raises(EvidencePackageError):
        build_evidence_package([document])


def test_rejects_missing_chunk_id():
    document = make_document(chunk_id=None)

    with pytest.raises(EvidencePackageError):
        build_evidence_package([document])


def test_rejects_missing_source_title():
    document = make_document(source_title="")

    with pytest.raises(EvidencePackageError):
        build_evidence_package([document])


def test_rejects_empty_excerpt():
    document = make_document(content="  ")

    with pytest.raises(EvidencePackageError):
        build_evidence_package([document])
