package com.example.taskapi.entity;

import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

import java.time.Instant;

import static org.assertj.core.api.Assertions.assertThat;

class TaskTest {

    @Test
    void appliesPersistenceDefaultsAndTimestamps() {
        Task task = new Task("New task", null, null, null, null);

        task.onCreate();

        assertThat(task.getStatus()).isEqualTo(Status.TODO);
        assertThat(task.getPriority()).isEqualTo(Priority.MEDIUM);
        assertThat(task.getCreatedAt()).isNotNull();
        assertThat(task.getUpdatedAt()).isEqualTo(task.getCreatedAt());
    }

    @Test
    void refreshesUpdatedTimestamp() {
        Task task = new Task("New task", null, Status.TODO, Priority.LOW, null);
        ReflectionTestUtils.setField(task, "updatedAt", Instant.EPOCH);

        task.onUpdate();

        assertThat(task.getUpdatedAt()).isAfter(Instant.EPOCH);
    }
}
