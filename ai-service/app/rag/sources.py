"""Authoritative documentation sources used by VersionWise RAG."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentationSource:
    source_id: str
    title: str
    url: str
    authority: str
    library_name: str
    document_type: str
    relevant_scope: str


DOCUMENTATION_SOURCES: tuple[DocumentationSource, ...] = (
    DocumentationSource(
        source_id="apache-maven-pom",
        title="Apache Maven POM Reference",
        url="https://maven.apache.org/pom.html",
        authority="Apache Software Foundation",
        library_name="Apache Maven",
        document_type="reference",
        relevant_scope="Maven project configuration and dependency declarations",
    ),
    DocumentationSource(
        source_id="spring-boot-3-migration",
        title="Spring Boot 3.0 Migration Guide",
        url=(
            "https://github.com/spring-projects/spring-boot/"
            "wiki/Spring-Boot-3.0-Migration-Guide"
        ),
        authority="Spring",
        library_name="Spring Boot",
        document_type="migration-guide",
        relevant_scope="Spring Boot 3 migration and compatibility changes",
    ),
    DocumentationSource(
        source_id="hibernate-orm-6-migration",
        title="Hibernate ORM 6.0 Migration Guide",
        url=(
            "https://docs.hibernate.org/orm/6.0/migration-guide/"
            "migration-guide/"
        ),
        authority="Hibernate",
        library_name="Hibernate ORM",
        document_type="migration-guide",
        relevant_scope="Hibernate ORM 6 migration and compatibility changes",
    ),
)


def get_documentation_sources() -> tuple[DocumentationSource, ...]:
    """Return the approved documentation source registry."""
    return DOCUMENTATION_SOURCES