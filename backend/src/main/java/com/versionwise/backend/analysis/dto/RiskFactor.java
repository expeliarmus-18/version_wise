package com.versionwise.backend.analysis.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public record RiskFactor(
        String ruleId,
        String name,
        int contribution,
        String explanation,
        boolean evaluated,
        String evidenceSource,
        String currentVersion,
        String targetVersion
) {
}