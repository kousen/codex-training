package com.example.taskapi.builder;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.entity.TaskPriority;
import java.time.LocalDate;

public class TaskCreateRequestBuilder {

    private String title = "New Task";
    private String description = "Do something important";
    private TaskPriority priority = TaskPriority.MEDIUM;
    private LocalDate dueDate = LocalDate.now().plusDays(3);

    public static TaskCreateRequestBuilder aTaskCreateRequest() {
        return new TaskCreateRequestBuilder();
    }

    public TaskCreateRequestBuilder withTitle(String title) {
        this.title = title;
        return this;
    }

    public TaskCreateRequestBuilder withDescription(String description) {
        this.description = description;
        return this;
    }

    public TaskCreateRequestBuilder withPriority(TaskPriority priority) {
        this.priority = priority;
        return this;
    }

    public TaskCreateRequestBuilder withDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
        return this;
    }

    public TaskCreateRequest build() {
        return new TaskCreateRequest(title, description, priority, dueDate);
    }
}
