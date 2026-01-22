package com.example.taskapi.repository;

import com.example.taskapi.entity.Task;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TaskRepository extends JpaRepository<Task, Long> {
    boolean existsByTitle(String title);
}
