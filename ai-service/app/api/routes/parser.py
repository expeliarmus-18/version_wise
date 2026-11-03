
from fastapi import APIRouter, HTTPException

from app.analysis.maven_parser import (
    PomParseError,
    parse_pom,
)

from app.models.dependency import (
    ParsePomRequest,
    PomParseResponse,
)


router = APIRouter()


@router.post(
    "/parse-pom",
    response_model=PomParseResponse,
)
async def parse_maven_pom(
    request: ParsePomRequest,
):
    try:
        return parse_pom(request.pom_xml)

    except PomParseError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
