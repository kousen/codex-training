package com.example.taskapi.service;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.BusinessRuleViolationException;
import com.example.taskapi.exception.DuplicateTaskTitleException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.exception.TaskValidationException;
import com.example.taskapi.repository.TaskRepository;
import jakarta.validation.Valid;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.validation.annotation.Validated;

@Service
@Validated
@Transactional
public class TaskService {

    private final TaskRepository taskRepository;

    public TaskService(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    @CacheEvict(cacheNames = {"tasks", "task", "taskSearches"}, allEntries = true)
    public Task createTask(@Valid Task task) {
        validateTaskForCreate(task);
        applyCreateDefaults(task);
        validateUniqueTitle(task.getTitle(), null);
        return taskRepository.save(task);
    }

    @Cacheable(cacheNames = "task", key = "#id")
    @Transactional(readOnly = true)
    public Task getTaskById(Long id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new TaskNotFoundException(id));
    }

    @Cacheable(cacheNames = "tasks", key = "'all'")
    @Transactional(readOnly = true)
    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    @Cacheable(cacheNames = "tasks", key = "'status:' + #status")
    @Transactional(readOnly = true)
    public List<Task> getTasksByStatus(Status status) {
        return taskRepository.findByStatus(status);
    }

    @Cacheable(cacheNames = "tasks", key = "'priority:' + #priority")
    @Transactional(readOnly = true)
    public List<Task> getTasksByPriority(Priority priority) {
        return taskRepository.findByPriority(priority);
    }

    @Cacheable(
            cacheNames = "taskSearches",
            key = "{#keyword, #status, #priority, #dueBefore, #dueAfter}")
    @Transactional(readOnly = true)
    public List<Task> searchTasks(
            String keyword, Status status, Priority priority, LocalDate dueBefore, LocalDate dueAfter) {
        return taskRepository.search(blankToNull(keyword), status, priority, dueBefore, dueAfter);
    }

    @CacheEvict(cacheNames = {"tasks", "task", "taskSearches"}, allEntries = true)
    public Task updateTask(Long id, Task updates) {
        Task existingTask = getTaskById(id);
        validateTaskForUpdate(updates);

        if (updates.getTitle() != null) {
            validateUniqueTitle(updates.getTitle(), existingTask.getId());
            existingTask.setTitle(updates.getTitle());
        }
        if (updates.getDescription() != null) {
            existingTask.setDescription(updates.getDescription());
        }
        if (updates.getStatus() != null) {
            validateStatusTransition(existingTask.getStatus(), updates.getStatus());
            existingTask.setStatus(updates.getStatus());
        }
        if (updates.getPriority() != null) {
            existingTask.setPriority(updates.getPriority());
        }
        if (updates.getDueDate() != null) {
            validateFutureDueDate(updates.getDueDate());
            existingTask.setDueDate(updates.getDueDate());
        }

        return taskRepository.save(existingTask);
    }

    @CacheEvict(cacheNames = {"tasks", "task", "taskSearches"}, allEntries = true)
    public void deleteTask(Long id) {
        Task task = getTaskById(id);
        if (task.getStatus() == Status.IN_PROGRESS) {
            throw new BusinessRuleViolationException("Cannot delete task with status IN_PROGRESS");
        }
        taskRepository.delete(task);
    }

    private void validateTaskForCreate(Task task) {
        if (task == null) {
            throw new TaskValidationException("Task is required");
        }
        validateTitle(task.getTitle());
        if (task.getDescription() != null && task.getDescription().length() > 500) {
            throw new TaskValidationException("Task description must be 500 characters or fewer");
        }
        validateFutureDueDate(task.getDueDate());
    }

    private void validateTaskForUpdate(Task task) {
        if (task == null) {
            throw new TaskValidationException("Task updates are required");
        }
        if (task.getTitle() != null) {
            validateTitle(task.getTitle());
        }
        if (task.getDescription() != null && task.getDescription().length() > 500) {
            throw new TaskValidationException("Task description must be 500 characters or fewer");
        }
        validateFutureDueDate(task.getDueDate());
    }

    private void applyCreateDefaults(Task task) {
        if (task.getStatus() == null) {
            task.setStatus(Status.TODO);
        }
        if (task.getPriority() == null) {
            task.setPriority(Priority.MEDIUM);
        }
    }

    private void validateUniqueTitle(String title, Long currentTaskId) {
        Optional<Task> taskWithTitle = taskRepository.findByTitleIgnoreCase(title);
        if (taskWithTitle.isPresent() && !taskWithTitle.get().getId().equals(currentTaskId)) {
            throw new DuplicateTaskTitleException(title);
        }
    }

    private void validateStatusTransition(Status currentStatus, Status newStatus) {
        if (currentStatus == Status.DONE && newStatus == Status.TODO) {
            throw new BusinessRuleViolationException("Cannot change DONE task back to TODO");
        }
    }

    private void validateFutureDueDate(LocalDate dueDate) {
        if (dueDate != null && !dueDate.isAfter(LocalDate.now())) {
            throw new TaskValidationException("Due date must be in the future");
        }
    }

    private void validateTitle(String title) {
        if (title == null || title.isBlank()) {
            throw new TaskValidationException("Task title is required");
        }
        if (title.length() > 100) {
            throw new TaskValidationException("Task title must be 100 characters or fewer");
        }
    }

    private String blankToNull(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }
        return value.trim();
    }
}
