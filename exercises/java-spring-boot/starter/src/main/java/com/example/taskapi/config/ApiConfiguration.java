package com.example.taskapi.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import java.time.Clock;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ApiConfiguration {
    @Bean
    public Clock clock() { return Clock.systemUTC(); }

    @Bean
    public OpenAPI taskApi() {
        return new OpenAPI().info(new Info().title("Task Management API").version("v1")
            .description("Task CRUD and search. Dates use ISO 8601; due-date validation uses UTC."));
    }
}
