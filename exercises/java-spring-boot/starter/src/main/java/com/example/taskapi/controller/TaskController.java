package com.example.taskapi.controller;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.service.TaskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.enums.ParameterIn;
import io.swagger.v3.oas.annotations.Parameters;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;

@RestController
@Validated
@RequestMapping("/api/v1/tasks")
@Tag(name = "Tasks", description = "Task management API")
public class TaskController {

    private final TaskService taskService;

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @GetMapping
    @Operation(summary = "List tasks")
    @Parameters({
            @Parameter(name = "page", in = ParameterIn.QUERY, description = "Zero-based page index", example = "0"),
            @Parameter(name = "size", in = ParameterIn.QUERY, description = "Page size between 1 and 100", example = "20"),
            @Parameter(
                    name = "sort",
                    in = ParameterIn.QUERY,
                    description = "Sort as field,direction. Allowed fields: id, title, status, priority, dueDate, createdAt, updatedAt",
                    example = "createdAt,desc"
            )
    })
    public Page<TaskResponse> getTasks(
            @Parameter(hidden = true) @PageableDefault(size = 20, sort = "createdAt") Pageable pageable
    ) {
        return taskService.getAllTasks(pageable);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get a task by id")
    public TaskResponse getTask(@PathVariable Long id) {
        return taskService.getTaskById(id);
    }

    @PostMapping
    @Operation(summary = "Create a task")
    public ResponseEntity<TaskResponse> createTask(@Valid @RequestBody TaskCreateRequest request) {
        TaskResponse createdTask = taskService.createTask(request);
        URI location = ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(createdTask.id())
                .toUri();
        return ResponseEntity.created(location).body(createdTask);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update a task")
    public TaskResponse updateTask(@PathVariable Long id, @Valid @RequestBody TaskUpdateRequest request) {
        return taskService.updateTask(id, request);
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a task")
    public ResponseEntity<Void> deleteTask(@PathVariable Long id) {
        taskService.deleteTask(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/search")
    @Operation(summary = "Search tasks by title or description")
    @Parameters({
            @Parameter(name = "q", in = ParameterIn.QUERY, description = "Search text for title or description", example = "backlog"),
            @Parameter(name = "page", in = ParameterIn.QUERY, description = "Zero-based page index", example = "0"),
            @Parameter(name = "size", in = ParameterIn.QUERY, description = "Page size between 1 and 100", example = "20"),
            @Parameter(
                    name = "sort",
                    in = ParameterIn.QUERY,
                    description = "Sort as field,direction. Allowed fields: id, title, status, priority, dueDate, createdAt, updatedAt",
                    example = "createdAt,desc"
            )
    })
    public Page<TaskResponse> searchTasks(
            @RequestParam("q") @NotBlank(message = "Search query is required") String query,
            @Parameter(hidden = true) @PageableDefault(size = 20, sort = "createdAt") Pageable pageable
    ) {
        return taskService.searchTasks(query, pageable);
    }
}
