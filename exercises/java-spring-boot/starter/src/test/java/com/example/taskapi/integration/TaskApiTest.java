package com.example.taskapi.integration;

import com.example.taskapi.dto.*;
import com.example.taskapi.entity.*;
import com.example.taskapi.repository.TaskRepository;
import java.time.*;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.context.annotation.*;
import org.springframework.test.web.servlet.*;
import tools.jackson.databind.ObjectMapper;
import static com.example.taskapi.support.TaskFixtures.*;
import static org.assertj.core.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {"app.sample-data.enabled=false", "spring.datasource.url=jdbc:h2:mem:api-tests", "spring.jpa.show-sql=false", "logging.level.org.hibernate.SQL=INFO"})
@AutoConfigureMockMvc
@Import(TaskApiTest.TimeConfiguration.class)
class TaskApiTest {
    @TestConfiguration static class TimeConfiguration {
        @Bean @Primary Clock testClock() { return CLOCK; }
    }
    @Autowired MockMvc mvc;
    @Autowired ObjectMapper json;
    @Autowired TaskRepository repository;
    @BeforeEach void clean() { repository.deleteAll(); }

    long createTask(String title, TaskStatus status) throws Exception {
        var request = new CreateTaskRequest(title, "Searchable description", status, null, null);
        var result = mvc.perform(post("/api/v1/tasks").contentType("application/json").content(json.writeValueAsString(request)))
            .andExpect(status().isCreated()).andReturn();
        return json.readTree(result.getResponse().getContentAsString()).get("id").longValue();
    }

    @Test void completeCrudAndTimestamps() throws Exception {
        var result = mvc.perform(post("/api/v1/tasks").contentType("application/json").content("{\"title\":\"  First task  \"}"))
            .andExpect(status().isCreated()).andExpect(jsonPath("$.title").value("First task"))
            .andExpect(jsonPath("$.status").value("TODO")).andExpect(jsonPath("$.priority").value("MEDIUM"))
            .andExpect(jsonPath("$.createdAt").value(NOW.toString())).andExpect(jsonPath("$.updatedAt").value(NOW.toString()))
            .andExpect(jsonPath("$.titleKey").doesNotExist()).andExpect(jsonPath("$.version").doesNotExist()).andReturn();
        long id = json.readTree(result.getResponse().getContentAsString()).get("id").longValue();
        assertThat(result.getResponse().getHeader("Location")).isEqualTo("/api/v1/tasks/" + id);
        mvc.perform(get("/api/v1/tasks/{id}", id)).andExpect(status().isOk()).andExpect(jsonPath("$.title").value("First task"));
        var updated = mvc.perform(put("/api/v1/tasks/{id}", id).contentType("application/json")
            .content(json.writeValueAsString(update("New title", TaskStatus.DONE))))
            .andExpect(status().isOk()).andExpect(jsonPath("$.status").value("DONE"))
            .andExpect(jsonPath("$.createdAt").value(NOW.toString())).andReturn();
        assertThat(Instant.parse(json.readTree(updated.getResponse().getContentAsString()).get("updatedAt").stringValue())).isAfter(NOW);
        mvc.perform(delete("/api/v1/tasks/{id}", id)).andExpect(status().isNoContent()).andExpect(content().string(""));
        mvc.perform(get("/api/v1/tasks/{id}", id)).andExpect(status().isNotFound()).andExpect(jsonPath("$.path").value("/api/v1/tasks/" + id));
    }

