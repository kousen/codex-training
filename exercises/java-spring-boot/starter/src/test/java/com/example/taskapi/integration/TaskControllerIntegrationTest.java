package com.example.taskapi.integration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.repository.TaskRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.hamcrest.Matchers;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class TaskControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private TaskRepository taskRepository;

    @Test
    void shouldListTasks() throws Exception {
        mockMvc.perform(get("/api/v1/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }

    @Test
    void shouldCreateTask() throws Exception {
        TaskCreateRequest request = new TaskCreateRequest(
                "Integration New Task",
                "Integration test creation",
                TaskPriority.HIGH,
                LocalDate.now().plusDays(3)
        );

        String payload = objectMapper.writeValueAsString(request);

        String responseBody = mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isCreated())
                .andExpect(header().exists("Location"))
                .andExpect(jsonPath("$.id").isNumber())
                .andExpect(jsonPath("$.status").value("TODO"))
                .andReturn()
                .getResponse()
                .getContentAsString();

        com.example.taskapi.dto.TaskResponse created = objectMapper.readValue(responseBody, com.example.taskapi.dto.TaskResponse.class);
        assertThat(taskRepository.findById(created.id())).isPresent();
    }

    @Test
    void shouldRejectDuplicateTitle() throws Exception {
        TaskCreateRequest request = new TaskCreateRequest(
                "Initial Project Setup",
                "Duplicate title test",
                TaskPriority.LOW,
                LocalDate.now().plusDays(5)
        );

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Task title must be unique"));
    }

    @Test
    void shouldValidateDueDate() throws Exception {
        TaskCreateRequest request = new TaskCreateRequest(
                "Invalid Due Date",
                "Testing due date validation",
                TaskPriority.MEDIUM,
                LocalDate.now()
        );

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Validation error"))
                .andExpect(jsonPath("$.details[0]").value(org.hamcrest.Matchers.containsString("Due date must be in the future")));
    }

    @Test
    void shouldUpdateTask() throws Exception {
        Long taskId = taskRepository.findByTitleIgnoreCase("Initial Project Setup")
                .map(task -> task.getId())
                .orElseThrow();

        TaskUpdateRequest request = new TaskUpdateRequest(
                "Initial Project Setup Updated",
                "Updated via integration test",
                TaskStatus.IN_PROGRESS,
                TaskPriority.HIGH,
                LocalDate.now().plusDays(10)
        );

        mockMvc.perform(put("/api/v1/tasks/{id}", taskId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Initial Project Setup Updated"))
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
    }

    @Test
    void shouldPreventDeletingInProgressTask() throws Exception {
        Long taskId = taskRepository.findByTitleIgnoreCase("Draft API Specification")
                .map(task -> task.getId())
                .orElseThrow();

        mockMvc.perform(delete("/api/v1/tasks/{id}", taskId))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Cannot delete task in progress"));
    }

    @Test
    void shouldReturnNotFoundForMissingTask() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/{id}", 9999))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").value("Task with id 9999 not found"));
    }
}
