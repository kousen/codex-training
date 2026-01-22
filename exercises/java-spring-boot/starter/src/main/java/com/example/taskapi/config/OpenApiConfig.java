package com.example.taskapi.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import io.swagger.v3.oas.annotations.servers.Server;
import io.swagger.v3.oas.models.ExternalDocumentation;
import io.swagger.v3.oas.models.OpenAPI;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "Task Management API",
                description = "REST API for managing tasks with validation and business rules.",
                version = "v1",
                contact = @Contact(name = "Task API Support", email = "support@example.com"),
                license = @License(name = "Apache 2.0", url = "https://www.apache.org/licenses/LICENSE-2.0.html")
        ),
        servers = {
                @Server(url = "http://localhost:8080", description = "Local development")
        }
)
public class OpenApiConfig {

    @Bean
    public OpenAPI taskApiOpenApi() {
        return new OpenAPI()
                .externalDocs(new ExternalDocumentation()
                        .description("Project README")
                        .url("https://example.com/docs"));
    }
}
