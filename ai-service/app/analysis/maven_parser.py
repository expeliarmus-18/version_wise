
import re
import xml.etree.ElementTree as ET

from typing import Optional

from defusedxml import ElementTree as SafeET
from defusedxml.common import DefusedXmlException

from app.models.dependency import (
    MavenCoordinates,
    MavenDependency,
    PomParseResponse,
)


PROPERTY_PATTERN = re.compile(r"\$\{([^}]+)\}")

VALID_SCOPES = {
    "compile",
    "provided",
    "runtime",
    "test",
    "system",
    "import",
}


class PomParseError(ValueError):
    """Raised when Maven POM content is invalid or unsupported."""


def local_name(tag: str) -> str:
    """Remove an optional XML namespace from a tag."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def find_children(element, name: str):
    """Return immediate children matching an XML local name."""
    return [
        child
        for child in element
        if local_name(child.tag) == name
    ]


def find_child(element, name: str):
    children = find_children(element, name)
    return children[0] if children else None


def child_text(element, name: str) -> Optional[str]:
    child = find_child(element, name)

    if child is None or child.text is None:
        return None

    value = child.text.strip()
    return value or None


def resolve_value(
    raw_value: Optional[str],
    properties: dict[str, str],
    stack: tuple[str, ...] = (),
):
    """
    Resolve locally declared Maven properties.

    Unresolved expressions are preserved instead of guessed.
    Recursive property references are supported.
    """

    if raw_value is None:
        return None, "missing"

    resolved_property = False
    unresolved = False

    def replace(match):
        nonlocal resolved_property, unresolved

        property_name = match.group(1)

        if property_name not in properties:
            unresolved = True
            return match.group(0)

        if property_name in stack:
            unresolved = True
            return match.group(0)

        property_value = properties[property_name]

        resolved, status = resolve_value(
            property_value,
            properties,
            stack + (property_name,),
        )

        if status == "unresolved":
            unresolved = True
        else:
            resolved_property = True

        return resolved if resolved is not None else match.group(0)

    result = PROPERTY_PATTERN.sub(replace, raw_value)

    if PROPERTY_PATTERN.search(result):
        unresolved = True

    if unresolved:
        return result, "unresolved"

    if resolved_property:
        return result, "property"

    return result, "literal"


def extract_properties(root) -> dict[str, str]:
    properties_element = find_child(root, "properties")

    if properties_element is None:
        return {}

    properties = {}

    for element in properties_element:
        name = local_name(element.tag)

        if element.text and element.text.strip():
            properties[name] = element.text.strip()

    return properties


def extract_coordinates(element, properties):
    if element is None:
        return None

    values = {}

    for xml_name in ("groupId", "artifactId", "version"):
        raw = child_text(element, xml_name)

        resolved, _ = resolve_value(raw, properties)

        values[xml_name] = resolved

    return MavenCoordinates(
        groupId=values["groupId"],
        artifactId=values["artifactId"],
        version=values["version"],
    )


def parse_dependency_element(
    element,
    properties,
    origin,
    index,
    warnings,
):
    group_raw = child_text(element, "groupId")
    artifact_raw = child_text(element, "artifactId")

    if not group_raw:
        raise PomParseError(
            f"{origin.capitalize()} dependency #{index} "
            "is missing groupId."
        )

    if not artifact_raw:
        raise PomParseError(
            f"{origin.capitalize()} dependency #{index} "
            "is missing artifactId."
        )

    group_id, group_status = resolve_value(
        group_raw, properties
    )

    artifact_id, artifact_status = resolve_value(
        artifact_raw, properties
    )

    if group_status == "unresolved":
        warnings.append(
            f"{origin.capitalize()} dependency #{index}: "
            f"unresolved groupId expression '{group_raw}'."
        )

    if artifact_status == "unresolved":
        warnings.append(
            f"{origin.capitalize()} dependency #{index}: "
            f"unresolved artifactId expression '{artifact_raw}'."
        )

    declared_version = child_text(element, "version")

    version, version_status = resolve_value(
        declared_version, properties
    )

    if version_status == "unresolved":
        warnings.append(
            f"{origin.capitalize()} dependency "
            f"{group_id}:{artifact_id} has unresolved version "
            f"'{declared_version}'."
        )

    if version_status == "missing":
        warnings.append(
            f"{origin.capitalize()} dependency "
            f"{group_id}:{artifact_id} has no declared version. "
            "It may be supplied through dependency management "
            "or Maven inheritance."
        )

    scope = child_text(element, "scope") or "compile"
    dependency_type = child_text(element, "type") or "jar"
    classifier = child_text(element, "classifier")

    if scope not in VALID_SCOPES:
        warnings.append(
            f"Dependency {group_id}:{artifact_id} uses "
            f"unrecognized Maven scope '{scope}'."
        )

    optional_raw = child_text(element, "optional")

    optional = False

    if optional_raw is not None:
        normalized = optional_raw.lower()

        if normalized in ("true", "false"):
            optional = normalized == "true"
        else:
            warnings.append(
                f"Dependency {group_id}:{artifact_id} has "
                f"invalid optional value '{optional_raw}'. "
                "Defaulting to false."
            )

    return MavenDependency(
        groupId=group_id,
        artifactId=artifact_id,
        version=version,
        declaredVersion=declared_version,
        versionResolved=version_status in ("literal", "property"),
        versionResolution=version_status,
        scope=scope,
        type=dependency_type,
        classifier=classifier,
        optional=optional,
        origin=origin,
    )


def extract_dependencies(
    dependencies_element,
    properties,
    origin,
    warnings,
):
    if dependencies_element is None:
        return []

    dependencies = []

    for index, element in enumerate(
        find_children(dependencies_element, "dependency"),
        start=1,
    ):
        dependencies.append(
            parse_dependency_element(
                element,
                properties,
                origin,
                index,
                warnings,
            )
        )

    return dependencies


def parse_pom(pom_xml: str) -> PomParseResponse:
    """
    Parse Maven POM XML into structured dependency information.

    This parser does not implement full Maven effective-POM resolution.
    """

    if not isinstance(pom_xml, str) or not pom_xml.strip():
        raise PomParseError("POM XML input cannot be empty.")

    try:
        root = SafeET.fromstring(pom_xml)

    except (ET.ParseError, DefusedXmlException, ValueError) as exc:
        raise PomParseError(
            "Invalid or unsafe POM XML document."
        ) from exc

    if local_name(root.tag) != "project":
        raise PomParseError(
            "Invalid POM document: root element must be 'project'."
        )

    properties = extract_properties(root)
    warnings = []

    project = extract_coordinates(root, properties)

    parent_element = find_child(root, "parent")
    parent = extract_coordinates(parent_element, properties)

    if project.group_id is None:
        warnings.append(
            "Project groupId is not declared in the current POM. "
            "Parent inheritance is not resolved."
        )

    if project.version is None:
        warnings.append(
            "Project version is not declared in the current POM. "
            "Parent inheritance is not resolved."
        )

    dependencies_element = find_child(root, "dependencies")

    dependencies = extract_dependencies(
        dependencies_element,
        properties,
        "direct",
        warnings,
    )

    management_element = find_child(root, "dependencyManagement")

    managed_dependencies_element = (
        find_child(management_element, "dependencies")
        if management_element is not None
        else None
    )

    managed_dependencies = extract_dependencies(
        managed_dependencies_element,
        properties,
        "managed",
        warnings,
    )

    return PomParseResponse(
        project=project,
        parent=parent,
        dependencies=dependencies,
        managedDependencies=managed_dependencies,
        warnings=warnings,
    )
