package com.example.taskapi.integration;

import com.example.taskapi.entity.*;
import com.example.taskapi.repository.TaskRepository;
import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.dao.*;
import org.springframework.data.domain.PageRequest;
import static com.example.taskapi.support.TaskFixtures.*;
import static org.assertj.core.api.Assertions.*;

@DataJpaTest(properties = "app.sample-data.enabled=false")
class TaskRepositoryTest {
    @Autowired TaskRepository repository;
    @Autowired EntityManager em;

    Task save(String title, String description) {
        return repository.saveAndFlush(new Task(title, description, TaskStatus.TODO, TaskPriority.MEDIUM, null, NOW));
    }

    @Test void databaseRejectsNormalizedDuplicatesWithoutServiceCheck() {
        save("  Unique Title ", null);
        assertThatThrownBy(() -> save("UNIQUE TITLE", null)).isInstanceOf(DataIntegrityViolationException.class);
    }

    @Test void findsLiteralWildcardsAndNullableDescriptions() {
        save("100% complete", null);
        save("Another task", "under_score");
        var page = PageRequest.of(0, 20);
        assertThat(repository.findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase("%", "%", page).getContent())
            .extracting(Task::getTitle).containsExactly("100% complete");
        assertThat(repository.findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase("_", "_", page).getContent())
            .extracting(Task::getTitle).containsExactly("Another task");
    }

    @Test void staleEntityCannotOverwriteNewerUpdate() {
        Task first = save("Original", null);
        em.clear();
        Task stale = repository.findById(first.getId()).orElseThrow();
        em.clear();
        first.update("Newer", null, TaskStatus.DONE, TaskPriority.HIGH, null, NOW.plusSeconds(1));
        repository.saveAndFlush(first);
        em.clear();
        stale.update("Stale", null, TaskStatus.TODO, TaskPriority.LOW, null, NOW.plusSeconds(2));
        assertThatThrownBy(() -> repository.saveAndFlush(stale)).isInstanceOf(OptimisticLockingFailureException.class);
    }
}
