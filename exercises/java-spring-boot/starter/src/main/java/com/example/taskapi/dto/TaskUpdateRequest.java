package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

@Schema(description = "Request payload for updating a task")
public record TaskUpdateRequest(
        @NotBlank
        @Size(max = 100)
        @Schema(description = "Updated title of the task", example = "Finalize project report")
        String title,

        @Size(max = 500)
        @Schema(description = "Updated description of the task", example = "Gather data from all departments")
        String description,

        @Schema(description = "Updated task status", example = "IN_PROGRESS")
        TaskStatus status,

        @Schema(description = "Updated task priority", example = "MEDIUM")
        TaskPriority priority,

        @Future(message = "Due date must be in the future")
        @JsonFormat(pattern = "yyyy-MM-dd")
        @Schema(description = "Updated due date in ISO format", example = "2025-01-15")
        LocalDate dueDate
) {
}
