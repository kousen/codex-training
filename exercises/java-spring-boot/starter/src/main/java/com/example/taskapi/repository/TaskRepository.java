package com.example.taskapi.repository;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface TaskRepository extends JpaRepository<Task, Long> {

    Optional<Task> findByTitleIgnoreCase(String title);

    boolean existsByTitleIgnoreCase(String title);

    List<Task> findByStatus(Status status);

    List<Task> findByPriority(Priority priority);

    List<Task> findByStatusAndPriority(Status status, Priority priority);

    List<Task> findByDueDateBefore(LocalDate dueDate);

    List<Task> findByDueDateBetween(LocalDate startDate, LocalDate endDate);

    List<Task> findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
            String titleKeyword, String descriptionKeyword);

    @Query("""
            select task
            from Task task
            where (:keyword is null
                or lower(task.title) like lower(concat('%', :keyword, '%'))
                or lower(task.description) like lower(concat('%', :keyword, '%')))
              and (:status is null or task.status = :status)
              and (:priority is null or task.priority = :priority)
              and (:dueBefore is null or task.dueDate <= :dueBefore)
              and (:dueAfter is null or task.dueDate >= :dueAfter)
            order by task.dueDate asc nulls last, task.createdAt desc
            """)
    List<Task> search(
            @Param("keyword") String keyword,
            @Param("status") Status status,
            @Param("priority") Priority priority,
            @Param("dueBefore") LocalDate dueBefore,
            @Param("dueAfter") LocalDate dueAfter);
}
