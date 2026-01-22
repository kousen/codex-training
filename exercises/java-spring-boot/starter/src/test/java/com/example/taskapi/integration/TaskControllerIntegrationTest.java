package com.example.taskapi.integration;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.hasItems;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.transaction.annotation.Transactional;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class TaskControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void createAndGetTask() throws Exception {
        Long id = createTask("Integration Create", LocalDate.now().plusDays(5));

        mockMvc.perform(get("/api/v1/tasks/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(id))
                .andExpect(jsonPath("$.title").value("Integration Create"));
    }

    @Test
    void listTasksReturnsPage() throws Exception {
        mockMvc.perform(get("/api/v1/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }

    @Test
    void listTasksIncludesSeedData() throws Exception {
        mockMvc.perform(get("/api/v1/tasks?size=50"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[*].title", hasItems("Write README", "Set up CI")));
    }

    @Test
    void duplicateTitleReturnsConflict() throws Exception {
        createTask("Duplicate Title", LocalDate.now().plusDays(3));

        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(baseCreatePayload("Duplicate Title", LocalDate.now().plusDays(4)))))
                .andExpect(status().isConflict());
    }

    @Test
    void updateDoneToTodoReturnsConflict() throws Exception {
        Long id = createTask("Finish Task", LocalDate.now().plusDays(7));

        mockMvc.perform(put("/api/v1/tasks/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(Map.of("status", "DONE"))))
                .andExpect(status().isOk());

        mockMvc.perform(put("/api/v1/tasks/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(Map.of("status", "TODO"))))
                .andExpect(status().isConflict());
    }

    @Test
    void deleteInProgressReturnsConflict() throws Exception {
        Long id = createTask("In Progress Task", LocalDate.now().plusDays(6));

        mockMvc.perform(put("/api/v1/tasks/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(Map.of("status", "IN_PROGRESS"))))
                .andExpect(status().isOk());

        mockMvc.perform(delete("/api/v1/tasks/{id}", id))
                .andExpect(status().isConflict());
    }

    @Test
    void createWithPastDueDateReturnsBadRequest() throws Exception {
        mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(baseCreatePayload("Past Task", LocalDate.now()))))
                .andExpect(status().isBadRequest());
    }

    @Test
    void createDefaultsStatusAndPriority() throws Exception {
        MvcResult result = mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(baseCreatePayload("Defaults Task", LocalDate.now().plusDays(2)))))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("TODO"))
                .andExpect(jsonPath("$.priority").value("MEDIUM"))
                .andReturn();

        JsonNode response = objectMapper.readTree(result.getResponse().getContentAsString());
        assertThat(response.get("id").asLong()).isPositive();
    }

    private Long createTask(String title, LocalDate dueDate) throws Exception {
        MvcResult result = mockMvc.perform(post("/api/v1/tasks")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(baseCreatePayload(title, dueDate))))
                .andExpect(status().isCreated())
                .andReturn();
        JsonNode response = objectMapper.readTree(result.getResponse().getContentAsString());
        return response.get("id").asLong();
    }

    private Map<String, Object> baseCreatePayload(String title, LocalDate dueDate) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("title", title);
        payload.put("dueDate", dueDate);
        return payload;
    }
}
