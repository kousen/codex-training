package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

@Schema(description = "Request payload for creating a task")
public record TaskCreateRequest(
        @NotBlank
        @Size(max = 100)
        @Schema(description = "Unique title of the task", example = "Finish project report")
        String title,

        @Size(max = 500)
        @Schema(description = "Detailed description of the task", example = "Compile the Q4 financial summary")
        String description,

        @Schema(description = "Task priority", example = "HIGH")
        TaskPriority priority,

        @Future(message = "Due date must be in the future")
        @JsonFormat(pattern = "yyyy-MM-dd")
        @Schema(description = "Due date in ISO format", example = "2024-12-31")
        LocalDate dueDate
) {
}
