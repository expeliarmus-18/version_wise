package com.versionwise.backend.analysis.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public record MavenCoordinates(
        String groupId,
        String artifactId,
        String version
) {
}