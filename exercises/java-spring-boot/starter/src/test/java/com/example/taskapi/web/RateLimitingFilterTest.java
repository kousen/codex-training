package com.example.taskapi.web;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.taskapi.config.RateLimitProperties;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Duration;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

class RateLimitingFilterTest {

    private final ObjectMapper objectMapper = new ObjectMapper().findAndRegisterModules();

    @Test
    void returnsTooManyRequestsWhenClientExceedsLimit() throws Exception {
        RateLimitingFilter filter = new RateLimitingFilter(
                new RateLimitProperties(true, 1, Duration.ofMinutes(1)),
                objectMapper);
        MockHttpServletRequest firstRequest = apiRequest("192.0.2.10");
        MockHttpServletResponse firstResponse = new MockHttpServletResponse();
        MockHttpServletRequest secondRequest = apiRequest("192.0.2.10");
        MockHttpServletResponse secondResponse = new MockHttpServletResponse();

        filter.doFilter(firstRequest, firstResponse, new MockFilterChain());
        filter.doFilter(secondRequest, secondResponse, new MockFilterChain());

        assertThat(firstResponse.getStatus()).isEqualTo(HttpStatus.OK.value());
        assertThat(secondResponse.getStatus()).isEqualTo(HttpStatus.TOO_MANY_REQUESTS.value());
        assertThat(secondResponse.getContentAsString()).contains("Rate limit exceeded");
    }

    @Test
    void ignoresNonApiRequests() throws Exception {
        RateLimitingFilter filter = new RateLimitingFilter(
                new RateLimitProperties(true, 0, Duration.ofMinutes(1)),
                objectMapper);
        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/swagger-ui.html");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, new MockFilterChain());

        assertThat(response.getStatus()).isEqualTo(HttpStatus.OK.value());
    }

    @Test
    void doesNotLimitWhenDisabled() throws Exception {
        RateLimitingFilter filter = new RateLimitingFilter(
                new RateLimitProperties(false, 0, Duration.ofMinutes(1)),
                objectMapper);
        MockHttpServletRequest request = apiRequest("192.0.2.11");
        MockHttpServletResponse response = new MockHttpServletResponse();

        filter.doFilter(request, response, new MockFilterChain());

        assertThat(response.getStatus()).isEqualTo(HttpStatus.OK.value());
    }

    private MockHttpServletRequest apiRequest(String forwardedFor) {
        MockHttpServletRequest request = new MockHttpServletRequest("GET", "/api/v1/tasks");
        request.addHeader("X-Forwarded-For", forwardedFor);
        request.setRemoteAddr("127.0.0.1");
        return request;
    }
}
