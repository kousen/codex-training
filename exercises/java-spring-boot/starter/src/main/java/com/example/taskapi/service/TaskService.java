package com.example.taskapi.service;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskMapper;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.exception.DuplicateTaskTitleException;
import com.example.taskapi.exception.TaskConflictException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

@Service
@Transactional
public class TaskService {

    private final TaskRepository taskRepository;
    private final TaskMapper taskMapper;

    public TaskService(TaskRepository taskRepository, TaskMapper taskMapper) {
        this.taskRepository = taskRepository;
        this.taskMapper = taskMapper;
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> getAllTasks(Pageable pageable) {
        return taskRepository.findAll(pageable).map(taskMapper::toResponse);
    }

    @Transactional(readOnly = true)
    public TaskResponse getTask(Long id) {
        return taskMapper.toResponse(findTask(id));
    }

    public TaskResponse createTask(TaskCreateRequest request) {
        if (taskRepository.existsByTitleIgnoreCase(request.title())) {
            throw new DuplicateTaskTitleException(request.title());
        }

        Task task = new Task();
        task.setTitle(request.title());
        task.setDescription(request.description());
        task.setPriority(request.priority());
        task.setDueDate(request.dueDate());

        return taskMapper.toResponse(taskRepository.save(task));
    }

    public TaskResponse updateTask(Long id, TaskUpdateRequest request) {
        Task task = findTask(id);

        if (taskRepository.existsByTitleIgnoreCaseAndIdNot(request.title(), id)) {
            throw new DuplicateTaskTitleException(request.title());
        }

        if (task.getStatus() == TaskStatus.DONE && request.status() == TaskStatus.TODO) {
            throw new TaskConflictException("Cannot change a DONE task back to TODO");
        }

        task.setTitle(request.title());
        task.setDescription(request.description());
        task.setStatus(request.status());
        task.setPriority(request.priority());
        task.setDueDate(request.dueDate());

        return taskMapper.toResponse(task);
    }

    public void deleteTask(Long id) {
        Task task = findTask(id);

        if (task.getStatus() == TaskStatus.IN_PROGRESS) {
            throw new TaskConflictException("Cannot delete a task that is IN_PROGRESS");
        }

        taskRepository.delete(task);
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> searchTasks(String query, Pageable pageable) {
        if (!StringUtils.hasText(query)) {
            throw new IllegalArgumentException("Search query is required");
        }

        String trimmedQuery = query.trim();
        return taskRepository
                .findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
                        trimmedQuery, trimmedQuery, pageable)
                .map(taskMapper::toResponse);
    }

    private Task findTask(Long id) {
        return taskRepository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }
}
