package com.example.taskapi.service;

import com.example.taskapi.dto.*;
import com.example.taskapi.entity.*;
import com.example.taskapi.exception.*;
import com.example.taskapi.repository.TaskRepository;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import java.time.LocalDate;
import java.time.ZoneOffset;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.validation.annotation.Validated;

@Service
@Validated
@Transactional(readOnly = true)
public class TaskService {
    private final TaskRepository repository;

    public TaskService(TaskRepository repository) { this.repository = repository; }

    public Page<TaskResponse> list(Pageable pageable) {
        return repository.findAll(pageable).map(TaskResponse::from);
    }

    public Page<TaskResponse> search(String query, Pageable pageable) {
        return repository.findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
                query.trim(), query.trim(), pageable).map(TaskResponse::from);
    }

    public TaskResponse get(@Positive long id) { return TaskResponse.from(find(id)); }

    @Transactional
    public TaskResponse create(@NotNull @Valid TaskRequest request) {
        if (request.dueDate() != null && !request.dueDate().isAfter(LocalDate.now(ZoneOffset.UTC))) {
            throw new IllegalArgumentException("Due date must be in the future when creating a task (UTC)");
        }
        if (repository.existsByTitle(request.title().trim())) {
            throw new TaskConflictException("Task title already exists");
        }
        Task task = new Task();
        apply(task, request);
        return TaskResponse.from(repository.saveAndFlush(task));
    }

    @Transactional
    public TaskResponse update(@Positive long id, @NotNull @Valid TaskRequest request) {
        Task task = find(id);
        if (task.getStatus() == Status.DONE && request.status() == Status.TODO) {
            throw new TaskConflictException("Cannot change a DONE task back to TODO");
        }
        if (repository.existsByTitleAndIdNot(request.title().trim(), id)) {
            throw new TaskConflictException("Task title already exists");
        }
        apply(task, request);
        return TaskResponse.from(repository.saveAndFlush(task));
    }

    @Transactional
    public void delete(@Positive long id) {
        Task task = find(id);
        if (task.getStatus() == Status.IN_PROGRESS) {
            throw new TaskConflictException("Cannot delete an IN_PROGRESS task");
        }
        repository.delete(task);
    }

    private Task find(long id) {
        return repository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }

    private void apply(Task task, TaskRequest request) {
        task.setTitle(request.title().trim());
        task.setDescription(request.description());
        if (request.status() != null) task.setStatus(request.status());
        if (request.priority() != null) task.setPriority(request.priority());
        task.setDueDate(request.dueDate());
    }
}
