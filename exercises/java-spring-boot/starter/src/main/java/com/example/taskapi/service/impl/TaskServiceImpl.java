package com.example.taskapi.service.impl;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.UpdateTaskRequest;
import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.exception.BadRequestException;
import com.example.taskapi.exception.ConflictException;
import com.example.taskapi.exception.ResourceNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import java.time.LocalDate;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class TaskServiceImpl implements TaskService {

    private final TaskRepository taskRepository;

    public TaskServiceImpl(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @Override
    public TaskResponse create(CreateTaskRequest request) {
        if (taskRepository.existsByTitle(request.title())) {
            throw new ConflictException("Task title must be unique");
        }
        validateDueDate(request.dueDate());

        Task task = new Task();
        task.setTitle(request.title());
        task.setDescription(request.description());
        task.setPriority(request.priority() == null ? TaskPriority.MEDIUM : request.priority());
        task.setStatus(TaskStatus.TODO);
        task.setDueDate(request.dueDate());

        Task saved = taskRepository.save(task);
        return toResponse(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public TaskResponse getById(Long id) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task not found"));
        return toResponse(task);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<TaskResponse> list(Pageable pageable) {
        return taskRepository.findAll(pageable).map(this::toResponse);
    }

    @Override
    public TaskResponse update(Long id, UpdateTaskRequest request) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task not found"));

        if (request.title() != null && !request.title().equals(task.getTitle())) {
            if (taskRepository.existsByTitle(request.title())) {
                throw new ConflictException("Task title must be unique");
            }
            task.setTitle(request.title());
        }

        if (request.description() != null) {
            task.setDescription(request.description());
        }

        if (request.priority() != null) {
            task.setPriority(request.priority());
        }

        if (request.status() != null) {
            if (task.getStatus() == TaskStatus.DONE && request.status() == TaskStatus.TODO) {
                throw new ConflictException("Cannot change DONE task back to TODO");
            }
            task.setStatus(request.status());
        }

        if (request.dueDate() != null) {
            validateDueDate(request.dueDate());
            task.setDueDate(request.dueDate());
        }

        Task saved = taskRepository.save(task);
        return toResponse(saved);
    }

    @Override
    public void delete(Long id) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task not found"));
        if (task.getStatus() == TaskStatus.IN_PROGRESS) {
            throw new ConflictException("Cannot delete task with status IN_PROGRESS");
        }
        taskRepository.delete(task);
    }

    private void validateDueDate(LocalDate dueDate) {
        if (dueDate != null && !dueDate.isAfter(LocalDate.now())) {
            throw new BadRequestException("Due date must be in the future");
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
