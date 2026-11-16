"""Fetch and extract approved technical documentation."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from app.rag.sources import (
    DocumentationSource,
    get_documentation_sources,
)


REQUEST_TIMEOUT = 30.0

HEADERS = {
    "User-Agent": "VersionWise-Documentation-Ingestion/1.0",
}

BOILERPLATE_TAGS = {
    "script",
    "style",
    "nav",
    "footer",
    "header",
    "aside",
    "noscript",
    "svg",
    "form",
}

HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


class DocumentFetchError(RuntimeError):
    """Raised when a documentation source cannot be fetched or extracted."""


def _extract_content(html: str) -> str:
    """Extract readable documentation while preserving section headings."""
    soup = BeautifulSoup(html, "html.parser")

    for element in soup.find_all(BOILERPLATE_TAGS):
        element.decompose()

    main = soup.find("main") or soup.find("article") or soup.body

    if main is None:
        raise DocumentFetchError("HTML contains no extractable document body.")

    lines: list[str] = []

    for element in main.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre", "blockquote"]
    ):
        text = element.get_text(" ", strip=True)

        if not text:
            continue

        if element.name in HEADING_TAGS:
            lines.append(f"\n{'#' * int(element.name[1])} {text}\n")
        elif element.name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)

    content = "\n".join(lines).strip()

    if len(content) < 100:
        raise DocumentFetchError(
            "Extracted documentation is unexpectedly short."
        )

    return content


def fetch_document(
    source: DocumentationSource,
    client: httpx.Client,
) -> Document:
    """Fetch one source and convert it into a traceable LangChain document."""
    try:
        response = client.get(source.url)
        response.raise_for_status()

        content = _extract_content(response.text)

    except (httpx.HTTPError, DocumentFetchError) as exc:
        raise DocumentFetchError(
            f"Failed to ingest source '{source.source_id}': {exc}"
        ) from exc

    content_hash = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    retrieved_at = datetime.now(timezone.utc).isoformat()

    return Document(
        page_content=content,
        metadata={
            "document_id": source.source_id,
            "source_id": source.source_id,
            "source_title": source.title,
            "source_url": source.url,
            "authority": source.authority,
            "library_name": source.library_name,
            "document_type": source.document_type,
            "relevant_scope": source.relevant_scope,
            "retrieved_at": retrieved_at,
            "content_hash": content_hash,
        },
    )


def fetch_all_documents() -> tuple[list[Document], list[dict[str, str]]]:
    """
    Fetch all approved sources.

    Failed sources are recorded explicitly; they are never silently skipped.
    """
    documents: list[Document] = []
    failures: list[dict[str, str]] = []

    with httpx.Client(
        timeout=REQUEST_TIMEOUT,
        headers=HEADERS,
        follow_redirects=True,
    ) as client:
        for source in get_documentation_sources():
            try:
                document = fetch_document(source, client)
                documents.append(document)

            except DocumentFetchError as exc:
                failures.append(
                    {
                        "source_id": source.source_id,
                        "source_url": source.url,
                        "error": str(exc),
                    }
                )

    return documents, failures