package com.example.taskapi.controller;

import com.example.taskapi.dto.*;
import com.example.taskapi.service.TaskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import java.net.URI;
import org.springframework.data.domain.*;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/tasks")
@Validated
@Tag(name = "Tasks", description = "Task management API v1")
public class TaskController {
    private final TaskService service;

    public TaskController(TaskService service) { this.service = service; }

    @GetMapping
    @Operation(summary = "List tasks", description = "Zero-based pages, ordered by ID; size defaults to 20, maximum 100.")
    public TaskPage list(@RequestParam(defaultValue = "0") @Min(0) int page,
            @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size) {
        return TaskPage.from(service.list(pageable(page, size)));
    }

    @GetMapping("/search")
    @Operation(summary = "Search titles and descriptions", description = "Case-insensitive literal substring search.")
    public TaskPage search(@RequestParam @NotBlank @Size(max = 500) String q,
            @RequestParam(defaultValue = "0") @Min(0) int page,
            @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size) {
        return TaskPage.from(service.search(q, pageable(page, size)));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get a task")
    public TaskResponse get(@PathVariable @Positive long id) { return service.get(id); }

    @PostMapping
    @Operation(summary = "Create a task", description = "Defaults to TODO and MEDIUM. Titles are unique and trimmed. Due dates must be after today in UTC.")
    public ResponseEntity<TaskResponse> create(@RequestBody @Valid TaskRequest request) {
        TaskResponse task = service.create(request);
        return ResponseEntity.created(URI.create("/api/v1/tasks/" + task.id())).body(task);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update a task", description = "Title is required. Omitted status/priority retain their values; omitted description/dueDate clear them.")
    public TaskResponse update(@PathVariable @Positive long id, @RequestBody @Valid TaskRequest request) {
        return service.update(id, request);
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a task", description = "Tasks in progress cannot be deleted.")
    public ResponseEntity<Void> delete(@PathVariable @Positive long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }

    private Pageable pageable(int page, int size) {
        return PageRequest.of(page, size, Sort.by("id"));
    }
}
