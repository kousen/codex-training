package com.example.taskapi.builder;

import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import java.time.LocalDate;

public class TaskUpdateRequestBuilder {

    private String title = "Updated Task";
    private String description = "Updated description";
    private TaskStatus status = TaskStatus.IN_PROGRESS;
    private TaskPriority priority = TaskPriority.HIGH;
    private LocalDate dueDate = LocalDate.now().plusDays(5);

    public static TaskUpdateRequestBuilder aTaskUpdateRequest() {
        return new TaskUpdateRequestBuilder();
    }

    public TaskUpdateRequestBuilder withTitle(String title) {
        this.title = title;
        return this;
    }

    public TaskUpdateRequestBuilder withDescription(String description) {
        this.description = description;
        return this;
    }

    public TaskUpdateRequestBuilder withStatus(TaskStatus status) {
        this.status = status;
        return this;
    }

    public TaskUpdateRequestBuilder withPriority(TaskPriority priority) {
        this.priority = priority;
        return this;
    }

    public TaskUpdateRequestBuilder withDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
        return this;
    }

    public TaskUpdateRequest build() {
        return new TaskUpdateRequest(title, description, status, priority, dueDate);
    }
}
