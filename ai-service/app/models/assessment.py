"""Structured contract for future evidence-grounded LLM assessments.

This module defines the output boundary only. It does not call an LLM,
retrieve documents, or claim that an assessment has been generated.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AssessmentStatus(str, Enum):
    RECOMMENDED = "RECOMMENDED"
    NOT_RECOMMENDED = "NOT_RECOMMENDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class FindingSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class EvidenceReference(BaseModel):
    """A traceable source excerpt supporting an assessment."""

    source_title: str = Field(alias="sourceTitle", min_length=1)
    source_uri: str = Field(alias="sourceUri", min_length=1)
    excerpt: str = Field(min_length=1)
    retrieved_at: Optional[str] = Field(default=None, alias="retrievedAt")


class AssessmentFinding(BaseModel):
    """A compatibility, breaking-change, migration, or security finding."""

    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: FindingSeverity = FindingSeverity.UNKNOWN
    evidence_ids: list[str] = Field(default_factory=list, alias="evidenceIds")


class UpgradeAssessment(BaseModel):
    """Future LLM report contract; evidence must be supplied by retrieval."""

    model_config = ConfigDict(populate_by_name=True)

    status: AssessmentStatus
    summary: str = Field(min_length=1)
    compatibility_findings: list[AssessmentFinding] = Field(
        default_factory=list, alias="compatibilityFindings"
    )
    breaking_changes: list[AssessmentFinding] = Field(
        default_factory=list, alias="breakingChanges"
    )
    migration_concerns: list[AssessmentFinding] = Field(
        default_factory=list, alias="migrationConcerns"
    )
    security_findings: list[AssessmentFinding] = Field(
        default_factory=list, alias="securityFindings"
    )
    evidence: list[EvidenceReference] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @field_validator("summary")
    @classmethod
    def summary_must_contain_non_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("summary must not be blank")
        return value.strip()
