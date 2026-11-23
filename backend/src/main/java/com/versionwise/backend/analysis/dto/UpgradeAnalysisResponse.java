package com.versionwise.backend.analysis.dto;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;
@JsonIgnoreProperties(ignoreUnknown = true)
public record UpgradeAnalysisResponse(
        String groupId,
        String artifactId,
        String currentVersion,
        String targetVersion,
        String comparison,
        int riskScore,
        String riskCategory,
        List<RiskFactor> factors,
        List<String> warnings,
        List<String> recommendations,
        boolean scoreIsProbability
) {
}