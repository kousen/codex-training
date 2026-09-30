package com.example.taskapi.unit;

import com.example.taskapi.controller.TaskController;
import com.example.taskapi.exception.GlobalExceptionHandler;
import com.example.taskapi.service.TaskService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
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

    @Test void databaseRaceReturnsConflict() throws Exception {
        doThrow(new DataIntegrityViolationException("SQL internal details")).when(service).delete(1);
        mvc.perform(delete("/api/v1/tasks/1")).andExpect(status().isConflict())
            .andExpect(jsonPath("$.message").value("Task conflicts with existing data; titles must be unique"));
    }

    @Test void concurrentUpdateReturnsConflict() throws Exception {
        doThrow(new OptimisticLockingFailureException("stale version")).when(service).delete(1);
        mvc.perform(delete("/api/v1/tasks/1")).andExpect(status().isConflict())
            .andExpect(jsonPath("$.message").value("Task changed concurrently; reload it and retry"));
    }
}
