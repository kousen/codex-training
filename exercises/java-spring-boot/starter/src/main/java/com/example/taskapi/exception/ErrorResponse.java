package com.example.taskapi.exception;

import io.swagger.v3.oas.annotations.media.Schema;
import java.time.Instant;

@Schema(description = "Standard error response.")
public class ErrorResponse {

    @Schema(description = "Time of the error", example = "2030-01-01T12:00:00Z")
    private Instant timestamp;
    @Schema(description = "HTTP status code", example = "404")
    private int status;
    @Schema(description = "HTTP status description", example = "Not Found")
    private String error;
    @Schema(description = "Human-readable error message", example = "Task not found")
    private String message;
    @Schema(description = "Request path", example = "/api/v1/tasks/99")
    private String path;

    public ErrorResponse() {
    }

    public ErrorResponse(Instant timestamp, int status, String error, String message, String path) {
        this.timestamp = timestamp;
        this.status = status;
        this.error = error;
        this.message = message;
        this.path = path;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }
}
