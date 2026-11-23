package com.versionwise.backend.analysis.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;


@JsonIgnoreProperties(ignoreUnknown = true)
public record AssessmentFinding(
        String title,
        String description,
        String severity,
        List<String> evidenceIds
) {
}