package com.example.taskapi.integration;

import static com.example.taskapi.entity.TaskStatus.DONE;
import static com.example.taskapi.entity.TaskStatus.IN_PROGRESS;
import static com.example.taskapi.entity.TaskStatus.TODO;
import static com.example.taskapi.fixture.TaskTestData.task;
import static com.example.taskapi.fixture.TaskTestData.updateRequest;
import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.repository.TaskRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@Sql(statements = "DELETE FROM tasks", executionPhase = Sql.ExecutionPhase.BEFORE_TEST_METHOD)
class TaskControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private TaskRepository taskRepository;

    @Test
    void listTasksReturnsPaginatedResults() throws Exception {
        taskRepository.save(task(null, "First task", TODO));
        taskRepository.save(task(null, "Second task", IN_PROGRESS));

        mockMvc.perform(get("/api/v1/tasks").param("page", "0").param("size", "1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content.length()").value(1))
                .andExpect(jsonPath("$.totalElements").value(2));
    }

    @Test
    void getTaskReturnsTaskById() throws Exception {
        Task task = taskRepository.save(task(null, "Find me", TODO));

        mockMvc.perform(get("/api/v1/tasks/{id}", task.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(task.getId()))
                .andExpect(jsonPath("$.title").value("Find me"));
    }

    @Test
    void createTaskAppliesDefaultStatusAndPriority() throws Exception {
        TaskCreateRequest request =
                new TaskCreateRequest("Create API", "Build the create endpoint", null, LocalDate.now().plusDays(4));

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", containsString("/api/v1/tasks/")))
                .andExpect(jsonPath("$.title").value("Create API"))
                .andExpect(jsonPath("$.status").value("TODO"))
                .andExpect(jsonPath("$.priority").value("MEDIUM"));
    }

    @Test
    void createTaskRejectsInvalidInput() throws Exception {
        TaskCreateRequest request =
                new TaskCreateRequest("", "Missing title", TaskPriority.HIGH, LocalDate.now().minusDays(1));

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Validation failed"))
                .andExpect(jsonPath("$.validationErrors.title").exists())
                .andExpect(jsonPath("$.validationErrors.dueDate").exists());
    }

    @Test
    void updateTaskRejectsDoneTaskReturningToTodo() throws Exception {
        Task task = taskRepository.save(task(null, "Already done", DONE));

        mockMvc.perform(put("/api/v1/tasks/{id}", task.getId())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updateRequest("Already done", TODO))))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Cannot change a DONE task back to TODO"));
    }

    @Test
    void deleteTaskRejectsInProgressTask() throws Exception {
        Task task = taskRepository.save(task(null, "Working", IN_PROGRESS));

        mockMvc.perform(delete("/api/v1/tasks/{id}", task.getId()))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.message").value("Cannot delete a task that is IN_PROGRESS"));
    }

    @Test
    void deleteTaskRemovesTodoTask() throws Exception {
        Task task = taskRepository.save(task(null, "Delete me", TODO));

        mockMvc.perform(delete("/api/v1/tasks/{id}", task.getId())).andExpect(status().isNoContent());
    }

    @Test
    void searchTasksFindsTitleOrDescriptionMatches() throws Exception {
        taskRepository.save(task(null, "Write docs", TODO));
        taskRepository.save(task(null, "Implement API", TODO));

        mockMvc.perform(get("/api/v1/tasks/search").param("q", "docs"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalElements").value(1))
                .andExpect(jsonPath("$.content[0].title").value("Write docs"));
    }
}
