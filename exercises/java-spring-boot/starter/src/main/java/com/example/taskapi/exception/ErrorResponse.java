package com.example.taskapi.exception;

import io.swagger.v3.oas.annotations.media.Schema;
import java.time.Instant;
import java.util.Map;

@Schema(description = "Standard API error response")
public record ErrorResponse(
        @Schema(description = "Time the error response was generated", example = "2026-07-01T14:30:00Z")
        Instant timestamp,

        @Schema(description = "HTTP status code", example = "400")
        int status,

        @Schema(description = "HTTP reason phrase", example = "Bad Request")
        String error,

        @Schema(description = "Human-readable error message", example = "Validation failed")
        String message,

        @Schema(description = "Request path that produced the error", example = "/api/v1/tasks")
        String path,

        @Schema(
                description = "Field-specific validation errors, present for request validation failures",
                example = "{\"title\":\"Task title is required\"}")
        Map<String, String> validationErrors) {

    public static ErrorResponse of(int status, String error, String message, String path) {
        return new ErrorResponse(Instant.now(), status, error, message, path, Map.of());
    }

    public static ErrorResponse withValidationErrors(
            int status, String error, String message, String path, Map<String, String> validationErrors) {
        return new ErrorResponse(Instant.now(), status, error, message, path, validationErrors);
    }
}
