package com.example.taskapi.service.impl;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.exception.InvalidTaskStateException;
import com.example.taskapi.exception.TaskConflictException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import com.example.taskapi.util.TaskMapper;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class TaskServiceImpl implements TaskService {

    private final TaskRepository taskRepository;
    private final Clock clock;

    @Autowired
    public TaskServiceImpl(TaskRepository taskRepository, Clock clock) {
        this.taskRepository = taskRepository;
        this.clock = clock;
    }

    @Override
    public TaskResponse createTask(TaskCreateRequest request) {
        String normalizedTitle = normalizeTitle(request.title());
        validateTitleUniqueness(normalizedTitle);
        validateDueDate(request.dueDate());

        Task task = new Task();
        Instant now = Instant.now(clock);
        task.setTitle(normalizedTitle);
        task.setDescription(request.description());
        task.setPriority(Optional.ofNullable(request.priority()).orElse(TaskPriority.MEDIUM));
        task.setStatus(TaskStatus.TODO);
        task.setDueDate(request.dueDate());
        task.setCreatedAt(now);
        task.setUpdatedAt(now);

        Task saved = taskRepository.save(task);
        return TaskMapper.toResponse(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<TaskResponse> getTasks(Pageable pageable) {
        return taskRepository.findAll(pageable)
                .map(TaskMapper::toResponse);
    }

    @Override
    @Transactional(readOnly = true)
    public TaskResponse getTask(Long id) {
        Task task = getTaskOrThrow(id);
        return TaskMapper.toResponse(task);
    }

    @Override
    public TaskResponse updateTask(Long id, TaskUpdateRequest request) {
        Task task = getTaskOrThrow(id);

        String normalizedTitle = normalizeTitle(request.title());
        validateTitleUniquenessForUpdate(normalizedTitle, id);
        validateStatusTransition(task.getStatus(), request.status());
        validateDueDate(request.dueDate());

        task.setTitle(normalizedTitle);
        task.setDescription(request.description());
        task.setPriority(Optional.ofNullable(request.priority()).orElse(TaskPriority.MEDIUM));
        if (request.status() != null) {
            task.setStatus(request.status());
        }
        task.setDueDate(request.dueDate());
        task.setUpdatedAt(Instant.now(clock));

        Task updated = taskRepository.save(task);
        return TaskMapper.toResponse(updated);
    }

    @Override
    public void deleteTask(Long id) {
        Task task = getTaskOrThrow(id);
        if (TaskStatus.IN_PROGRESS.equals(task.getStatus())) {
            throw new InvalidTaskStateException("Cannot delete task in progress");
        }
        taskRepository.delete(task);
    }

    private String normalizeTitle(String title) {
        return title == null ? null : title.trim();
    }

    private void validateTitleUniqueness(String title) {
        taskRepository.findByTitleIgnoreCase(title)
                .ifPresent(existing -> {
                    throw new TaskConflictException("Task title must be unique");
                });
    }

    private void validateTitleUniquenessForUpdate(String title, Long id) {
        taskRepository.findByTitleIgnoreCaseAndIdNot(title, id)
                .ifPresent(existing -> {
                    throw new TaskConflictException("Task title must be unique");
                });
    }

    private void validateStatusTransition(TaskStatus currentStatus, TaskStatus requestedStatus) {
        if (currentStatus == TaskStatus.DONE && requestedStatus == TaskStatus.TODO) {
            throw new InvalidTaskStateException("Cannot change a completed task back to TODO");
        }
    }

    private void validateDueDate(LocalDate dueDate) {
        if (dueDate != null && !dueDate.isAfter(LocalDate.now(clock))) {
            throw new InvalidTaskStateException("Due date must be in the future");
        }
    }

    private Task getTaskOrThrow(Long id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new TaskNotFoundException(id));
    }
}
