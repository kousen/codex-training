package com.example.taskapi.exception;

public class TaskConflictException extends RuntimeException {

    public TaskConflictException(String message) {
        super(message);
    }
}
