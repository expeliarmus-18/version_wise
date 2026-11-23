package com.versionwise.backend.analysis.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class AnalysisExceptionHandler {

    @ExceptionHandler(AiServiceException.class)
    public ProblemDetail handleAiServiceException(
            AiServiceException exception
    ) {

        ProblemDetail problemDetail = ProblemDetail.forStatusAndDetail(
                exception.getStatusCode(),
                exception.getMessage()
        );

        problemDetail.setTitle("AI Service Error");

        return problemDetail;
    }
}