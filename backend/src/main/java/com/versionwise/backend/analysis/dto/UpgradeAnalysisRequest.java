package com.versionwise.backend.analysis.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record UpgradeAnalysisRequest(

        @NotBlank
        @Size(max = 300)
        String groupId,

        @NotBlank
        @Size(max = 300)
        String artifactId,

        @NotBlank
        @Size(max = 200)
        String currentVersion,

        @NotBlank
        @Size(max = 200)
        String targetVersion,

        @Size(max = 50)
        String scope,

        @Size(max = 100)
        String type,

        @Size(max = 200)
        String classifier,

        String versionResolution,

        Boolean metadataAvailable,

        // Optional context is forwarded only by the AI assessment request.
        // The frontend deliberately omits this field from analyze-upgrade.
        PomParseResponse projectContext
) {
}
