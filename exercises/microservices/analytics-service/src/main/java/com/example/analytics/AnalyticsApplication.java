package com.example.analytics;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class AnalyticsApplication {

    public static void main(String[] args) {
        SpringApplication.run(AnalyticsApplication.class, args);
    }

    @GetMapping("/health")
    public HealthResponse health() {
        return new HealthResponse("healthy", "analytics-service");
    }

    // TODO: Implement analytics endpoints using Codex
    // - GET /api/analytics/orders/daily
    // - GET /api/analytics/revenue/monthly
    // - GET /api/analytics/users/growth
    // - WebSocket /api/analytics/realtime

    record HealthResponse(String status, String service) {}
}