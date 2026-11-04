from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class UpgradeAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    group_id: str = Field(alias="groupId", min_length=1, max_length=300)
    artifact_id: str = Field(alias="artifactId", min_length=1, max_length=300)
    current_version: str = Field(alias="currentVersion", min_length=1, max_length=200)
    target_version: str = Field(alias="targetVersion", min_length=1, max_length=200)
    scope: Optional[str] = Field(default=None, max_length=50)
    dependency_type: Optional[str] = Field(default=None, alias="type", max_length=100)
    classifier: Optional[str] = Field(default=None, max_length=200)
    version_resolution: Optional[Literal["literal", "property", "unresolved", "missing"]] = Field(
        default=None, alias="versionResolution"
    )
    metadata_available: Optional[bool] = Field(default=None, alias="metadataAvailable")


class RiskFactor(BaseModel):
    rule_id: str = Field(alias="ruleId")
    name: str
    contribution: int
    explanation: str
    evaluated: bool = True
    evidence_source: Optional[str] = Field(default=None, alias="evidenceSource")
    current_version: Optional[str] = Field(default=None, alias="currentVersion")
    target_version: Optional[str] = Field(default=None, alias="targetVersion")


class UpgradeAnalysisResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    group_id: str = Field(alias="groupId")
    artifact_id: str = Field(alias="artifactId")
    current_version: str = Field(alias="currentVersion")
    target_version: str = Field(alias="targetVersion")
    comparison: Literal["upgrade", "downgrade", "equal", "unknown"]
    risk_score: int = Field(alias="riskScore", ge=0, le=100)
    risk_category: Literal["LOW", "MODERATE", "HIGH", "CRITICAL"] = Field(alias="riskCategory")
    factors: list[RiskFactor]
    warnings: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    score_is_probability: Literal[False] = Field(default=False, alias="scoreIsProbability")
