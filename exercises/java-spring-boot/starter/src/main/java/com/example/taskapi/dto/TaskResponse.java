package com.example.taskapi.dto;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.Instant;
import java.time.LocalDate;

@Schema(description = "Task resource returned by the API")
public record TaskResponse(
        @Schema(description = "Task identifier", example = "1")
        Long id,

        @Schema(description = "Unique task title", example = "Prepare workshop materials")
        String title,

        @Schema(description = "Optional task details", example = "Update slides and verify lab instructions")
        String description,

        @Schema(description = "Current task status", example = "TODO")
        Status status,

        @Schema(description = "Current task priority", example = "HIGH")
        Priority priority,

        @Schema(description = "Optional due date", example = "2026-08-15")
        LocalDate dueDate,

        @Schema(description = "Creation timestamp", example = "2026-07-01T14:30:00Z")
        Instant createdAt,

        @Schema(description = "Last update timestamp", example = "2026-07-01T15:45:00Z")
        Instant updatedAt) {
}
