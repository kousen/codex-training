package com.example.taskapi.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.tags.Tag;
import java.util.List;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    public static final String BASIC_AUTH_SCHEME = "basicAuth";

    @Bean
    public OpenAPI taskManagementOpenAPI() {
        return new OpenAPI()
                .components(new Components()
                        .addSecuritySchemes(BASIC_AUTH_SCHEME, new SecurityScheme()
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("basic")
                                .description("HTTP Basic authentication for write operations. "
                                        + "Use admin/changeme in the local development profile.")))
                .info(new Info()
                        .title("Task Management API")
                        .version("v1")
                        .description("""
                                REST API for managing tasks in the Codex CLI Spring Boot lab.

                                The API uses JSON request and response bodies, ISO 8601 dates,
                                and predictable HTTP status codes for validation, not-found,
                                and business-rule conflicts.
                                """)
                        .contact(new Contact()
                                .name("Codex CLI Training")
                                .url("https://github.com/kousen/codex-training"))
                        .license(new License()
                                .name("Training Materials")))
                .servers(List.of(
                        new Server()
                                .url("http://localhost:8080")
                                .description("Local development server")))
                .tags(List.of(new Tag()
                        .name("Tasks")
                        .description("Create, read, update, search, and delete task resources")));
    }
}
