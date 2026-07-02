package com.example.taskapi.repository;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

@DataJpaTest
class TaskRepositoryTest {

    @Autowired
    private TaskRepository taskRepository;

    @Test
    void seedDataIsLoaded() {
        assertThat(taskRepository.findAll())
                .extracting(Task::getTitle)
                .contains(
                        "Review API requirements",
                        "Implement REST controller",
                        "Write service unit tests",
                        "Document Swagger examples");
    }

    @Test
    void findByTitleIgnoreCaseMatchesRegardlessOfCase() {
        assertThat(taskRepository.findByTitleIgnoreCase("review api requirements"))
                .isPresent()
                .get()
                .extracting(Task::getStatus)
                .isEqualTo(Status.DONE);
    }

    @Test
    void searchFiltersByKeywordStatusPriorityAndDueDate() {
        assertThat(taskRepository.search(
                        "swagger",
                        Status.TODO,
                        Priority.LOW,
                        LocalDate.of(2026, 8, 31),
                        LocalDate.of(2026, 8, 1)))
                .hasSize(1)
                .first()
                .extracting(Task::getTitle)
                .isEqualTo("Document Swagger examples");
    }

    @Test
    void saveAppliesAuditingCallbacks() {
        Task task = new Task(
                "Repository callback test",
                "Verify timestamps",
                null,
                null,
                LocalDate.now().plusDays(14));

        Task saved = taskRepository.saveAndFlush(task);

        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getStatus()).isEqualTo(Status.TODO);
        assertThat(saved.getPriority()).isEqualTo(Priority.MEDIUM);
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getUpdatedAt()).isNotNull();
    }
}
