
from unittest.mock import Mock

import pytest
from langchain_core.documents import Document

from app.llm.assessment_service import (
    AssessmentService,
    AssessmentValidationError,
)
from app.models.assessment import AssessmentStatus
from app.models.llm_assessment import (
    DraftFinding,
    LLMAssessmentDraft,
)
from app.models.risk import UpgradeAnalysisRequest


@pytest.fixture
def upgrade_request():
    return UpgradeAnalysisRequest(
        groupId="org.springframework.boot",
        artifactId="spring-boot-starter-web",
        currentVersion="2.7.18",
        targetVersion="3.0.0",
        metadataAvailable=True,
    )


@pytest.fixture
def document():
    return Document(
        page_content=(
            "Spring Boot 3 migrates to Jakarta EE APIs. "
            "Applications using Java EE packages must migrate."
        ),
        metadata={
            "chunk_id": "spring-chunk-1",
            "document_id": "spring-boot-3-migration",
            "source_title": "Spring Boot 3 Migration Guide",
            "source_url": (
                "https://github.com/spring-projects/"
                "spring-boot/wiki/Spring-Boot-3.0-Migration-Guide"
            ),
            "retrieved_at": "2026-11-18T10:00:00+00:00",
            "section_heading": "Jakarta EE",
        },
    )


def make_provider(draft):
    provider = Mock()
    provider.generate_assessment.return_value = draft
    return provider


def test_no_evidence_returns_insufficient_without_llm(upgrade_request):
    provider = make_provider(None)

    service = AssessmentService(
        provider=provider,
        retrieval_fn=lambda query: [],
    )

    result = service.assess(upgrade_request)

    assert result.status == AssessmentStatus.INSUFFICIENT_EVIDENCE
    assert result.evidence == []
    provider.generate_assessment.assert_not_called()


def test_valid_assessment_uses_application_owned_citations(
    upgrade_request,
    document,
):
    draft = LLMAssessmentDraft(
        status="RECOMMENDED",
        summary="The documentation describes the migration requirements.",
        evidence_ids=["ev-spring-chunk-1"],
        compatibility_findings=[
            DraftFinding(
                title="Jakarta API migration",
                description="Applications must migrate to Jakarta APIs.",
                severity="HIGH",
                evidence_ids=["ev-spring-chunk-1"],
            )
        ],
    )

    provider = make_provider(draft)

    service = AssessmentService(
        provider=provider,
        retrieval_fn=lambda query: [document],
    )

    result = service.assess(upgrade_request)

    assert result.status == AssessmentStatus.RECOMMENDED
    assert len(result.evidence) == 1
    assert result.evidence[0].source_uri == document.metadata["source_url"]
    assert result.breaking_changes == []
    assert result.compatibility_findings[0].evidence_ids == [
        "ev-spring-chunk-1"
    ]


def test_unknown_top_level_evidence_id_is_rejected(
    upgrade_request,
    document,
):
    draft = LLMAssessmentDraft(
        status="RECOMMENDED",
        summary="Supported recommendation.",
        evidence_ids=["invented-evidence"],
    )

    service = AssessmentService(
        provider=make_provider(draft),
        retrieval_fn=lambda query: [document],
    )

    with pytest.raises(AssessmentValidationError):
        service.assess(upgrade_request)


def test_unknown_finding_evidence_id_is_rejected(
    upgrade_request,
    document,
):
    draft = LLMAssessmentDraft(
        status="RECOMMENDED",
        summary="Supported recommendation.",
        evidence_ids=["ev-spring-chunk-1"],
        breaking_changes=[
            DraftFinding(
                title="Breaking change",
                description="An unsupported claim.",
                evidence_ids=["invented-evidence"],
            )
        ],
    )

    service = AssessmentService(
        provider=make_provider(draft),
        retrieval_fn=lambda query: [document],
    )

    with pytest.raises(AssessmentValidationError):
        service.assess(upgrade_request)


def test_finding_without_citations_is_rejected(
    upgrade_request,
    document,
):
    draft = LLMAssessmentDraft(
        status="RECOMMENDED",
        summary="Supported recommendation.",
        evidence_ids=["ev-spring-chunk-1"],
        compatibility_findings=[
            DraftFinding(
                title="Uncited finding",
                description="No supporting evidence.",
                evidence_ids=[],
            )
        ],
    )

    service = AssessmentService(
        provider=make_provider(draft),
        retrieval_fn=lambda query: [document],
    )

    with pytest.raises(AssessmentValidationError):
        service.assess(upgrade_request)


def test_recommended_status_requires_top_level_citations(
    upgrade_request,
    document,
):
    draft = LLMAssessmentDraft(
        status="RECOMMENDED",
        summary="Recommendation without overall citations.",
    )

    service = AssessmentService(
        provider=make_provider(draft),
        retrieval_fn=lambda query: [document],
    )

    with pytest.raises(AssessmentValidationError):
        service.assess(upgrade_request)


def test_recommendation_is_overridden_for_downgrade(document):
    downgrade_request = UpgradeAnalysisRequest(
        groupId="org.example",
        artifactId="demo",
        currentVersion="2.0.0",
        targetVersion="1.0.0",
    )

    draft = LLMAssessmentDraft(
        status="RECOMMENDED",
        summary="The model recommends this change.",
        evidence_ids=["ev-spring-chunk-1"],
    )

    service = AssessmentService(
        provider=make_provider(draft),
        retrieval_fn=lambda query: [document],
    )

    result = service.assess(downgrade_request)

    assert result.status == AssessmentStatus.NOT_RECOMMENDED


def test_insufficient_evidence_draft_is_preserved(
    upgrade_request,
    document,
):
    draft = LLMAssessmentDraft(
        status="INSUFFICIENT_EVIDENCE",
        summary="The retrieved documentation is not conclusive.",
        limitations=["No direct compatibility statement was found."],
    )

    service = AssessmentService(
        provider=make_provider(draft),
        retrieval_fn=lambda query: [document],
    )

    result = service.assess(upgrade_request)

    assert result.status == AssessmentStatus.INSUFFICIENT_EVIDENCE


def test_retrieval_query_contains_dependency_and_analysis(
    upgrade_request,
    document,
):
    provider = make_provider(
        LLMAssessmentDraft(
            status="INSUFFICIENT_EVIDENCE",
            summary="Evidence is inconclusive.",
        )
    )

    captured = []

    def retrieve(query):
        captured.append(query)
        return [document]

    service = AssessmentService(
        provider=provider,
        retrieval_fn=retrieve,
    )

    service.assess(upgrade_request)

    assert len(captured) == 1
    assert "org.springframework.boot" in captured[0]
    assert "spring-boot-starter-web" in captured[0]
    assert "2.7.18" in captured[0]
    assert "3.0.0" in captured[0]


def test_prompt_contains_untrusted_evidence_and_analysis(
    upgrade_request,
    document,
):
    provider = make_provider(
        LLMAssessmentDraft(
            status="INSUFFICIENT_EVIDENCE",
            summary="Evidence is inconclusive.",
        )
    )

    service = AssessmentService(
        provider=provider,
        retrieval_fn=lambda query: [document],
    )

    service.assess(upgrade_request)

    _, kwargs = provider.generate_assessment.call_args
    system_prompt = kwargs["system_prompt"]
    user_prompt = kwargs["user_prompt"]

    assert "untrusted data" in system_prompt.lower()
    assert "deterministic_analysis" in user_prompt
    assert "ev-spring-chunk-1" in user_prompt
    assert document.page_content in user_prompt
