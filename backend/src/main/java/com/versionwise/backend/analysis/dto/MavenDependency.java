package com.versionwise.backend.analysis.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public record MavenDependency(
        String groupId,
        String artifactId,
        String version,
        String declaredVersion,
        boolean versionResolved,
        String versionResolution,
        String scope,
        String type,
        String classifier,
        boolean optional,
        String origin
) {
}