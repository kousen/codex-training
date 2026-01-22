package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.Instant;
import java.time.LocalDate;

@Schema(description = "Task representation returned by the API.")
public record TaskResponse(
        @Schema(description = "Task identifier", example = "1")
        Long id,
        @Schema(description = "Task title", example = "Plan sprint")
        String title,
        @Schema(description = "Task description", example = "Create backlog and confirm scope")
        String description,
        @Schema(description = "Task status", example = "TODO")
        TaskStatus status,
        @Schema(description = "Task priority", example = "MEDIUM")
        TaskPriority priority,
        @Schema(description = "Due date", example = "2030-06-30")
        LocalDate dueDate,
        @Schema(description = "Creation timestamp", example = "2030-01-01T10:15:30Z")
        Instant createdAt,
        @Schema(description = "Last update timestamp", example = "2030-01-02T08:00:00Z")
        Instant updatedAt
) {
}
