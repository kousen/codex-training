package com.example.taskapi.fixture;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import java.time.Instant;
import java.time.LocalDate;

public final class TaskTestData {

    private TaskTestData() {}

    public static Task task(Long id, String title, TaskStatus status) {
        Task task = new Task();
        task.setId(id);
        task.setTitle(title);
        task.setDescription(title + " description");
        task.setStatus(status);
        task.setPriority(TaskPriority.MEDIUM);
        task.setDueDate(LocalDate.now().plusDays(5));
        task.setCreatedAt(Instant.parse("2026-05-04T12:00:00Z"));
        task.setUpdatedAt(Instant.parse("2026-05-04T12:00:00Z"));
        return task;
    }

    public static TaskCreateRequest createRequest(String title) {
        return new TaskCreateRequest(title, title + " description", null, LocalDate.now().plusDays(5));
    }

    public static TaskUpdateRequest updateRequest(String title, TaskStatus status) {
        return new TaskUpdateRequest(
                title, title + " updated description", status, TaskPriority.HIGH, LocalDate.now().plusDays(10));
    }
}
