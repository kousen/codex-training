package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.Instant;
import java.time.LocalDate;

@Schema(description = "Response representation of a task")
public record TaskResponse(
        @Schema(description = "Unique identifier", example = "1")
        Long id,

        @Schema(description = "Title of the task", example = "Finish project report")
        String title,

        @Schema(description = "Description of the task")
        String description,

        @Schema(description = "Status of the task", example = "TODO")
        TaskStatus status,

        @Schema(description = "Priority of the task", example = "MEDIUM")
        TaskPriority priority,

        @JsonFormat(pattern = "yyyy-MM-dd")
        @Schema(description = "Due date of the task", example = "2024-12-31")
        LocalDate dueDate,

        @Schema(description = "Timestamp when the task was created")
        Instant createdAt,

        @Schema(description = "Timestamp when the task was last updated")
        Instant updatedAt
) {
}
