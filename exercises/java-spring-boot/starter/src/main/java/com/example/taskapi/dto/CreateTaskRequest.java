package com.example.taskapi.dto;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

@Schema(description = "Request body for creating a task")
public record CreateTaskRequest(
        @Schema(description = "Unique task title", example = "Prepare workshop materials")
        @NotBlank(message = "Task title is required")
        @Size(max = 100, message = "Task title must be 100 characters or fewer")
        String title,

        @Schema(description = "Optional task details", example = "Update slides and verify lab instructions")
        @Size(max = 500, message = "Task description must be 500 characters or fewer")
        String description,

        @Schema(description = "Initial task status. Defaults to TODO when omitted", example = "TODO")
        Status status,

        @Schema(description = "Initial task priority. Defaults to MEDIUM when omitted", example = "HIGH")
        Priority priority,

        @Schema(description = "Optional future due date", example = "2026-08-15")
        @Future(message = "Due date must be in the future")
        LocalDate dueDate) {
}
