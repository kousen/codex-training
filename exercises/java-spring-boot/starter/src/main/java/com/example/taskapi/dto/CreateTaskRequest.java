package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

public record CreateTaskRequest(
    @NotBlank @Size(max = 100) @Schema(example = "Prepare workshop") String title,
    @Size(max = 500) String description,
    @Schema(defaultValue = "TODO") TaskStatus status,
    @Schema(defaultValue = "MEDIUM") TaskPriority priority,
    @Schema(description = "Optional; must be after today's date in UTC") LocalDate dueDate
) { }
