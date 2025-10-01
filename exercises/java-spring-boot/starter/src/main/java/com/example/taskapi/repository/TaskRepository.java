package com.example.taskapi.repository;

import com.example.taskapi.entity.Task;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

    Optional<Task> findByTitleIgnoreCase(String title);

    Optional<Task> findByTitleIgnoreCaseAndIdNot(String title, Long id);
}
