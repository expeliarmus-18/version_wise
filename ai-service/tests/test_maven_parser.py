
import pytest

from app.analysis.maven_parser import (
    PomParseError,
    parse_pom,
)


VALID_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.versionwise</groupId>
    <artifactId>demo-project</artifactId>
    <version>1.0.0</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.5.0</version>
    </parent>

    <properties>
        <spring.version>6.2.0</spring.version>
        <framework.version>${spring.version}</framework.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>${framework.version}</version>
        </dependency>

        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.11.0</version>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>com.example</groupId>
            <artifactId>runtime-lib</artifactId>
            <version>2.0.0</version>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>

        <dependency>
            <groupId>com.example</groupId>
            <artifactId>provided-lib</artifactId>
            <version>1.0.0</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-web</artifactId>
                <version>${spring.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
"""


def test_extract_project_coordinates():
    result = parse_pom(VALID_POM)

    assert result.project.group_id == "com.versionwise"
    assert result.project.artifact_id == "demo-project"
    assert result.project.version == "1.0.0"


def test_extract_multiple_direct_dependencies():
    result = parse_pom(VALID_POM)

    assert len(result.dependencies) == 4

    assert result.dependencies[0].group_id == "org.springframework"
    assert result.dependencies[0].artifact_id == "spring-core"


def test_default_dependency_scope_is_compile():
    result = parse_pom(VALID_POM)

    dependency = result.dependencies[0]

    assert dependency.scope == "compile"


def test_dependency_scopes_are_preserved():
    result = parse_pom(VALID_POM)

    scopes = {
        dependency.artifact_id: dependency.scope
        for dependency in result.dependencies
    }

    assert scopes["spring-core"] == "compile"
    assert scopes["junit-jupiter"] == "test"
    assert scopes["runtime-lib"] == "runtime"
    assert scopes["provided-lib"] == "provided"


def test_optional_dependency_is_preserved():
    result = parse_pom(VALID_POM)

    dependency = result.dependencies[2]

    assert dependency.optional is True


def test_managed_dependencies_are_separate():
    result = parse_pom(VALID_POM)

    assert len(result.dependencies) == 4
    assert len(result.managed_dependencies) == 1

    managed = result.managed_dependencies[0]

    assert managed.artifact_id == "spring-web"
    assert managed.version == "6.2.0"
    assert managed.origin == "managed"


def test_simple_properties_are_resolved():
    result = parse_pom(VALID_POM)

    dependency = result.dependencies[0]

    assert dependency.version == "6.2.0"
    assert dependency.declared_version == "${framework.version}"
    assert dependency.version_resolved is True
    assert dependency.version_resolution == "property"


def test_unresolved_properties_are_preserved():
    pom = """
    <project>
        <dependencies>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>unknown-lib</artifactId>
                <version>${unknown.version}</version>
            </dependency>
        </dependencies>
    </project>
    """

    result = parse_pom(pom)

    dependency = result.dependencies[0]

    assert dependency.version == "${unknown.version}"
    assert dependency.version_resolved is False
    assert dependency.version_resolution == "unresolved"
    assert result.warnings


def test_nested_property_references_are_resolved():
    result = parse_pom(VALID_POM)

    dependency = result.dependencies[0]

    assert dependency.version == "6.2.0"


def test_parent_coordinates_are_extracted():
    result = parse_pom(VALID_POM)

    assert result.parent is not None
    assert result.parent.group_id == "org.springframework.boot"
    assert result.parent.artifact_id == "spring-boot-starter-parent"
    assert result.parent.version == "3.5.0"


def test_missing_version_is_reported_without_guessing():
    pom = """
    <project>
        <dependencies>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>managed-lib</artifactId>
            </dependency>
        </dependencies>
    </project>
    """

    result = parse_pom(pom)

    dependency = result.dependencies[0]

    assert dependency.version is None
    assert dependency.version_resolved is False
    assert dependency.version_resolution == "missing"
    assert result.warnings


def test_missing_group_id_is_rejected():
    pom = """
    <project>
        <dependencies>
            <dependency>
                <artifactId>demo</artifactId>
                <version>1.0</version>
            </dependency>
        </dependencies>
    </project>
    """

    with pytest.raises(PomParseError, match="groupId"):
        parse_pom(pom)


def test_missing_artifact_id_is_rejected():
    pom = """
    <project>
        <dependencies>
            <dependency>
                <groupId>com.example</groupId>
                <version>1.0</version>
            </dependency>
        </dependencies>
    </project>
    """

    with pytest.raises(PomParseError, match="artifactId"):
        parse_pom(pom)


def test_malformed_xml_is_rejected():
    with pytest.raises(PomParseError, match="Invalid"):
        parse_pom("<project><dependencies>")


def test_empty_xml_is_rejected():
    with pytest.raises(PomParseError, match="empty"):
        parse_pom("")


def test_non_project_root_is_rejected():
    with pytest.raises(PomParseError, match="root element"):
        parse_pom("<dependencies></dependencies>")


def test_unsafe_xml_is_rejected():
    pom = """<!DOCTYPE project [
        <!ENTITY xxe SYSTEM "file:///C:/Windows/win.ini">
    ]>
    <project>
        <description>&xxe;</description>
    </project>
    """

    with pytest.raises(PomParseError, match="unsafe"):
        parse_pom(pom)
