package com.example.taskapi.exception;

public class DuplicateTaskTitleException extends RuntimeException {

    public DuplicateTaskTitleException(String title) {
        super("Task title already exists: " + title);
    }
}
