package com.versionwise.backend.analysis.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;


@JsonIgnoreProperties(ignoreUnknown = true)
public record AssessmentEvidence(
        String sourceTitle,
        String sourceUri,
        String excerpt,
        String retrievalTimestamp
) {
}