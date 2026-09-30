package com.example.taskapi.unit;

import com.example.taskapi.controller.TaskController;
import com.example.taskapi.exception.GlobalExceptionHandler;
import com.example.taskapi.service.TaskService;
import java.sql.SQLException;
import java.util.Set;
import org.hibernate.exception.ConstraintViolationException;
import org.hibernate.exception.ConstraintViolationException.ConstraintKind;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.dao.*;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import static com.example.taskapi.support.TaskFixtures.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

class ErrorHandlingTest {
    TaskService service;
    MockMvc mvc;
    @BeforeEach void setup() {
        service = mock(TaskService.class);
        mvc = MockMvcBuilders.standaloneSetup(new TaskController(service))
            .setControllerAdvice(new GlobalExceptionHandler(CLOCK)).build();
    }

    @Test void unexpectedErrorsHideInternalDetails() throws Exception {
        when(service.get(1)).thenThrow(new IllegalStateException("sensitive internal details"));
        mvc.perform(get("/api/v1/tasks/1")).andExpect(status().isInternalServerError())
            .andExpect(jsonPath("$.message").value("An unexpected error occurred"));
    }

    @ParameterizedTest @ValueSource(strings = {"uk_tasks_title_key", "PUBLIC.UK_TASKS_TITLE_KEY INDEX PUBLIC.UK_TASKS_TITLE_KEY_INDEX_4"})
    void duplicateTitleConstraintReturnsConflict(String constraint) throws Exception {
        var cause = new ConstraintViolationException("SQL internal details", new SQLException(), ConstraintKind.UNIQUE, constraint);
        doThrow(new DataIntegrityViolationException("Write failed", cause)).when(service).delete(1);
        mvc.perform(delete("/api/v1/tasks/1")).andExpect(status().isConflict())
            .andExpect(jsonPath("$.message").value("A task with that title already exists"));
    }

    @ParameterizedTest @NullSource
    @ValueSource(strings = {"other_constraint", "uk_tasks_title_key_other", "PUBLIC.OTHER_INDEX_4"})
    void unknownConstraintsAreServerErrors(String constraint) throws Exception {
        var cause = new ConstraintViolationException("SQL internal details", new SQLException(), ConstraintKind.UNIQUE, constraint);
        doThrow(new DataIntegrityViolationException("Write failed", cause)).when(service).delete(1);
        mvc.perform(delete("/api/v1/tasks/1")).andExpect(status().isInternalServerError())
            .andExpect(jsonPath("$.message").value("An unexpected error occurred"));
    }

    @Test void otherIntegrityFailuresHideInternalDetails() throws Exception {
        var cause = new ConstraintViolationException("SQL internal details", new SQLException(), ConstraintKind.NOT_NULL, "uk_tasks_title_key");
        doThrow(new DataIntegrityViolationException("Write failed", cause)).when(service).delete(1);
        mvc.perform(delete("/api/v1/tasks/1")).andExpect(status().isInternalServerError())
            .andExpect(jsonPath("$.message").value("An unexpected error occurred"));
        doThrow(new DataIntegrityViolationException("SQL mentions uk_tasks_title_key")).when(service).delete(1);
        mvc.perform(delete("/api/v1/tasks/1")).andExpect(status().isInternalServerError())
            .andExpect(jsonPath("$.message").value("An unexpected error occurred"));
    }

    @Test void serviceValidationReturnsSafeBadRequest() throws Exception {
        when(service.get(1)).thenThrow(new jakarta.validation.ConstraintViolationException("internal method details", Set.of()));
        mvc.perform(get("/api/v1/tasks/1")).andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("Request validation failed"));
    }

    @Test void concurrentUpdateReturnsConflict() throws Exception {
        doThrow(new OptimisticLockingFailureException("stale version")).when(service).delete(1);
        mvc.perform(delete("/api/v1/tasks/1")).andExpect(status().isConflict())
            .andExpect(jsonPath("$.message").value("Task changed concurrently; reload it and retry"));
    }
}
