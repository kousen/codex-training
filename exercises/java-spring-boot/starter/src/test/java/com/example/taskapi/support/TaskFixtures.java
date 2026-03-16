package com.example.taskapi.support;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;

import java.time.Instant;
import java.time.LocalDate;

public final class TaskFixtures {

    private TaskFixtures() {
    }

    public static Task task(Long id, String title, Status status, Priority priority) {
        Task task = new Task();
        task.setId(id);
        task.setTitle(title);
        task.setDescription("Description for " + title);
        task.setStatus(status);
        task.setPriority(priority);
        task.setDueDate(LocalDate.now().plusDays(5));
        task.setCreatedAt(Instant.parse("2026-01-01T10:00:00Z"));
        task.setUpdatedAt(Instant.parse("2026-01-02T10:00:00Z"));
        return task;
    }

    public static TaskCreateRequest createRequest(String title) {
        return new TaskCreateRequest(
                title,
                "Create request description",
                null,
                null,
                LocalDate.now().plusDays(10)
        );
    }

    public static TaskUpdateRequest updateRequest(String title, Status status, Priority priority) {
        return new TaskUpdateRequest(
                title,
                "Updated description",
                status,
                priority,
                LocalDate.now().plusDays(12)
        );
    }
}
