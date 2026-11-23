package com.versionwise.backend.analysis.client;

import com.versionwise.backend.analysis.dto.PomParseRequest;
import com.versionwise.backend.analysis.dto.PomParseResponse;
import com.versionwise.backend.analysis.dto.UpgradeAnalysisRequest;
import com.versionwise.backend.analysis.dto.UpgradeAnalysisResponse;
import com.versionwise.backend.analysis.dto.UpgradeAssessmentResponse;
import com.versionwise.backend.analysis.exception.AiServiceException;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

@Component
public class AiServiceClient {

    private final RestClient restClient;

    public AiServiceClient(RestClient aiServiceRestClient) {
        this.restClient = aiServiceRestClient;
    }

    public PomParseResponse parsePom(PomParseRequest request) {

        return post(
                "/api/v1/parse-pom",
                request,
                PomParseResponse.class
        );
    }

    public UpgradeAnalysisResponse analyzeUpgrade(
            UpgradeAnalysisRequest request
    ) {

        return post(
                "/api/v1/analyze-upgrade",
                request,
                UpgradeAnalysisResponse.class
        );
    }

    public UpgradeAssessmentResponse assessUpgrade(
            UpgradeAnalysisRequest request
    ) {

        return post(
                "/api/v1/assess-upgrade",
                request,
                UpgradeAssessmentResponse.class
        );
    }

    private <T> T post(
            String endpoint,
            Object request,
            Class<T> responseType
    ) {

        try {

            return restClient.post()
                    .uri(endpoint)
                    .body(request)
                    .retrieve()
                    .onStatus(
                            status -> status.isError(),
                            (httpRequest, response) -> {
                                throw new AiServiceException(
                                        "AI service request failed",
                                        response.getStatusCode()
                                );
                            }
                    )
                    .body(responseType);

        } catch (AiServiceException exception) {

            throw exception;

        } catch (RestClientException exception) {

            throw new AiServiceException(
                    "AI service is currently unavailable",
                    org.springframework.http.HttpStatus.SERVICE_UNAVAILABLE,
                    exception
            );
        }
    }
}