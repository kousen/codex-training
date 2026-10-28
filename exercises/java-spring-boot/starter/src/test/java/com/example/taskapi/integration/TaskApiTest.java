package com.example.taskapi.integration;

import com.example.taskapi.dto.TaskRequest;
import com.example.taskapi.entity.Status;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDate;
import java.time.ZoneOffset;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.*;
import static com.example.taskapi.TaskFixtures.*;
import static org.assertj.core.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class TaskApiTest {
    static final String BASE = "/api/v1/tasks";
    @Autowired MockMvc mvc;
    @Autowired ObjectMapper json;
    @Autowired TaskRepository repository;
    @Autowired TaskService service;

    @BeforeEach void reset() { repository.deleteAll(); }

    @Test void fullCrudAndTimestamps() throws Exception {
        var created = mvc.perform(post(BASE).contentType("application/json")
                .content(json.writeValueAsString(request("First", Status.TODO))))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", org.hamcrest.Matchers.startsWith(BASE + "/")))
                .andExpect(jsonPath("$.createdAt").isNotEmpty())
                .andExpect(jsonPath("$.updatedAt").isNotEmpty()).andReturn();
        var body = json.readTree(created.getResponse().getContentAsString());
        long id = body.get("id").asLong();
        String path = BASE + "/" + id;
        mvc.perform(get(path)).andExpect(status().isOk()).andExpect(jsonPath("$.title").value("First"));
        var updated = mvc.perform(put(path).contentType("application/json")
                .content(json.writeValueAsString(request("Changed", Status.DONE))))
                .andExpect(status().isOk()).andExpect(jsonPath("$.status").value("DONE"))
                .andExpect(jsonPath("$.createdAt").value(body.get("createdAt").asText())).andReturn();
        var updatedBody = json.readTree(updated.getResponse().getContentAsString());
        assertThat(java.time.Instant.parse(updatedBody.get("updatedAt").asText()))
                .isAfter(java.time.Instant.parse(body.get("updatedAt").asText()));
        mvc.perform(delete(path)).andExpect(status().isNoContent());
        mvc.perform(get(path)).andExpect(status().isNotFound()).andExpect(jsonPath("$.detail").exists());
    }

    @Test void paginationAndSearch() throws Exception {
        service.create(request("Alpha", Status.TODO));
        service.create(request("Beta", Status.TODO));
        mvc.perform(get(BASE).param("size", "1").param("page", "1"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.content[0].title").value("Beta"))
                .andExpect(jsonPath("$.totalElements").value(2)).andExpect(jsonPath("$.totalPages").value(2));
        mvc.perform(get(BASE)).andExpect(status().isOk()).andExpect(jsonPath("$.size").value(20));
        mvc.perform(get(BASE + "/search").param("q", "ALPH"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.content[0].title").value("Alpha"));
        mvc.perform(get(BASE + "/search").param("q", "description"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.totalElements").value(2));
        mvc.perform(get(BASE + "/search").param("q", "%"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.totalElements").value(0));
    }

    @Test void unversionedEndpointIsNotAvailable() throws Exception {
        mvc.perform(get("/api/tasks")).andExpect(status().isNotFound());
    }

    @Test void conflictsAndDefaults() throws Exception {
        var task = service.create(request("Busy", Status.IN_PROGRESS));
        mvc.perform(delete(BASE + "/" + task.id())).andExpect(status().isConflict());
        mvc.perform(post(BASE).contentType("application/json").content("{\"title\":\" Busy \"}"))
                .andExpect(status().isConflict());
        var done = service.create(request("Finished", Status.DONE));
        mvc.perform(put(BASE + "/" + done.id()).contentType("application/json")
                .content("{\"title\":\"Finished\",\"status\":\"TODO\"}"))
                .andExpect(status().isConflict());
        mvc.perform(post(BASE).contentType("application/json").content("{\"title\":\"Default\"}"))
                .andExpect(status().isCreated()).andExpect(jsonPath("$.status").value("TODO"))
                .andExpect(jsonPath("$.priority").value("MEDIUM"));
    }

    @ParameterizedTest
    @ValueSource(strings = {"{}", "{\"title\":\" \"}", "{\"title\":\"New\",\"status\":\"INVALID\"}",
            "{\"title\":\"New\",\"priority\":1}", "{\"title\":\"New\",\"dueDate\":\"nonsense\"}", "{", "null"})
    void rejectsInvalidBodies(String body) throws Exception {
        mvc.perform(post(BASE).contentType("application/json").content(body)).andExpect(status().isBadRequest());
    }

    @Test void rejectsLongFieldsAndPastDueDate() throws Exception {
        for (TaskRequest request : new TaskRequest[] {
                request("x".repeat(101), Status.TODO),
                new TaskRequest("New", "x".repeat(501), null, null, null),
                new TaskRequest("New", null, null, null, LocalDate.now(ZoneOffset.UTC))}) {
            mvc.perform(post(BASE).contentType("application/json").content(json.writeValueAsString(request)))
                    .andExpect(status().isBadRequest());
        }
    }

    @ParameterizedTest
    @ValueSource(strings = {"?page=-1", "?size=0", "?size=101", "?page=no", "/0", "/-1", "/bad",
            "/search", "/search?q="})
    void rejectsInvalidParameters(String suffix) throws Exception {
        mvc.perform(get(BASE + suffix)).andExpect(status().isBadRequest());
    }

    @Test void rejectsWhitespaceSearch() throws Exception {
        mvc.perform(get(BASE + "/search").param("q", "   ")).andExpect(status().isBadRequest());
    }

    @Test void missingUpdateAndDelete() throws Exception {
        mvc.perform(put(BASE + "/99999").contentType("application/json")
                .content(json.writeValueAsString(request("Missing", Status.TODO))))
                .andExpect(status().isNotFound());
        mvc.perform(delete(BASE + "/99999")).andExpect(status().isNotFound());
    }

    @Test void swaggerDocumentsEndpointsAndSchemas() throws Exception {
        mvc.perform(get("/api-docs")).andExpect(status().isOk())
                .andExpect(jsonPath("$.paths['/api/v1/tasks'].post").exists())
                .andExpect(jsonPath("$.paths['/api/tasks']").doesNotExist())
                .andExpect(jsonPath("$.components.schemas.TaskResponse").exists());
        mvc.perform(get("/swagger-ui.html")).andExpect(status().is3xxRedirection());
        mvc.perform(get("/swagger-ui/index.html")).andExpect(status().isOk());
    }

    @Test void serviceProxyValidatesRequests() {
        assertThatThrownBy(() -> service.create(new TaskRequest(" ", null, null, null, null)))
                .isInstanceOf(jakarta.validation.ConstraintViolationException.class);
        assertThatThrownBy(() -> service.get(0))
                .isInstanceOf(jakarta.validation.ConstraintViolationException.class);
    }
}
