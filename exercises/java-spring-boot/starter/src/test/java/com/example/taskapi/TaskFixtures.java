package com.example.taskapi;

import com.example.taskapi.dto.TaskRequest;
import com.example.taskapi.entity.*;
import java.time.LocalDate;

public final class TaskFixtures {
    private TaskFixtures() {}

    public static TaskRequest request(String title, Status status) {
        return new TaskRequest(title, "Sample description", status, Priority.HIGH, LocalDate.now().plusDays(7));
    }

    public static Task task(Status status) {
        Task task = new Task();
        task.setTitle("Sample task");
        task.setDescription("Sample description");
        task.setStatus(status);
        return task;
    }
}
