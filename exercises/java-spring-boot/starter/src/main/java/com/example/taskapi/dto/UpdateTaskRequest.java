package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

@Schema(description = "Payload to update an existing task. All fields are optional.")
public record UpdateTaskRequest(
        @Size(max = 100)
        @Schema(description = "Updated task title", example = "Ship v1", maxLength = 100)
        String title,
        @Size(max = 500)
        @Schema(description = "Updated task details", example = "Finalize and release the first version", maxLength = 500)
        String description,
        @Schema(description = "Updated task status", example = "IN_PROGRESS")
        TaskStatus status,
        @Schema(description = "Updated task priority", example = "LOW")
        TaskPriority priority,
        @Future
        @Schema(description = "Updated due date must be in the future", example = "2031-01-15")
        LocalDate dueDate
) {
}
