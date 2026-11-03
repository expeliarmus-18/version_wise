
from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.parser import router as parser_router


app = FastAPI(
    title="VersionWise AI Service",
    description=(
        "Python analysis service for Maven dependency "
        "parsing and upgrade intelligence."
    ),
    version="1.0.0",
)

app.include_router(health_router)

app.include_router(
    parser_router,
    prefix="/api/v1",
    tags=["Dependency Analysis"],
)
