package com.example.taskapi.repository;

import com.example.taskapi.entity.Task;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TaskRepository extends JpaRepository<Task, Long> {
    boolean existsByTitleKey(String titleKey);
    boolean existsByTitleKeyAndIdNot(String titleKey, Long id);
    Page<Task> findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
        String title, String description, Pageable pageable);
}