    @Test void listAndSearchHaveStablePagination() throws Exception {
        createTask("Zulu", TaskStatus.TODO);
        createTask("Alpha", TaskStatus.DONE);
        mvc.perform(get("/api/v1/tasks")).andExpect(status().isOk()).andExpect(jsonPath("$.size").value(20))
            .andExpect(jsonPath("$.totalElements").value(2)).andExpect(jsonPath("$.content[0].title").value("Zulu"));
        mvc.perform(get("/api/v1/tasks").param("page", "1").param("size", "1"))
            .andExpect(status().isOk()).andExpect(jsonPath("$.content[0].title").value("Alpha"))
            .andExpect(jsonPath("$.page").value(1)).andExpect(jsonPath("$.totalPages").value(2));
        mvc.perform(get("/api/v1/tasks/search").param("q", " ALP "))
            .andExpect(status().isOk()).andExpect(jsonPath("$.totalElements").value(1));
        mvc.perform(get("/api/v1/tasks/search").param("q", "SEARCHABLE").param("size", "1").param("page", "1"))
            .andExpect(status().isOk()).andExpect(jsonPath("$.totalElements").value(2)).andExpect(jsonPath("$.content.length()").value(1));
        mvc.perform(get("/api/v1/tasks").param("page", "99")).andExpect(status().isOk()).andExpect(jsonPath("$.content").isEmpty());
    }

    @ParameterizedTest @ValueSource(strings = {"%", "_", "' OR 1=1 --", "no match"})
    void searchTreatsSqlAndWildcardsAsLiteralText(String query) throws Exception {
        createTask("Ordinary task", TaskStatus.TODO);
        mvc.perform(get("/api/v1/tasks/search").param("q", query)).andExpect(status().isOk()).andExpect(jsonPath("$.totalElements").value(0));
    }

    @Test void enforcesBusinessConflictsAndRollsBackUpdates() throws Exception {
        long done = createTask("Completed", TaskStatus.DONE);
        long active = createTask("Active", TaskStatus.IN_PROGRESS);
        mvc.perform(post("/api/v1/tasks").contentType("application/json").content("{\"title\":\" COMPLETED \"}"))
            .andExpect(status().isConflict());
        mvc.perform(put("/api/v1/tasks/{id}", done).contentType("application/json").content(json.writeValueAsString(update("Changed", TaskStatus.TODO))))
            .andExpect(status().isConflict());
        mvc.perform(put("/api/v1/tasks/{id}", active).contentType("application/json").content(json.writeValueAsString(update("completed", TaskStatus.DONE))))
            .andExpect(status().isConflict());
        mvc.perform(get("/api/v1/tasks/{id}", active)).andExpect(jsonPath("$.title").value("Active")).andExpect(jsonPath("$.status").value("IN_PROGRESS"));
        mvc.perform(delete("/api/v1/tasks/{id}", active)).andExpect(status().isConflict());
        mvc.perform(put("/api/v1/tasks/{id}", done).contentType("application/json").content(json.writeValueAsString(update("COMPLETED", TaskStatus.DONE))))
            .andExpect(status().isOk());
    }

    @ParameterizedTest @ValueSource(strings = {"", " ", "\t"})
    void rejectsBlankTitles(String title) throws Exception {
        mvc.perform(post("/api/v1/tasks").contentType("application/json").content(json.writeValueAsString(create(title))))
            .andExpect(status().isBadRequest()).andExpect(jsonPath("$.fieldErrors.title").exists());
    }

    @Test void validatesLengthsRequiredFieldsAndDueDates() throws Exception {
        mvc.perform(post("/api/v1/tasks").contentType("application/json").content("{}"))
            .andExpect(status().isBadRequest()).andExpect(jsonPath("$.fieldErrors.title").exists());
        mvc.perform(post("/api/v1/tasks").contentType("application/json")
            .content(json.writeValueAsString(new CreateTaskRequest("t".repeat(101), "d".repeat(501), null, null, null))))
            .andExpect(status().isBadRequest()).andExpect(jsonPath("$.fieldErrors.title").exists()).andExpect(jsonPath("$.fieldErrors.description").exists());
        mvc.perform(post("/api/v1/tasks").contentType("application/json")
            .content(json.writeValueAsString(new CreateTaskRequest("t".repeat(100), "d".repeat(500), null, null, LocalDate.of(2030, 6, 16)))))
            .andExpect(status().isCreated());
        for (String date : new String[] {"2030-06-14", "2030-06-15"}) {
            mvc.perform(post("/api/v1/tasks").contentType("application/json").content("{\"title\":\"Task\",\"dueDate\":\"" + date + "\"}"))
                .andExpect(status().isBadRequest()).andExpect(jsonPath("$.message").value("Due date must be in the future (UTC) when creating a task"));
        }
        long id = createTask("Existing", TaskStatus.TODO);
        mvc.perform(put("/api/v1/tasks/{id}", id).contentType("application/json").content("{\"title\":\"Task\"}"))
            .andExpect(status().isBadRequest()).andExpect(jsonPath("$.fieldErrors.status").exists()).andExpect(jsonPath("$.fieldErrors.priority").exists());
    }

