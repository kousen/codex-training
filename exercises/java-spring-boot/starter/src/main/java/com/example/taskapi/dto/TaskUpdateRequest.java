package com.example.taskapi.dto;

import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

public record TaskUpdateRequest(
        @NotBlank(message = "Title is required") @Size(max = 100, message = "Title must be 100 characters or fewer")
                String title,
        @Size(max = 500, message = "Description must be 500 characters or fewer") String description,
        @NotNull(message = "Status is required") TaskStatus status,
        @NotNull(message = "Priority is required") TaskPriority priority,
        @Future(message = "Due date must be in the future") LocalDate dueDate) {}
