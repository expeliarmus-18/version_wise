
"""API endpoint for evidence-grounded dependency upgrade assessments."""

from fastapi import APIRouter, HTTPException, status

from app.llm.assessment_service import (
    AssessmentService,
    AssessmentValidationError,
)
from app.llm.factory import get_llm_provider
from app.llm.provider import (
    LLMProviderError,
    LLMProviderUnavailableError,
)
from app.models.assessment import UpgradeAssessment
from app.models.risk import UpgradeAnalysisRequest


router = APIRouter()


@router.post(
    "/assess-upgrade",
    response_model=UpgradeAssessment,
    summary="Generate an evidence-grounded dependency upgrade assessment",
    description=(
        "Combines deterministic upgrade analysis, hybrid documentation "
        "retrieval, and structured LLM assessment generation."
    ),
)
def assess_dependency_upgrade(
    request: UpgradeAnalysisRequest,
) -> UpgradeAssessment:
    """Generate an assessment using retrieved documentation evidence."""

    try:
        provider = get_llm_provider()

        service = AssessmentService(
            provider=provider,
        )

        return service.assess(request)

    except LLMProviderUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except (LLMProviderError, AssessmentValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
