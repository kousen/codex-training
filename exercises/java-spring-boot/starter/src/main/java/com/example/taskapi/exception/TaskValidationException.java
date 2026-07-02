package com.example.taskapi.exception;

public class TaskValidationException extends RuntimeException {

    public TaskValidationException(String message) {
        super(message);
    }
}
