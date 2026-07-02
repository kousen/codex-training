package com.example.taskapi.entity;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Task workflow status", allowableValues = {"TODO", "IN_PROGRESS", "DONE"})
public enum Status {
    TODO,
    IN_PROGRESS,
    DONE
}
