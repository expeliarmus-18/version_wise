package com.versionwise.backend.analysis.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.time.Duration;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@ConfigurationProperties(prefix = "app.ai-service")
public record AiServiceProperties(
        String baseUrl,
        Duration connectTimeout,
        Duration readTimeout
) {
}