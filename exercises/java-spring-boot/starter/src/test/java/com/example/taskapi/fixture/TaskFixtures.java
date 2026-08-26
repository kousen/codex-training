package com.example.taskapi.fixture;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.UpdateTaskRequest;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import org.springframework.test.util.ReflectionTestUtils;

import java.time.Instant;
import java.time.LocalDate;

public final class TaskFixtures {

    private TaskFixtures() {
    }

    public static Task task(Long id, Status status) {
        Task task = new Task(
                "Prepare release",
                "Complete the release checklist",
                status,
                Priority.HIGH,
                LocalDate.now().plusDays(5)
        );
        ReflectionTestUtils.setField(task, "id", id);
        ReflectionTestUtils.setField(task, "createdAt", Instant.parse("2026-01-01T12:00:00Z"));
        ReflectionTestUtils.setField(task, "updatedAt", Instant.parse("2026-01-01T12:00:00Z"));
        return task;
    }

    public static CreateTaskRequest createRequest(String title) {
        return new CreateTaskRequest(
                title,
                "A new task",
                null,
                null,
                LocalDate.now().plusDays(2)
        );
    }

    public static UpdateTaskRequest updateRequest(Status status) {
        return new UpdateTaskRequest(
                "Prepare release",
                "Updated checklist",
                status,
                Priority.MEDIUM,
                LocalDate.now().plusDays(7)
        );
    }
}
