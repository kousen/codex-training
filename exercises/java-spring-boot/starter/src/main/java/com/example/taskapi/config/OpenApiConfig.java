package com.example.taskapi.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI taskApiOpenAPI() {
        return new OpenAPI()
                .components(new Components())
                .info(new Info()
                        .title("Task Management API")
                        .description("REST API for managing tasks")
                        .version("1.0.0")
                        .contact(new Contact().name("Task API Team").email("support@example.com"))
                        .license(new License().name("Apache 2.0")));
    }
}
