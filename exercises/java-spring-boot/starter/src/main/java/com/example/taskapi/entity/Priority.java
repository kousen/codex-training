package com.example.taskapi.entity;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Task priority", allowableValues = {"LOW", "MEDIUM", "HIGH"})
public enum Priority {
    LOW,
    MEDIUM,
    HIGH
}
