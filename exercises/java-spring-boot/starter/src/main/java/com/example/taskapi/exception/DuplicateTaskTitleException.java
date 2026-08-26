package com.example.taskapi.exception;

public class DuplicateTaskTitleException extends RuntimeException {

    public DuplicateTaskTitleException(String title) {
        super("A task with title '" + title + "' already exists");
    }
}
