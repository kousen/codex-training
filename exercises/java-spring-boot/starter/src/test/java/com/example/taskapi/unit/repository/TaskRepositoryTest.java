package com.example.taskapi.unit.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.repository.TaskRepository;
import java.time.Instant;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

@DataJpaTest
class TaskRepositoryTest {

    @Autowired
    private TaskRepository taskRepository;

    @Test
    void shouldFindByTitleIgnoreCase() {
        assertThat(taskRepository.findByTitleIgnoreCase("initial project setup")).isPresent();
    }

    @Test
    void shouldReturnEmptyWhenTitleDoesNotExist() {
        assertThat(taskRepository.findByTitleIgnoreCase("missing title")).isEmpty();
    }

    @Test
    void shouldFindByTitleIgnoreCaseAndIdNot() {
        Task task = new Task();
        task.setTitle("Repository Unique Title");
        task.setDescription("Repository test");
        task.setStatus(TaskStatus.TODO);
        task.setPriority(TaskPriority.MEDIUM);
        task.setDueDate(LocalDate.now().plusDays(5));
        task.setCreatedAt(Instant.now());
        task.setUpdatedAt(Instant.now());

        Task saved = taskRepository.save(task);

        assertThat(taskRepository.findByTitleIgnoreCaseAndIdNot("Repository Unique Title", saved.getId()))
                .isEmpty();
        assertThat(taskRepository.findByTitleIgnoreCaseAndIdNot("Repository Unique Title", saved.getId() + 1))
                .isPresent();
    }
}
