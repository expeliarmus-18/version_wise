
"""Section-aware document chunking with reproducible chunk identifiers."""

from __future__ import annotations

import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150

MARKDOWN_HEADERS = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
    ("####", "h4"),
    ("#####", "h5"),
    ("######", "h6"),
]


def _content_hash(content: str) -> str:
    """Return the SHA-256 hash of normalized chunk content."""
    normalized = content.strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _section_heading(metadata: dict) -> str:
    """Build a readable section path from Markdown heading metadata."""
    headings = [
        metadata[key]
        for key in ("h1", "h2", "h3", "h4", "h5", "h6")
        if metadata.get(key)
    ]

    return " > ".join(headings) if headings else "Document"


def chunk_document(document: Document) -> list[Document]:
    """Split a source document into section-aware, traceable chunks."""
    if not document.page_content.strip():
        return []

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS,
        strip_headers=False,
    )

    sections = header_splitter.split_text(document.page_content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,
    )

    chunks: list[Document] = []

    for section in sections:
        section_name = _section_heading(section.metadata)

        section_chunks = text_splitter.split_documents([section])

        for chunk in section_chunks:
            content = chunk.page_content.strip()

            if not content:
                continue

            content_hash = _content_hash(content)
            document_id = document.metadata["document_id"]

            start_index = chunk.metadata.get("start_index", 0)

            chunk_id_input = (
               f"{document_id}:{section_name}:{start_index}:{content_hash}"
            )

            chunk_id = hashlib.sha256(
                chunk_id_input.encode("utf-8")
            ).hexdigest()

            metadata = {
                **document.metadata,
                **chunk.metadata,
                "document_id": document_id,
                "chunk_id": chunk_id,
                "section_heading": section_name,
                "chunk_hash": content_hash,
            }

            chunks.append(
                Document(
                    page_content=content,
                    metadata=metadata,
                )
            )

    return chunks


def chunk_documents(documents: list[Document]) -> list[Document]:
    """Chunk multiple source documents while preserving their metadata."""
    chunks: list[Document] = []

    for document in documents:
        chunks.extend(chunk_document(document))

    return chunks
