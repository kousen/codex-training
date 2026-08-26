package com.example.taskapi.integration;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.UpdateTaskRequest;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

import static org.hamcrest.Matchers.greaterThanOrEqualTo;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class TaskControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void listsTasksWithPagination() throws Exception {
        mockMvc.perform(get("/api/v1/tasks").param("size", "2"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content.length()").value(2))
                .andExpect(jsonPath("$.totalElements").value(greaterThanOrEqualTo(3)))
                .andExpect(jsonPath("$.size").value(2));
    }

    @Test
    void getsTaskById() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Review API design"))
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
    }

    @Test
    void reportsMissingTask() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/99999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.message").value("Task with id 99999 was not found"))
                .andExpect(jsonPath("$.path").value("/api/v1/tasks/99999"));
    }

    @Test
    void createsTaskWithDefaults() throws Exception {
        CreateTaskRequest request = new CreateTaskRequest(
                "Prepare workshop",
                "Set up the coding lab",
                null,
                null,
                LocalDate.now().plusDays(10)
        );

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", org.hamcrest.Matchers.matchesPattern("/api/v1/tasks/\\d+")))
                .andExpect(jsonPath("$.title").value("Prepare workshop"))
                .andExpect(jsonPath("$.status").value("TODO"))
                .andExpect(jsonPath("$.priority").value("MEDIUM"))
                .andExpect(jsonPath("$.createdAt").exists())
                .andExpect(jsonPath("$.updatedAt").exists());
    }

    @Test
    void validatesCreateRequest() throws Exception {
        String invalidRequest = """
                {
                  "title": " ",
                  "description": "valid",
                  "dueDate": "2020-01-01"
                }
                """;

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(invalidRequest))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Request validation failed"))
                .andExpect(jsonPath("$.fieldErrors.title").value("Title is required"))
                .andExpect(jsonPath("$.fieldErrors.dueDate").value("Due date must be in the future"));
    }

    @Test
    void updatesTask() throws Exception {
        UpdateTaskRequest request = new UpdateTaskRequest(
                "Write integration tests",
                "Expanded endpoint coverage",
                Status.IN_PROGRESS,
                Priority.HIGH,
                LocalDate.now().plusDays(12)
        );

        mockMvc.perform(put("/api/v1/tasks/2")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"))
                .andExpect(jsonPath("$.priority").value("HIGH"))
                .andExpect(jsonPath("$.description").value("Expanded endpoint coverage"));
    }

    @Test
    void preventsDoneTaskReturningToTodo() throws Exception {
        UpdateTaskRequest request = new UpdateTaskRequest(
                "Publish documentation",
                "Keep docs published",
                Status.TODO,
                Priority.LOW,
                null
        );

        mockMvc.perform(put("/api/v1/tasks/3")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("A DONE task cannot be changed back to TODO"));
    }

    @Test
    void preventsDeletingInProgressTask() throws Exception {
        mockMvc.perform(delete("/api/v1/tasks/1"))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("An IN_PROGRESS task cannot be deleted"));
    }

    @Test
    void deletesTodoTask() throws Exception {
        mockMvc.perform(delete("/api/v1/tasks/2"))
                .andExpect(status().isNoContent());

        mockMvc.perform(get("/api/v1/tasks/2"))
                .andExpect(status().isNotFound());
    }

    @Test
    void searchesTitleAndDescription() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/search")
                        .param("query", "documentation"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalElements").value(1))
                .andExpect(jsonPath("$.content[0].title").value("Publish documentation"));
    }

    @Test
    void rejectsBlankSearchQuery() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/search").param("query", " "))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Request validation failed"))
                .andExpect(jsonPath("$.fieldErrors").isNotEmpty());
    }

    @Test
    void rejectsMalformedEnumValue() throws Exception {
        String malformedRequest = """
                {
                  "title": "Invalid status task",
                  "status": "BLOCKED",
                  "priority": "HIGH"
                }
                """;

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(malformedRequest))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Request contains an invalid value"));
    }

    @Test
    void publishesOpenApiDocumentation() throws Exception {
        mockMvc.perform(get("/api-docs"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.info.title").value("Task Management API"))
                .andExpect(jsonPath("$.paths['/api/v1/tasks']").exists());
    }
}