    @ParameterizedTest @ValueSource(strings = {"{", "null", "{\"title\":\"X\",\"status\":\"INVALID\"}", "{\"title\":\"X\",\"status\":1}", "{\"title\":\"X\",\"priority\":\"INVALID\"}", "{\"title\":\"X\",\"dueDate\":\"not-a-date\"}"})
    void malformedJsonReturnsSafeErrors(String body) throws Exception {
        mvc.perform(post("/api/v1/tasks").contentType("application/json").content(body))
            .andExpect(status().isBadRequest()).andExpect(jsonPath("$.status").value(400))
            .andExpect(jsonPath("$.message").value("Invalid request body or parameters"));
    }

    @ParameterizedTest @ValueSource(strings = {"/api/v1/tasks?page=-1", "/api/v1/tasks?page=2147483647&size=100", "/api/v1/tasks?size=0", "/api/v1/tasks?size=101", "/api/v1/tasks?page=abc", "/api/v1/tasks/search", "/api/v1/tasks/search?q=", "/api/v1/tasks/0", "/api/v1/tasks/-1", "/api/v1/tasks/abc"})
    void rejectsInvalidParameters(String url) throws Exception {
        mvc.perform(get(url)).andExpect(status().isBadRequest()).andExpect(jsonPath("$.status").value(400));
    }

    @Test void searchRejectsWhitespaceAndTooLongQuery() throws Exception {
        for (String query : new String[] {"   ", "x".repeat(501)}) {
            mvc.perform(get("/api/v1/tasks/search").param("q", query)).andExpect(status().isBadRequest());
        }
        mvc.perform(get("/api/v1/tasks").param("size", "100")).andExpect(status().isOk());
    }

    @Test void returns404ForMissingWriteTargets() throws Exception {
        mvc.perform(put("/api/v1/tasks/{id}", Long.MAX_VALUE).contentType("application/json").content(json.writeValueAsString(update("Absent", TaskStatus.TODO))))
            .andExpect(status().isNotFound());
        mvc.perform(delete("/api/v1/tasks/{id}", Long.MAX_VALUE)).andExpect(status().isNotFound());
    }

    @Test void exposesDocumentationAndHandlesUnsupportedHttp() throws Exception {
        mvc.perform(get("/api-docs")).andExpect(status().isOk())
            .andExpect(jsonPath("$.info.title").value("Task Management API"))
            .andExpect(jsonPath("$.paths['/api/v1/tasks'].post.responses['201']").exists())
            .andExpect(jsonPath("$.paths['/api/v1/tasks/search']").exists())
            .andExpect(jsonPath("$.paths['/api/v1/tasks'].post.responses['400'].content['application/json'].schema['$ref']").value("#/components/schemas/ApiError"));
        mvc.perform(get("/swagger-ui.html")).andExpect(status().is3xxRedirection());
        mvc.perform(patch("/api/v1/tasks/1")).andExpect(status().isMethodNotAllowed());
        mvc.perform(post("/api/v1/tasks").contentType("text/plain").content("hello")).andExpect(status().isUnsupportedMediaType());
    }
}
