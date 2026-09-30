package com.example.taskapi.exception;

import com.example.taskapi.dto.ApiError;
import jakarta.servlet.http.HttpServletRequest;
import java.time.Clock;
import java.util.LinkedHashMap;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.OptimisticLockingFailureException;
import org.springframework.http.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.context.request.ServletWebRequest;
import org.springframework.web.context.request.WebRequest;
import org.springframework.validation.method.ParameterErrors;
import org.springframework.web.method.annotation.HandlerMethodValidationException;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    private final Clock clock;
    public GlobalExceptionHandler(Clock clock) { this.clock = clock; }

    @ExceptionHandler(TaskNotFoundException.class)
    ResponseEntity<Object> notFound(TaskNotFoundException ex, HttpServletRequest request) {
        return error(HttpStatus.NOT_FOUND, ex.getMessage(), request.getRequestURI());
    }

    @ExceptionHandler(TaskConflictException.class)
    ResponseEntity<Object> conflict(TaskConflictException ex, HttpServletRequest request) {
        return error(HttpStatus.CONFLICT, ex.getMessage(), request.getRequestURI());
    }

    @ExceptionHandler(InvalidTaskException.class)
    ResponseEntity<Object> invalid(InvalidTaskException ex, HttpServletRequest request) {
        return error(HttpStatus.BAD_REQUEST, ex.getMessage(), request.getRequestURI());
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    ResponseEntity<Object> integrity(DataIntegrityViolationException ex, HttpServletRequest request) {
        log.warn("Task write violated a database constraint", ex);
        return error(HttpStatus.CONFLICT, "Task conflicts with existing data; titles must be unique", request.getRequestURI());
    }

    @ExceptionHandler(OptimisticLockingFailureException.class)
    ResponseEntity<Object> concurrent(OptimisticLockingFailureException ex, HttpServletRequest request) {
        return error(HttpStatus.CONFLICT, "Task changed concurrently; reload it and retry", request.getRequestURI());
    }

    @ExceptionHandler(Exception.class)
    ResponseEntity<Object> unexpected(Exception ex, HttpServletRequest request) {
        log.error("Unexpected API failure", ex);
        return error(HttpStatus.INTERNAL_SERVER_ERROR, "An unexpected error occurred", request.getRequestURI());
    }

    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
            HttpHeaders headers, HttpStatusCode status, WebRequest request) {
        Map<String, String> fields = new LinkedHashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(e -> fields.putIfAbsent(e.getField(), e.getDefaultMessage()));
        return new ResponseEntity<>(body(status, "Request validation failed", path(request), fields), headers, status);
    }

    @Override
    protected ResponseEntity<Object> handleHandlerMethodValidationException(HandlerMethodValidationException ex,
            HttpHeaders headers, HttpStatusCode status, WebRequest request) {
        Map<String, String> fields = new LinkedHashMap<>();
        ex.getParameterValidationResults().forEach(result -> {
            if (result instanceof ParameterErrors errors) {
                errors.getFieldErrors().forEach(e -> fields.putIfAbsent(e.getField(), e.getDefaultMessage()));
            } else {
                String name = result.getMethodParameter().getParameterName();
                result.getResolvableErrors().forEach(e -> fields.putIfAbsent(name, e.getDefaultMessage()));
            }
        });
        return new ResponseEntity<>(body(status, "Request validation failed", path(request), fields), headers, status);
    }

    @Override
    protected ResponseEntity<Object> handleExceptionInternal(Exception ex, Object ignored,
            HttpHeaders headers, HttpStatusCode status, WebRequest request) {
        String message = status.value() == 400 ? "Invalid request body or parameters" : HttpStatus.valueOf(status.value()).getReasonPhrase();
        return new ResponseEntity<>(body(status, message, path(request), Map.of()), headers, status);
    }

    private ResponseEntity<Object> error(HttpStatus status, String message, String path) {
        return ResponseEntity.status(status).body(body(status, message, path, Map.of()));
    }

    private ApiError body(HttpStatusCode status, String message, String path, Map<String, String> fields) {
        return new ApiError(clock.instant(), status.value(), HttpStatus.valueOf(status.value()).getReasonPhrase(), message, path, fields);
    }

    private String path(WebRequest request) {
        return ((ServletWebRequest) request).getRequest().getRequestURI();
    }
}
