package com.versionwise.backend.analysis.dto;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record PomParseRequest(
        @NotBlank
        @Size(max = 2_000_000)
        String pomXml
) {
}