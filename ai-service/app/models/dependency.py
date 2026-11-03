
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class MavenCoordinates(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    group_id: Optional[str] = Field(default=None, alias="groupId")
    artifact_id: Optional[str] = Field(default=None, alias="artifactId")
    version: Optional[str] = None


class MavenDependency(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    group_id: str = Field(alias="groupId")
    artifact_id: str = Field(alias="artifactId")

    # Resolved value when possible; original expression otherwise.
    version: Optional[str] = None

    declared_version: Optional[str] = Field(
        default=None,
        alias="declaredVersion"
    )

    version_resolved: bool = Field(alias="versionResolved")

    version_resolution: Literal[
        "literal",
        "property",
        "unresolved",
        "missing"
    ] = Field(alias="versionResolution")

    scope: str = "compile"
    type: str = "jar"
    classifier: Optional[str] = None
    optional: bool = False

    origin: Literal["direct", "managed"]


class PomParseResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    project: MavenCoordinates
    parent: Optional[MavenCoordinates] = None

    dependencies: list[MavenDependency]

    managed_dependencies: list[MavenDependency] = Field(
        default_factory=list,
        alias="managedDependencies"
    )

    warnings: list[str] = Field(default_factory=list)


class ParsePomRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pom_xml: str = Field(min_length=1, max_length=2_000_000)
