package com.versionwise.backend.analysis.controller;

import com.versionwise.backend.analysis.dto.PomParseRequest;
import com.versionwise.backend.analysis.dto.PomParseResponse;
import com.versionwise.backend.analysis.dto.UpgradeAnalysisRequest;
import com.versionwise.backend.analysis.dto.UpgradeAnalysisResponse;
import com.versionwise.backend.analysis.dto.UpgradeAssessmentResponse;
import com.versionwise.backend.analysis.service.AnalysisService;
import jakarta.validation.Valid;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/projects/{projectId}/analysis")
public class AnalysisController {

    private final AnalysisService analysisService;

    public AnalysisController(AnalysisService analysisService) {
        this.analysisService = analysisService;
    }

    @PostMapping("/parse-pom")
    public PomParseResponse parsePom(
            @PathVariable UUID projectId,
            @Valid @RequestBody PomParseRequest request,
            @AuthenticationPrincipal Jwt jwt
    ) {

        return analysisService.parsePom(
                projectId,
                authenticatedUserId(jwt),
                request
        );
    }

    @PostMapping("/analyze-upgrade")
    public UpgradeAnalysisResponse analyzeUpgrade(
            @PathVariable UUID projectId,
            @Valid @RequestBody UpgradeAnalysisRequest request,
            @AuthenticationPrincipal Jwt jwt
    ) {

        return analysisService.analyzeUpgrade(
                projectId,
                authenticatedUserId(jwt),
                request
        );
    }

    @PostMapping("/assess-upgrade")
    public UpgradeAssessmentResponse assessUpgrade(
            @PathVariable UUID projectId,
            @Valid @RequestBody UpgradeAnalysisRequest request,
            @AuthenticationPrincipal Jwt jwt
    ) {

        return analysisService.assessUpgrade(
                projectId,
                authenticatedUserId(jwt),
                request
        );
    }

    private UUID authenticatedUserId(Jwt jwt) {

        try {
            return UUID.fromString(jwt.getClaimAsString("uid"));
        } catch (RuntimeException exception) {
            throw new IllegalStateException(
                    "Invalid authentication token"
            );
        }
    }
}