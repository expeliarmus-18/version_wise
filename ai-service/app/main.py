
from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.parser import router as parser_router
from app.api.routes.analysis import router as analysis_router


app = FastAPI(
    title="VersionWise AI Service",
    description=(
        "Independent Python service for Maven dependency parsing and "
        "deterministic upgrade analysis. Evidence retrieval and LLM "
        "assessment are planned capabilities, not currently implemented."
    ),
    version="1.0.0",
)

app.include_router(health_router)

app.include_router(
    parser_router,
    prefix="/api/v1",
    tags=["Dependency Analysis"],
)

app.include_router(analysis_router, prefix="/api/v1", tags=["Dependency Analysis"])
