package com.versionwise.backend.analysis.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record PomParseResponse(
        MavenCoordinates project,
        MavenCoordinates parent,
        List<MavenDependency> dependencies,
        List<MavenDependency> managedDependencies,
        List<String> warnings
) {
}