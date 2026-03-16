package com.example.taskapi.integration;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.support.TaskFixtures;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class TaskControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private TaskRepository taskRepository;

    @BeforeEach
    void setUp() {
        taskRepository.deleteAll();

        Task alpha = new Task();
        alpha.setTitle("Alpha task");
        alpha.setDescription("First task");
        alpha.setStatus(Status.TODO);
        alpha.setPriority(Priority.HIGH);
        alpha.setDueDate(LocalDate.now().plusDays(4));

        Task beta = new Task();
        beta.setTitle("Beta task");
        beta.setDescription("Contains searchable text");
        beta.setStatus(Status.IN_PROGRESS);
        beta.setPriority(Priority.MEDIUM);
        beta.setDueDate(LocalDate.now().plusDays(6));

        taskRepository.save(alpha);
        taskRepository.save(beta);
    }

    @Test
    void getTasksReturnsPagedResults() throws Exception {
        mockMvc.perform(get("/api/v1/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content.length()").value(2))
                .andExpect(jsonPath("$.content[0].title").exists());
    }

    @Test
    void getTasksReturnsBadRequestForInvalidSortField() throws Exception {
        mockMvc.perform(get("/api/v1/tasks").param("sort", "string"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value(org.hamcrest.Matchers.containsString("Invalid sort field 'string'")))
                .andExpect(jsonPath("$.message").value(org.hamcrest.Matchers.containsString("createdAt")))
                .andExpect(jsonPath("$.message").value(org.hamcrest.Matchers.containsString("updatedAt")));
    }

    @Test
    void getTaskReturnsSingleRecord() throws Exception {
        Long taskId = taskRepository.findAll().get(0).getId();

        mockMvc.perform(get("/api/v1/tasks/{id}", taskId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(taskId))
                .andExpect(jsonPath("$.title").exists());
    }

    @Test
    void createTaskReturnsCreatedResource() throws Exception {
        var request = TaskFixtures.createRequest("Created from API");

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", org.hamcrest.Matchers.containsString("/api/v1/tasks/")))
                .andExpect(jsonPath("$.title").value("Created from API"))
                .andExpect(jsonPath("$.status").value("TODO"))
                .andExpect(jsonPath("$.priority").value("MEDIUM"));
    }

    @Test
    void createTaskReturnsBadRequestForInvalidPayload() throws Exception {
        String payload = """
                {
                  "title": "",
                  "description": "Invalid"
                }
                """;

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(payload))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Validation failed"))
                .andExpect(jsonPath("$.fieldErrors.title").value("Title is required"));
    }

    @Test
    void updateTaskReturnsUpdatedTask() throws Exception {
        Long taskId = taskRepository.findAll().get(0).getId();
        var request = TaskFixtures.updateRequest("Alpha task updated", Status.DONE, Priority.LOW);

        mockMvc.perform(put("/api/v1/tasks/{id}", taskId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Alpha task updated"))
                .andExpect(jsonPath("$.status").value("DONE"))
                .andExpect(jsonPath("$.priority").value("LOW"));
    }

    @Test
    void deleteTaskReturnsConflictForInProgressTask() throws Exception {
        Long taskId = taskRepository.findAll().stream()
                .filter(task -> task.getStatus() == Status.IN_PROGRESS)
                .findFirst()
                .orElseThrow()
                .getId();

        mockMvc.perform(delete("/api/v1/tasks/{id}", taskId))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Task with status IN_PROGRESS cannot be deleted"));
    }

    @Test
    void searchTasksMatchesTitleOrDescription() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/search").param("q", "searchable"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content.length()").value(1))
                .andExpect(jsonPath("$.content[0].title").value("Beta task"));
    }

    @Test
    void missingTaskReturnsNotFound() throws Exception {
        mockMvc.perform(get("/api/v1/tasks/{id}", 9999))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").value("Task not found with id 9999"));
    }
}
