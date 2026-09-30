package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

public record UpdateTaskRequest(
    @NotBlank @Size(max = 100) String title,
    @Size(max = 500) String description,
    @NotNull TaskStatus status,
    @NotNull TaskPriority priority,
    LocalDate dueDate
) { }
