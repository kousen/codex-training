package com.example.taskapi.service;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.BusinessRuleViolationException;
import com.example.taskapi.exception.InvalidRequestException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
@Transactional
public class TaskService {

    private static final List<String> ALLOWED_SORT_FIELDS = List.of(
            "id",
            "title",
            "status",
            "priority",
            "dueDate",
            "createdAt",
            "updatedAt"
    );

    private final TaskRepository taskRepository;

    public TaskService(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> getAllTasks(Pageable pageable) {
        return taskRepository.findAll(normalizePageable(pageable)).map(TaskResponse::fromEntity);
    }

    @Transactional(readOnly = true)
    public TaskResponse getTaskById(Long id) {
        return TaskResponse.fromEntity(findTask(id));
    }

    public TaskResponse createTask(TaskCreateRequest request) {
        String normalizedTitle = normalizeTitle(request.title());
        validateUniqueTitle(normalizedTitle, null);
        validateDueDate(request.dueDate());

        Task task = new Task();
        task.setTitle(normalizedTitle);
        task.setDescription(normalizeDescription(request.description()));
        task.setStatus(request.status() != null ? request.status() : Status.TODO);
        task.setPriority(request.priority() != null ? request.priority() : Priority.MEDIUM);
        task.setDueDate(request.dueDate());

        return TaskResponse.fromEntity(taskRepository.save(task));
    }

    public TaskResponse updateTask(Long id, TaskUpdateRequest request) {
        Task task = findTask(id);
        String normalizedTitle = normalizeTitle(request.title());

        validateUniqueTitle(normalizedTitle, id);
        validateDueDate(request.dueDate());

        Status nextStatus = request.status() != null ? request.status() : task.getStatus();
        if (task.getStatus() == Status.DONE && nextStatus == Status.TODO) {
            throw new BusinessRuleViolationException("A DONE task cannot be moved back to TODO");
        }

        task.setTitle(normalizedTitle);
        task.setDescription(normalizeDescription(request.description()));
        task.setStatus(nextStatus);
        task.setPriority(request.priority() != null ? request.priority() : task.getPriority());
        task.setDueDate(request.dueDate());

        return TaskResponse.fromEntity(taskRepository.save(task));
    }

    public void deleteTask(Long id) {
        Task task = findTask(id);
        if (task.getStatus() == Status.IN_PROGRESS) {
            throw new BusinessRuleViolationException("Task with status IN_PROGRESS cannot be deleted");
        }
        taskRepository.delete(task);
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> searchTasks(String query, Pageable pageable) {
        return taskRepository.search(query.trim(), normalizePageable(pageable)).map(TaskResponse::fromEntity);
    }

    private Task findTask(Long id) {
        return taskRepository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }

    private void validateUniqueTitle(String title, Long idToExclude) {
        boolean exists = idToExclude == null
                ? taskRepository.existsByTitleIgnoreCase(title)
                : taskRepository.existsByTitleIgnoreCaseAndIdNot(title, idToExclude);
        if (exists) {
            throw new BusinessRuleViolationException("Task title must be unique");
        }
    }

    private void validateDueDate(LocalDate dueDate) {
        if (dueDate != null && !dueDate.isAfter(LocalDate.now())) {
            throw new BusinessRuleViolationException("Due date must be in the future");
        }
    }

    private Pageable normalizePageable(Pageable pageable) {
        int size = Math.min(Math.max(pageable.getPageSize(), 1), 100);
        Sort sort = pageable.getSort().isSorted() ? pageable.getSort() : Sort.by(Sort.Direction.DESC, "createdAt");
        validateSortFields(sort);
        return PageRequest.of(pageable.getPageNumber(), size, sort);
    }

    private void validateSortFields(Sort sort) {
        for (Sort.Order order : sort) {
            if (!ALLOWED_SORT_FIELDS.contains(order.getProperty())) {
                throw new InvalidRequestException(
                        "Invalid sort field '" + order.getProperty()
                                + "'. Allowed fields: " + String.join(", ", ALLOWED_SORT_FIELDS)
                );
            }
        }
    }

    private String normalizeTitle(String title) {
        return title.trim();
    }

    private String normalizeDescription(String description) {
        return description == null || description.isBlank() ? null : description.trim();
    }
}
