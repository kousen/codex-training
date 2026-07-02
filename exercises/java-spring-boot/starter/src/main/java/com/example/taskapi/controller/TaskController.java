package com.example.taskapi.controller;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.UpdateTaskRequest;
import com.example.taskapi.config.OpenApiConfig;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.ErrorResponse;
import com.example.taskapi.service.TaskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import java.net.URI;
import java.time.LocalDate;
import java.util.List;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
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

@RestController
@RequestMapping("/api/v1/tasks")
@Tag(name = "Tasks", description = "Task management operations")
public class TaskController {

    private final TaskService taskService;

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @Operation(
            summary = "Create a task",
            description = """
                    Creates a new task.

                    Business rules:
                    - title is required and must be unique
                    - status defaults to TODO when omitted
                    - priority defaults to MEDIUM when omitted
                    - dueDate must be in the future when supplied
                    """)
    @SecurityRequirement(name = OpenApiConfig.BASIC_AUTH_SCHEME)
    @ApiResponses({
            @ApiResponse(responseCode = "201", description = "Task created",
                    content = @Content(
                            schema = @Schema(implementation = TaskResponse.class),
                            examples = @ExampleObject(name = "created-task", value = """
                                    {
                                      "id": 5,
                                      "title": "Prepare workshop materials",
                                      "description": "Update slides and verify lab instructions",
                                      "status": "TODO",
                                      "priority": "HIGH",
                                      "dueDate": "2026-08-15",
                                      "createdAt": "2026-07-01T14:30:00Z",
                                      "updatedAt": "2026-07-01T14:30:00Z"
                                    }
                                    """))),
            @ApiResponse(responseCode = "400", description = "Validation error",
                    content = @Content(
                            schema = @Schema(implementation = ErrorResponse.class),
                            examples = @ExampleObject(name = "validation-error", value = """
                                    {
                                      "timestamp": "2026-07-01T14:30:00Z",
                                      "status": 400,
                                      "error": "Bad Request",
                                      "message": "Validation failed",
                                      "path": "/api/v1/tasks",
                                      "validationErrors": {
                                        "title": "Task title is required"
                                      }
                                    }
                                    """))),
            @ApiResponse(responseCode = "409", description = "Task title already exists",
                    content = @Content(
                            schema = @Schema(implementation = ErrorResponse.class),
                            examples = @ExampleObject(name = "duplicate-title", value = """
                                    {
                                      "timestamp": "2026-07-01T14:30:00Z",
                                      "status": 409,
                                      "error": "Conflict",
                                      "message": "Task title already exists: Prepare workshop materials",
                                      "path": "/api/v1/tasks",
                                      "validationErrors": {}
                                    }
                                    """)))
    })
    @PostMapping
    public ResponseEntity<TaskResponse> createTask(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    description = "Task fields to create. Omit status or priority to use defaults.",
                    content = @Content(
                            schema = @Schema(implementation = CreateTaskRequest.class),
                            examples = @ExampleObject(name = "create-task", value = """
                                    {
                                      "title": "Prepare workshop materials",
                                      "description": "Update slides and verify lab instructions",
                                      "priority": "HIGH",
                                      "dueDate": "2026-08-15"
                                    }
                                    """)))
            @Valid @RequestBody CreateTaskRequest request) {
        Task createdTask = taskService.createTask(toTask(request));
        URI location = ServletUriComponentsBuilder.fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(createdTask.getId())
                .toUri();
        return ResponseEntity.created(location).body(toResponse(createdTask));
    }

    @Operation(
            summary = "List tasks",
            description = """
                    Returns all tasks, optionally filtered by keyword, status, priority,
                    and due date range. When filters are omitted, all tasks are returned.
                    """)
    @ApiResponse(responseCode = "200", description = "Tasks returned",
            content = @Content(
                    array = @ArraySchema(schema = @Schema(implementation = TaskResponse.class)),
                    examples = @ExampleObject(name = "task-list", value = """
                            [
                              {
                                "id": 1,
                                "title": "Review API requirements",
                                "description": "Confirm task management business rules before implementation.",
                                "status": "DONE",
                                "priority": "HIGH",
                                "dueDate": "2026-08-01",
                                "createdAt": "2026-07-01T14:30:00Z",
                                "updatedAt": "2026-07-01T14:30:00Z"
                              }
                            ]
                            """)))
    @GetMapping
    public ResponseEntity<List<TaskResponse>> listTasks(
            @Parameter(description = "Search text matched against title or description", example = "swagger")
            @RequestParam(required = false) String keyword,

            @Parameter(description = "Filter by status", example = "TODO")
            @RequestParam(required = false) Status status,

            @Parameter(description = "Filter by priority", example = "HIGH")
            @RequestParam(required = false) Priority priority,

            @Parameter(description = "Only include tasks due on or before this date", example = "2026-08-31")
            @RequestParam(required = false)
            @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
            LocalDate dueBefore,

            @Parameter(description = "Only include tasks due on or after this date", example = "2026-08-01")
            @RequestParam(required = false)
            @DateTimeFormat(iso = DateTimeFormat.ISO.DATE)
            LocalDate dueAfter) {
        List<Task> tasks = hasFilters(keyword, status, priority, dueBefore, dueAfter)
                ? taskService.searchTasks(keyword, status, priority, dueBefore, dueAfter)
                : taskService.getAllTasks();
        return ResponseEntity.ok(tasks.stream().map(this::toResponse).toList());
    }

    @Operation(summary = "Get a task", description = "Returns one task by its numeric id.")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Task returned",
                    content = @Content(
                            schema = @Schema(implementation = TaskResponse.class),
                            examples = @ExampleObject(name = "task", value = """
                                    {
                                      "id": 1,
                                      "title": "Review API requirements",
                                      "description": "Confirm task management business rules before implementation.",
                                      "status": "DONE",
                                      "priority": "HIGH",
                                      "dueDate": "2026-08-01",
                                      "createdAt": "2026-07-01T14:30:00Z",
                                      "updatedAt": "2026-07-01T14:30:00Z"
                                    }
                                    """))),
            @ApiResponse(responseCode = "404", description = "Task not found",
                    content = @Content(
                            schema = @Schema(implementation = ErrorResponse.class),
                            examples = @ExampleObject(name = "not-found", value = """
                                    {
                                      "timestamp": "2026-07-01T14:30:00Z",
                                      "status": 404,
                                      "error": "Not Found",
                                      "message": "Task not found with id: 999",
                                      "path": "/api/v1/tasks/999",
                                      "validationErrors": {}
                                    }
                                    """)))
    })
    @GetMapping("/{id}")
    public ResponseEntity<TaskResponse> getTask(
            @Parameter(description = "Task id", example = "1")
            @PathVariable Long id) {
        return ResponseEntity.ok(toResponse(taskService.getTaskById(id)));
    }

    @Operation(
            summary = "Update a task",
            description = """
                    Updates the supplied fields on an existing task. Omitted fields remain unchanged.

                    Business rules:
                    - title must remain unique when changed
                    - dueDate must be in the future when supplied
                    - a DONE task cannot be changed back to TODO
                    """)
    @SecurityRequirement(name = OpenApiConfig.BASIC_AUTH_SCHEME)
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Task updated",
                    content = @Content(
                            schema = @Schema(implementation = TaskResponse.class),
                            examples = @ExampleObject(name = "updated-task", value = """
                                    {
                                      "id": 3,
                                      "title": "Write service unit tests",
                                      "description": "Cover title uniqueness, status transitions, and delete rules.",
                                      "status": "IN_PROGRESS",
                                      "priority": "HIGH",
                                      "dueDate": "2026-08-15",
                                      "createdAt": "2026-07-01T14:30:00Z",
                                      "updatedAt": "2026-07-01T15:45:00Z"
                                    }
                                    """))),
            @ApiResponse(responseCode = "400", description = "Validation error",
                    content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "404", description = "Task not found",
                    content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "409", description = "Business rule conflict",
                    content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @PutMapping("/{id}")
    public ResponseEntity<TaskResponse> updateTask(
            @Parameter(description = "Task id", example = "1")
            @PathVariable Long id,
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    description = "Fields to update. Any omitted field is left unchanged.",
                    content = @Content(
                            schema = @Schema(implementation = UpdateTaskRequest.class),
                            examples = @ExampleObject(name = "update-task", value = """
                                    {
                                      "status": "IN_PROGRESS",
                                      "priority": "HIGH",
                                      "dueDate": "2026-08-20"
                                    }
                                    """)))
            @Valid @RequestBody UpdateTaskRequest request) {
        return ResponseEntity.ok(toResponse(taskService.updateTask(id, toTask(request))));
    }

    @Operation(
            summary = "Delete a task",
            description = "Deletes a task unless it is currently IN_PROGRESS.")
    @SecurityRequirement(name = OpenApiConfig.BASIC_AUTH_SCHEME)
    @ApiResponses({
            @ApiResponse(responseCode = "204", description = "Task deleted"),
            @ApiResponse(responseCode = "404", description = "Task not found",
                    content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
            @ApiResponse(responseCode = "409", description = "Cannot delete an IN_PROGRESS task",
                    content = @Content(schema = @Schema(implementation = ErrorResponse.class)))
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTask(
            @Parameter(description = "Task id", example = "1")
            @PathVariable Long id) {
        taskService.deleteTask(id);
        return ResponseEntity.noContent().build();
    }

    private Task toTask(CreateTaskRequest request) {
        return new Task(
                request.title(),
                request.description(),
                request.status(),
                request.priority(),
                request.dueDate());
    }

    private Task toTask(UpdateTaskRequest request) {
        return Task.updatePatch(
                request.title(),
                request.description(),
                request.status(),
                request.priority(),
                request.dueDate());
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
                task.getUpdatedAt());
    }

    private boolean hasFilters(String keyword, Status status, Priority priority, LocalDate dueBefore, LocalDate dueAfter) {
        return keyword != null || status != null || priority != null || dueBefore != null || dueAfter != null;
    }
}
