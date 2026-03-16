package com.example.taskapi.repository;

import com.example.taskapi.entity.Task;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface TaskRepository extends JpaRepository<Task, Long> {

    boolean existsByTitleIgnoreCase(String title);

    boolean existsByTitleIgnoreCaseAndIdNot(String title, Long id);

    @Query("""
            select t
            from Task t
            where lower(t.title) like lower(concat('%', :query, '%'))
               or lower(coalesce(t.description, '')) like lower(concat('%', :query, '%'))
            """)
    Page<Task> search(@Param("query") String query, Pageable pageable);
}
