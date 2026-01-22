package com.example.taskapi.entity;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Priority of a task.")
public enum TaskPriority {
    LOW,
    MEDIUM,
    HIGH
}
