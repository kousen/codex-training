package com.example.taskapi.support;

import com.example.taskapi.dto.*;
import com.example.taskapi.entity.*;
import java.time.*;
import org.springframework.test.util.ReflectionTestUtils;

public final class TaskFixtures {
    public static final Instant NOW = Instant.parse("2030-06-15T12:00:00Z");
    public static final Clock CLOCK = Clock.fixed(NOW, ZoneOffset.UTC);
    private TaskFixtures() { }

    public static Task task(long id, String title, TaskStatus status) {
        Task task = new Task(title, "Description", status, TaskPriority.MEDIUM,
            LocalDate.of(2030, 6, 16), NOW.minusSeconds(60));
        ReflectionTestUtils.setField(task, "id", id);
        return task;
    }

    public static CreateTaskRequest create(String title) {
        return new CreateTaskRequest(title, "Description", null, null, null);
    }

    public static UpdateTaskRequest update(String title, TaskStatus status) {
        return new UpdateTaskRequest(title, "Updated description", status, TaskPriority.HIGH, null);
    }
}
