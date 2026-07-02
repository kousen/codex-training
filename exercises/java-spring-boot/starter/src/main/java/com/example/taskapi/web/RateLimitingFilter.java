package com.example.taskapi.web;

import com.example.taskapi.config.RateLimitProperties;
import com.example.taskapi.exception.ErrorResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.time.Clock;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.web.filter.OncePerRequestFilter;

public class RateLimitingFilter extends OncePerRequestFilter {

    private final RateLimitProperties properties;
    private final ObjectMapper objectMapper;
    private final Clock clock;
    private final Map<String, ClientWindow> clientWindows = new ConcurrentHashMap<>();

    public RateLimitingFilter(RateLimitProperties properties, ObjectMapper objectMapper) {
        this(properties, objectMapper, Clock.systemUTC());
    }

    RateLimitingFilter(RateLimitProperties properties, ObjectMapper objectMapper, Clock clock) {
        this.properties = properties;
        this.objectMapper = objectMapper;
        this.clock = clock;
    }

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {
        if (!properties.enabled() || !request.getRequestURI().startsWith("/api/v1/")) {
            filterChain.doFilter(request, response);
            return;
        }

        ClientWindow window = clientWindows.computeIfAbsent(clientKey(request), ignored -> new ClientWindow(now()));
        if (!window.tryAcquire(now(), properties.window().toMillis(), properties.requests())) {
            writeRateLimitResponse(request, response);
            return;
        }

        filterChain.doFilter(request, response);
    }

    private long now() {
        return clock.millis();
    }

    private String clientKey(HttpServletRequest request) {
        String forwardedFor = request.getHeader("X-Forwarded-For");
        if (forwardedFor != null && !forwardedFor.isBlank()) {
            return forwardedFor.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }

    private void writeRateLimitResponse(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        ErrorResponse errorResponse = ErrorResponse.of(
                HttpStatus.TOO_MANY_REQUESTS.value(),
                HttpStatus.TOO_MANY_REQUESTS.getReasonPhrase(),
                "Rate limit exceeded. Try again later.",
                request.getRequestURI());
        objectMapper.writeValue(response.getWriter(), errorResponse);
    }

    private static final class ClientWindow {

        private long windowStartedAt;
        private int requestCount;

        private ClientWindow(long windowStartedAt) {
            this.windowStartedAt = windowStartedAt;
        }

        private synchronized boolean tryAcquire(long now, long windowMillis, int limit) {
            if (now - windowStartedAt >= windowMillis) {
                windowStartedAt = now;
                requestCount = 0;
            }
            if (requestCount >= limit) {
                return false;
            }
            requestCount++;
            return true;
        }
    }
}
