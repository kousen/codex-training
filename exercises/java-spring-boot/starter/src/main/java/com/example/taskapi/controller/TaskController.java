package com.example.taskapi.controller;

import com.example.taskapi.dto.*;
import com.example.taskapi.service.TaskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import java.net.URI;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(value = "/api/v1/tasks", produces = MediaType.APPLICATION_JSON_VALUE)
@Tag(name = "Tasks", description = "Task management with validation and lifecycle rules")
@ApiResponses({@ApiResponse(responseCode = "400", description = "Invalid request",
        content = @Content(schema = @Schema(implementation = ApiError.class))),
    @ApiResponse(responseCode = "500", description = "Unexpected server error",
        content = @Content(schema = @Schema(implementation = ApiError.class)))})
public class TaskController {
    private final TaskService service;
    public TaskController(TaskService service) { this.service = service; }

    @GetMapping
    @Operation(summary = "List tasks", description = "Sorted by ID ascending; page is zero-based, size is 1–100.")
    public TaskPage list(@RequestParam(defaultValue = "0") @Min(0) int page,
                         @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size) {
        return service.list(page, size);
    }

    @GetMapping("/search")
    @Operation(summary = "Search titles and descriptions", description = "Case-insensitive literal substring search using q; results are paginated.")
    public TaskPage search(@RequestParam @NotBlank @Size(max = 500) String q,
                           @RequestParam(defaultValue = "0") @Min(0) int page,
                           @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size) {
        return service.search(q, page, size);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get a task")
    @ApiResponse(responseCode = "404", description = "Task not found",
        content = @Content(schema = @Schema(implementation = ApiError.class)))
    public TaskResponse get(@PathVariable @Positive long id) { return service.get(id); }

    @PostMapping
    @Operation(summary = "Create a task", description = "Titles are trimmed and unique ignoring case. Defaults: TODO and MEDIUM. Due date must be in the future in UTC.")
    @ApiResponses({@ApiResponse(responseCode = "201", description = "Task created"),
        @ApiResponse(responseCode = "409", description = "Duplicate title",
        content = @Content(schema = @Schema(implementation = ApiError.class)))})
    public ResponseEntity<TaskResponse> create(@Valid @RequestBody CreateTaskRequest request) {
        TaskResponse task = service.create(request);
        return ResponseEntity.created(URI.create("/api/v1/tasks/" + task.id())).body(task);
    }

    @PutMapping("/{id}")
    @Operation(summary = "Replace a task", description = "Title, status and priority are required. Omitted description/dueDate are cleared. DONE cannot move directly to TODO; past due dates are allowed on update.")
    @ApiResponses({@ApiResponse(responseCode = "404", description = "Task not found",
        content = @Content(schema = @Schema(implementation = ApiError.class))),
        @ApiResponse(responseCode = "409", description = "Duplicate title, prohibited transition or concurrent modification",
        content = @Content(schema = @Schema(implementation = ApiError.class)))})
    public TaskResponse update(@PathVariable @Positive long id, @Valid @RequestBody UpdateTaskRequest request) {
        return service.update(id, request);
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete a task", description = "Tasks in progress cannot be deleted.")
    @ApiResponses({@ApiResponse(responseCode = "204", description = "Task deleted"),
        @ApiResponse(responseCode = "404", description = "Task not found",
        content = @Content(schema = @Schema(implementation = ApiError.class))),
        @ApiResponse(responseCode = "409", description = "Task in progress or concurrent modification",
        content = @Content(schema = @Schema(implementation = ApiError.class)))})
    public ResponseEntity<Void> delete(@PathVariable @Positive long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
