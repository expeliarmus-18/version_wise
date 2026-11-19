
import pytest
from pydantic import ValidationError

from app.models.llm_assessment import (
    DraftFinding,
    LLMAssessmentDraft,
)


def test_draft_supports_top_level_evidence_ids():
    draft = LLMAssessmentDraft(
        status="RECOMMENDED",
        summary="The available documentation supports this upgrade.",
        evidence_ids=["ev-chunk-1"],
    )

    assert draft.evidence_ids == ["ev-chunk-1"]


def test_draft_defaults_to_no_evidence_ids():
    draft = LLMAssessmentDraft(
        status="INSUFFICIENT_EVIDENCE",
        summary="There is insufficient evidence.",
    )

    assert draft.evidence_ids == []


def test_finding_supports_evidence_ids():
    finding = DraftFinding(
        title="Migration change",
        description="A configuration property changed.",
        severity="HIGH",
        evidence_ids=["ev-chunk-1"],
    )

    assert finding.evidence_ids == ["ev-chunk-1"]


def test_draft_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        LLMAssessmentDraft(
            status="RECOMMENDED",
            summary="Supported assessment.",
            invented_source_url="https://example.org",
        )


def test_draft_rejects_invalid_status():
    with pytest.raises(ValidationError):
        LLMAssessmentDraft(
            status="MAYBE",
            summary="Uncertain assessment.",
        )


def test_draft_rejects_empty_summary():
    with pytest.raises(ValidationError):
        LLMAssessmentDraft(
            status="INSUFFICIENT_EVIDENCE",
            summary=" ",
        )
