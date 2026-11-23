package com.versionwise.backend.analysis.service;

import com.versionwise.backend.analysis.client.AiServiceClient;
import com.versionwise.backend.analysis.dto.PomParseRequest;
import com.versionwise.backend.analysis.dto.PomParseResponse;
import com.versionwise.backend.analysis.dto.UpgradeAnalysisRequest;
import com.versionwise.backend.analysis.dto.UpgradeAnalysisResponse;
import com.versionwise.backend.analysis.dto.UpgradeAssessmentResponse;
import com.versionwise.backend.service.ProjectService;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class AnalysisService {

    private final AiServiceClient aiServiceClient;
    private final ProjectService projectService;

    public AnalysisService(
            AiServiceClient aiServiceClient,
            ProjectService projectService
    ) {
        this.aiServiceClient = aiServiceClient;
        this.projectService = projectService;
    }

    public PomParseResponse parsePom(
            UUID projectId,
            UUID userId,
            PomParseRequest request
    ) {

        validateProjectOwnership(projectId, userId);

        return aiServiceClient.parsePom(request);
    }

    public UpgradeAnalysisResponse analyzeUpgrade(
            UUID projectId,
            UUID userId,
            UpgradeAnalysisRequest request
    ) {

        validateProjectOwnership(projectId, userId);

        return aiServiceClient.analyzeUpgrade(request);
    }

    public UpgradeAssessmentResponse assessUpgrade(
            UUID projectId,
            UUID userId,
            UpgradeAnalysisRequest request
    ) {

        validateProjectOwnership(projectId, userId);

        return aiServiceClient.assessUpgrade(request);
    }

    private void validateProjectOwnership(
            UUID projectId,
            UUID userId
    ) {

        projectService.getProject(projectId, userId);
    }
}