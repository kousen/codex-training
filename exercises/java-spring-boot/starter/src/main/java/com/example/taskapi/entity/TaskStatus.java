package com.example.taskapi.entity;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Lifecycle status of a task.")
public enum TaskStatus {
    TODO,
    IN_PROGRESS,
    DONE
}
