
"""Build traceable evidence packages from hybrid RAG results."""

from dataclasses import dataclass
from urllib.parse import urlparse

from langchain_core.documents import Document


class EvidencePackageError(ValueError):
    """Raised when retrieved documentation lacks traceable metadata."""


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    chunk_id: str
    document_id: str
    source_title: str
    source_uri: str
    excerpt: str
    retrieved_at: str | None
    section_heading: str


@dataclass(frozen=True)
class EvidencePackage:
    items: tuple[EvidenceItem, ...]
    limitations: tuple[str, ...]

    @property
    def is_sufficient(self) -> bool:
        return bool(self.items)

    def get_by_id(self, evidence_id: str) -> EvidenceItem | None:
        return next(
            (item for item in self.items if item.evidence_id == evidence_id),
            None,
        )


def _validate_source_uri(uri: object) -> str:
    """Accept only absolute HTTPS documentation URLs."""
    if not isinstance(uri, str) or not uri.strip():
        raise EvidencePackageError("Evidence source URL is missing.")

    parsed = urlparse(uri)

    if parsed.scheme != "https" or not parsed.netloc:
        raise EvidencePackageError(
            "Evidence source URL must be an absolute HTTPS URL."
        )

    return uri


def build_evidence_package(
    documents: list[Document],
) -> EvidencePackage:
    """Convert retrieved documents into verified, traceable evidence."""

    items: list[EvidenceItem] = []
    seen_chunk_ids: set[str] = set()

    for document in documents:
        metadata = document.metadata

        chunk_id = metadata.get("chunk_id")
        document_id = metadata.get("document_id")
        source_title = metadata.get("source_title")
        source_uri = metadata.get("source_url")
        excerpt = document.page_content.strip()

        if not isinstance(chunk_id, str) or not chunk_id.strip():
            raise EvidencePackageError(
                "Retrieved document has no valid chunk ID."
            )

        if chunk_id in seen_chunk_ids:
            continue

        if not isinstance(document_id, str) or not document_id.strip():
            raise EvidencePackageError(
                f"Evidence chunk '{chunk_id}' has no document ID."
            )

        if not isinstance(source_title, str) or not source_title.strip():
            raise EvidencePackageError(
                f"Evidence chunk '{chunk_id}' has no source title."
            )

        if not excerpt:
            raise EvidencePackageError(
                f"Evidence chunk '{chunk_id}' has empty content."
            )

        validated_uri = _validate_source_uri(source_uri)

        retrieved_at = metadata.get("retrieved_at")
        section_heading = metadata.get("section_heading", "Document")

        items.append(
            EvidenceItem(
                evidence_id=f"ev-{chunk_id}",
                chunk_id=chunk_id,
                document_id=document_id,
                source_title=source_title,
                source_uri=validated_uri,
                excerpt=excerpt,
                retrieved_at=retrieved_at,
                section_heading=section_heading,
            )
        )

        seen_chunk_ids.add(chunk_id)

    limitations = ()

    if not items:
        limitations = (
            "No traceable documentation evidence was retrieved.",
            "Compatibility cannot be established from missing evidence.",
        )

    return EvidencePackage(
        items=tuple(items),
        limitations=limitations,
    )
