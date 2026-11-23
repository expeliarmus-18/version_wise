package com.versionwise.backend.analysis.dto;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;
@JsonIgnoreProperties(ignoreUnknown = true)
public record UpgradeAssessmentResponse(
        String status,
        String summary,
        List<AssessmentFinding> compatibilityFindings,
        List<AssessmentFinding> breakingChanges,
        List<AssessmentFinding> migrationConcerns,
        List<AssessmentFinding> securityFindings,
        List<AssessmentEvidence> evidence,
        List<String> limitations
) {
}