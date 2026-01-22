package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

@Schema(description = "Payload to create a new task.")
public record CreateTaskRequest(
        @NotBlank
        @Size(max = 100)
        @Schema(description = "Short task title", example = "Write documentation", maxLength = 100, requiredMode = Schema.RequiredMode.REQUIRED)
        String title,
        @Size(max = 500)
        @Schema(description = "Optional task details", example = "Draft API overview and usage examples", maxLength = 500)
        String description,
        @Schema(description = "Task priority, defaults to MEDIUM when omitted", example = "HIGH")
        TaskPriority priority,
        @Future
        @Schema(description = "Due date must be in the future", example = "2030-12-31")
        LocalDate dueDate
) {
}
