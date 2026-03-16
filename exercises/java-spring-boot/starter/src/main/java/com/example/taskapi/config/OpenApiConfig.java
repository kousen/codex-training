package com.example.taskapi.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.servers.Server;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "Task Management API",
                version = "v1",
                description = "REST API for managing tasks with validation and business rules",
                contact = @Contact(name = "Task API Team")
        ),
        servers = @Server(url = "/", description = "Default server")
)
public class OpenApiConfig {
}
