package com.example.taskapi.service;

import com.example.taskapi.dto.*;
import com.example.taskapi.entity.*;
import com.example.taskapi.exception.*;
import com.example.taskapi.repository.TaskRepository;
import java.time.Clock;
import java.time.LocalDate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class TaskService {
    private static final Logger log = LoggerFactory.getLogger(TaskService.class);
    private final TaskRepository repository;
    private final Clock clock;

    public TaskService(TaskRepository repository, Clock clock) {
        this.repository = repository;
        this.clock = clock;
    }

    public TaskPage list(int page, int size) {
        return TaskPage.from(repository.findAll(pageable(page, size)).map(TaskResponse::from));
    }

    public TaskPage search(String query, int page, int size) {
        String term = query.strip();
        return TaskPage.from(repository.findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
            term, term, pageable(page, size)).map(TaskResponse::from));
    }

    public TaskResponse get(long id) { return TaskResponse.from(find(id)); }

    @Transactional
    public TaskResponse create(CreateTaskRequest request) {
        if (request.dueDate() != null && !request.dueDate().isAfter(LocalDate.now(clock))) {
            throw new InvalidTaskException("Due date must be in the future (UTC) when creating a task");
        }
        if (repository.existsByTitleKey(Task.normalizeTitle(request.title()))) {
            throw new TaskConflictException("A task with that title already exists");
        }
        Task task = new Task(request.title(), request.description(),
            request.status() == null ? TaskStatus.TODO : request.status(),
            request.priority() == null ? TaskPriority.MEDIUM : request.priority(), request.dueDate(), clock.instant());
        Task saved = repository.saveAndFlush(task);
        log.info("Created task {}", saved.getId());
        return TaskResponse.from(saved);
    }

    @Transactional
    public TaskResponse update(long id, UpdateTaskRequest request) {
        Task task = find(id);
        if (task.getStatus() == TaskStatus.DONE && request.status() == TaskStatus.TODO) {
            throw new TaskConflictException("A DONE task cannot be changed back to TODO");
        }
        if (repository.existsByTitleKeyAndIdNot(Task.normalizeTitle(request.title()), id)) {
            throw new TaskConflictException("A task with that title already exists");
        }
        task.update(request.title(), request.description(), request.status(), request.priority(),
            request.dueDate(), clock.instant());
        Task saved = repository.saveAndFlush(task);
        log.info("Updated task {}", id);
        return TaskResponse.from(saved);
    }

    @Transactional
    public void delete(long id) {
        Task task = find(id);
        if (task.getStatus() == TaskStatus.IN_PROGRESS) {
            throw new TaskConflictException("An IN_PROGRESS task cannot be deleted");
        }
        repository.delete(task);
        repository.flush();
        log.info("Deleted task {}", id);
    }

    private Task find(long id) {
        return repository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }

    private PageRequest pageable(int page, int size) {
        if ((long) page * size > Integer.MAX_VALUE) {
            throw new InvalidTaskException("Page offset exceeds supported range");
        }
        return PageRequest.of(page, size, Sort.by("id").ascending());
    }
}
