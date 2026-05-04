package com.example.taskapi.e2e;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.repository.TaskRepository;
import com.fasterxml.jackson.databind.JsonNode;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.jdbc.Sql;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Sql(statements = "DELETE FROM tasks", executionPhase = Sql.ExecutionPhase.BEFORE_TEST_METHOD)
class TaskApiE2ETest {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private TaskRepository taskRepository;

    @Test
    void taskLifecycleWorksOverHttp() {
        TaskCreateRequest createRequest = new TaskCreateRequest(
                "E2E task", "Created through a real HTTP request", TaskPriority.HIGH, LocalDate.now().plusDays(5));

        ResponseEntity<TaskResponse> createResponse =
                restTemplate.postForEntity(url("/api/v1/tasks"), createRequest, TaskResponse.class);

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(createResponse.getHeaders().getLocation()).hasPath("/api/v1/tasks/" + createResponse.getBody().id());
        assertThat(createResponse.getBody())
                .extracting(TaskResponse::title, TaskResponse::status, TaskResponse::priority)
                .containsExactly("E2E task", TaskStatus.TODO, TaskPriority.HIGH);

        Long taskId = createResponse.getBody().id();

        ResponseEntity<TaskResponse> getResponse =
                restTemplate.getForEntity(url("/api/v1/tasks/" + taskId), TaskResponse.class);

        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(getResponse.getBody().description()).isEqualTo("Created through a real HTTP request");

        TaskUpdateRequest updateRequest = new TaskUpdateRequest(
                "E2E task updated",
                "Updated through a real HTTP request",
                TaskStatus.IN_PROGRESS,
                TaskPriority.MEDIUM,
                LocalDate.now().plusDays(10));

        ResponseEntity<TaskResponse> updateResponse = restTemplate.exchange(
                url("/api/v1/tasks/" + taskId), HttpMethod.PUT, new HttpEntity<>(updateRequest), TaskResponse.class);

        assertThat(updateResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(updateResponse.getBody())
                .extracting(TaskResponse::title, TaskResponse::status, TaskResponse::priority)
                .containsExactly("E2E task updated", TaskStatus.IN_PROGRESS, TaskPriority.MEDIUM);

        ResponseEntity<JsonNode> searchResponse =
                restTemplate.getForEntity(url("/api/v1/tasks/search?q=updated"), JsonNode.class);

        assertThat(searchResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(searchResponse.getBody().path("totalElements").asLong()).isEqualTo(1);
        assertThat(searchResponse.getBody().path("content").get(0).path("title").asText())
                .isEqualTo("E2E task updated");

        TaskUpdateRequest readyToDeleteRequest = new TaskUpdateRequest(
                "E2E task updated",
                "Ready to delete",
                TaskStatus.DONE,
                TaskPriority.MEDIUM,
                LocalDate.now().plusDays(10));

        restTemplate.exchange(
                url("/api/v1/tasks/" + taskId),
                HttpMethod.PUT,
                new HttpEntity<>(readyToDeleteRequest),
                TaskResponse.class);

        ResponseEntity<Void> deleteResponse =
                restTemplate.exchange(url("/api/v1/tasks/" + taskId), HttpMethod.DELETE, HttpEntity.EMPTY, Void.class);

        assertThat(deleteResponse.getStatusCode()).isEqualTo(HttpStatus.NO_CONTENT);
        assertThat(taskRepository.existsById(taskId)).isFalse();
    }

    private String url(String path) {
        return "http://localhost:" + port + path;
    }
}
