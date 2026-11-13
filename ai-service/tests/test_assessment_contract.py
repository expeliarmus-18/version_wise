import pytest
from pydantic import ValidationError

from app.models.assessment import (
    AssessmentFinding,
    AssessmentStatus,
    EvidenceReference,
    UpgradeAssessment,
)


def test_upgrade_assessment_supports_insufficient_evidence():
    report = UpgradeAssessment(
        status=AssessmentStatus.INSUFFICIENT_EVIDENCE,
        summary="Available sources do not establish compatibility.",
        limitations=["No migration guide was retrieved."],
    )

    assert report.status == AssessmentStatus.INSUFFICIENT_EVIDENCE
    assert report.evidence == []
    assert report.model_dump(by_alias=True)["compatibilityFindings"] == []


def test_assessment_preserves_evidence_and_findings():
    evidence = EvidenceReference(
        sourceTitle="Official migration guide",
        sourceUri="https://example.org/migration",
        excerpt="The configuration key was renamed.",
    )
    finding = AssessmentFinding(
        title="Configuration key changed",
        description="Applications using the old key need migration.",
        severity="HIGH",
        evidenceIds=["evidence-1"],
    )
    report = UpgradeAssessment(
        status="NOT_RECOMMENDED",
        summary="A migration change requires attention.",
        breakingChanges=[finding],
        evidence=[evidence],
    )

    serialized = report.model_dump(by_alias=True)
    assert serialized["breakingChanges"][0]["evidenceIds"] == ["evidence-1"]
    assert serialized["evidence"][0]["sourceUri"] == "https://example.org/migration"


def test_assessment_requires_a_nonempty_summary():
    with pytest.raises(ValidationError):
        UpgradeAssessment(status="RECOMMENDED", summary=" ")
