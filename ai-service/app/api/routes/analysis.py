from fastapi import APIRouter

from app.analysis.rule_engine import analyze_upgrade
from app.models.risk import UpgradeAnalysisRequest, UpgradeAnalysisResponse

router = APIRouter()


@router.post("/analyze-upgrade", response_model=UpgradeAnalysisResponse)
async def analyze_dependency_upgrade(
    request: UpgradeAnalysisRequest,
) -> UpgradeAnalysisResponse:
    return analyze_upgrade(request)
