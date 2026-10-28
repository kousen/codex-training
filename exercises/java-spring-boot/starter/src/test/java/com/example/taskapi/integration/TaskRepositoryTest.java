package com.example.taskapi.integration;

import com.example.taskapi.entity.*;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.exception.GlobalExceptionHandler;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.dao.DataIntegrityViolationException;
import static com.example.taskapi.TaskFixtures.*;
import static org.assertj.core.api.Assertions.*;

@DataJpaTest
class TaskRepositoryTest {
    @Autowired TaskRepository repository;

    @Test void loadsSampleDataWithAllStatusesAndTimestamps() {
        assertThat(repository.findAll()).hasSize(3)
                .extracting(Task::getStatus).containsExactlyInAnyOrder(Status.values());
        assertThat(repository.findAll()).allSatisfy(task -> {
            assertThat(task.getCreatedAt()).isNotNull();
            assertThat(task.getUpdatedAt()).isNotNull();
        });
    }

    @Test void databaseEnforcesUniqueTitleAndHandlerRecognizesRealConstraint() {
        Task first = task(Status.TODO);
        repository.saveAndFlush(first);
        var failure = catchThrowableOfType(() -> repository.saveAndFlush(task(Status.DONE)),
                DataIntegrityViolationException.class);
        assertThat(failure).isNotNull();
        assertThat(new GlobalExceptionHandler().integrity(failure).getStatus()).isEqualTo(409);
    }
}
