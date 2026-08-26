package com.example.taskapi.service;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.UpdateTaskRequest;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.BusinessRuleException;
import com.example.taskapi.exception.DuplicateTaskTitleException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

@Service
@Transactional
public class TaskService {

    private final TaskRepository taskRepository;

    public TaskService(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> findAll(Pageable pageable) {
        return taskRepository.findAll(pageable).map(this::toResponse);
    }

    @Transactional(readOnly = true)
    public TaskResponse findById(Long id) {
        return toResponse(getTask(id));
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> search(String query, Pageable pageable) {
        String normalizedQuery = query.trim();
        return taskRepository
                .findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
                        normalizedQuery,
                        normalizedQuery,
                        pageable
                )
                .map(this::toResponse);
    }

    public TaskResponse create(CreateTaskRequest request) {
        String title = normalizeTitle(request.title());
        ensureUniqueTitle(title);
        ensureFutureDueDate(request.dueDate());

        Task task = new Task(
                title,
                request.description(),
                request.status() == null ? Status.TODO : request.status(),
                request.priority() == null ? Priority.MEDIUM : request.priority(),
                request.dueDate()
        );
        return toResponse(taskRepository.saveAndFlush(task));
    }

    public TaskResponse update(Long id, UpdateTaskRequest request) {
        Task task = getTask(id);
        String title = normalizeTitle(request.title());

        if (taskRepository.existsByTitleIgnoreCaseAndIdNot(title, id)) {
            throw new DuplicateTaskTitleException(title);
        }
        if (task.getStatus() == Status.DONE && request.status() == Status.TODO) {
            throw new BusinessRuleException("A DONE task cannot be changed back to TODO");
        }

        task.setTitle(title);
        task.setDescription(request.description());
        task.setStatus(request.status());
        task.setPriority(request.priority());
        task.setDueDate(request.dueDate());

        return toResponse(taskRepository.saveAndFlush(task));
    }

    public void delete(Long id) {
        Task task = getTask(id);
        if (task.getStatus() == Status.IN_PROGRESS) {
            throw new BusinessRuleException("An IN_PROGRESS task cannot be deleted");
        }
        taskRepository.delete(task);
    }

    private Task getTask(Long id) {
        return taskRepository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }

    private void ensureUniqueTitle(String title) {
        if (taskRepository.existsByTitleIgnoreCase(title)) {
            throw new DuplicateTaskTitleException(title);
        }
    }

    private String normalizeTitle(String title) {
        return title.trim();
    }

    private void ensureFutureDueDate(LocalDate dueDate) {
        if (dueDate != null && !dueDate.isAfter(LocalDate.now())) {
            throw new BusinessRuleException("Due date must be in the future");
        }
    }

    private TaskResponse toResponse(Task task) {
        return new TaskResponse(
                task.getId(),
                task.getTitle(),
                task.getDescription(),
                task.getStatus(),
                task.getPriority(),
                task.getDueDate(),
                task.getCreatedAt(),
                task.getUpdatedAt()
        );
    }
}
