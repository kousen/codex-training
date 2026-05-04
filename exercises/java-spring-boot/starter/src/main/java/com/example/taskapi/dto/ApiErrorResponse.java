package com.example.taskapi.dto;

import java.time.Instant;
import java.util.Map;

public record ApiErrorResponse(
        Instant timestamp,
        int status,
        String error,
        String message,
        String path,
        Map<String, String> validationErrors) {

    public static ApiErrorResponse of(int status, String error, String message, String path) {
        return new ApiErrorResponse(Instant.now(), status, error, message, path, Map.of());
    }

    public static ApiErrorResponse validation(String message, String path, Map<String, String> validationErrors) {
        return new ApiErrorResponse(Instant.now(), 400, "Bad Request", message, path, validationErrors);
    }
}
