package com.example.taskapi.controller;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.request.RequestPostProcessor;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class TaskControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void listTasksReturnsSeededDevelopmentData() throws Exception {
        mockMvc.perform(get("/api/v1/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(4)))
                .andExpect(jsonPath("$[0].title").value("Review API requirements"));
    }

    @Test
    void searchTasksFiltersByStatusAndPriority() throws Exception {
        mockMvc.perform(get("/api/v1/tasks")
                        .param("status", "TODO")
                        .param("priority", "LOW"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].title").value("Document Swagger examples"));
    }

    @Test
    void getTaskReturnsTaskById() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/{id}", 1))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.status").value("DONE"));
    }

    @Test
    void getTaskReturnsNotFoundForMissingTask() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/{id}", 999))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.message").value("Task not found with id: 999"));
    }

    @Test
    void createTaskReturnsCreatedTaskAndLocationHeader() throws Exception {
        String payload = """
                {
                  "title": "Controller integration test",
                  "description": "Created through MockMvc",
                  "priority": "HIGH",
                  "dueDate": "2026-09-01"
                }
                """;

        mockMvc.perform(post("/api/v1/tasks")
                        .with(admin())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", containsString("/api/v1/tasks/")))
                .andExpect(jsonPath("$.title").value("Controller integration test"))
                .andExpect(jsonPath("$.status").value("TODO"))
                .andExpect(jsonPath("$.priority").value("HIGH"));
    }

    @Test
    void createTaskReturnsValidationErrors() throws Exception {
        String payload = """
                {
                  "title": "",
                  "description": "Invalid request"
                }
                """;

        mockMvc.perform(post("/api/v1/tasks")
                        .with(admin())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Validation failed"))
                .andExpect(jsonPath("$.validationErrors.title").value("Task title is required"));
    }

    @Test
    void createTaskReturnsConflictForDuplicateTitle() throws Exception {
        String payload = """
                {
                  "title": "Review API requirements",
                  "dueDate": "2026-09-01"
                }
                """;

        mockMvc.perform(post("/api/v1/tasks")
                        .with(admin())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Task title already exists: Review API requirements"));
    }

    @Test
    void updateTaskReturnsUpdatedTask() throws Exception {
        String payload = """
                {
                  "title": "Updated controller task",
                  "status": "IN_PROGRESS",
                  "priority": "HIGH",
                  "dueDate": "2026-09-15"
                }
                """;

        mockMvc.perform(put("/api/v1/tasks/{id}", 3)
                        .with(admin())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Updated controller task"))
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"))
                .andExpect(jsonPath("$.priority").value("HIGH"));
    }

    @Test
    void updateTaskReturnsConflictForInvalidStatusTransition() throws Exception {
        String payload = """
                {
                  "status": "TODO"
                }
                """;

        mockMvc.perform(put("/api/v1/tasks/{id}", 1)
                        .with(admin())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Cannot change DONE task back to TODO"));
    }

    @Test
    void deleteTaskReturnsNoContent() throws Exception {
        mockMvc.perform(delete("/api/v1/tasks/{id}", 4)
                        .with(admin()))
                .andExpect(status().isNoContent());
    }

    @Test
    void deleteTaskReturnsConflictForInProgressTask() throws Exception {
        mockMvc.perform(delete("/api/v1/tasks/{id}", 2)
                        .with(admin()))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Cannot delete task with status IN_PROGRESS"));
    }

    @Test
    void malformedJsonReturnsBadRequest() throws Exception {
        mockMvc.perform(post("/api/v1/tasks")
                        .with(admin())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Request body is missing or malformed"));
    }

    @Test
    void createTaskRequiresAuthentication() throws Exception {
        String payload = """
                {
                  "title": "Unauthorized task",
                  "dueDate": "2026-09-01"
                }
                """;

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void invalidEnumQueryParameterReturnsBadRequest() throws Exception {
        mockMvc.perform(get("/api/v1/tasks").param("status", "BLOCKED"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Invalid value for 'status': expected Status"));
    }

    private RequestPostProcessor admin() {
        return httpBasic("admin", "changeme");
    }
}
