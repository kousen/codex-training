package com.example.taskapi.exception;

import jakarta.servlet.http.HttpServletRequest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.mock.http.MockHttpInputMessage;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class GlobalExceptionHandlerTest {

    private GlobalExceptionHandler handler;
    private HttpServletRequest request;

    @BeforeEach
    void setUp() {
        handler = new GlobalExceptionHandler();
        request = mock(HttpServletRequest.class);
        when(request.getRequestURI()).thenReturn("/api/v1/tasks");
    }

    @Test
    void mapsMalformedRequestsToBadRequest() {
        HttpMessageNotReadableException exception = new HttpMessageNotReadableException(
                "Malformed request",
                new MockHttpInputMessage(new byte[0])
        );

        ResponseEntity<ApiError> response = handler.handleMalformedRequest(exception, request);

        assertError(response, HttpStatus.BAD_REQUEST, "Request contains an invalid value");
    }

    @Test
    void mapsDatabaseConstraintFailuresToConflict() {
        DataIntegrityViolationException exception = new DataIntegrityViolationException("duplicate");

        ResponseEntity<ApiError> response = handler.handleDataIntegrity(exception, request);

        assertError(response, HttpStatus.CONFLICT, "Task data conflicts with an existing record");
    }

    @Test
    void hidesUnexpectedExceptionDetails() {
        ResponseEntity<ApiError> response = handler.handleUnexpected(
                new IllegalStateException("sensitive internal detail"),
                request
        );

        assertError(response, HttpStatus.INTERNAL_SERVER_ERROR, "An unexpected error occurred");
        assertThat(response.getBody().message()).doesNotContain("sensitive internal detail");
    }

    private void assertError(ResponseEntity<ApiError> response, HttpStatus status, String message) {
        assertThat(response.getStatusCode()).isEqualTo(status);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().message()).isEqualTo(message);
        assertThat(response.getBody().path()).isEqualTo("/api/v1/tasks");
    }
}
