package com.example.taskapi.exception;

public class TaskNotFoundException extends RuntimeException {
    public TaskNotFoundException(long id) { super("Task " + id + " was not found"); }
}
