package com.example.taskapi.dto;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

@Schema(description = "Request body for updating a task. Omitted fields are left unchanged")
public record UpdateTaskRequest(
        @Schema(description = "New unique task title", example = "Prepare final workshop materials")
        @Size(max = 100, message = "Task title must be 100 characters or fewer")
        String title,

        @Schema(description = "New task details", example = "Finalize slides and verify every lab")
        @Size(max = 500, message = "Task description must be 500 characters or fewer")
        String description,

        @Schema(description = "New task status", example = "IN_PROGRESS")
        Status status,

        @Schema(description = "New task priority", example = "MEDIUM")
        Priority priority,

        @Schema(description = "New future due date", example = "2026-08-20")
        @Future(message = "Due date must be in the future")
        LocalDate dueDate) {
}
