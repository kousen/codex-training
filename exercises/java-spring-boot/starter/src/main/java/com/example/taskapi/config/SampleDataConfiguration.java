package com.example.taskapi.config;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.entity.*;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import java.time.Clock;
import java.time.LocalDate;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnProperty(name = "app.sample-data.enabled", havingValue = "true")
public class SampleDataConfiguration {
    @Bean
    CommandLineRunner sampleTasks(TaskService service, TaskRepository repository, Clock clock) {
        return args -> {
            if (repository.count() == 0) {
                service.create(new CreateTaskRequest("Prepare workshop", "Review the API exercises", null, TaskPriority.HIGH, LocalDate.now(clock).plusDays(7)));
                service.create(new CreateTaskRequest("Implement task API", "Build and test CRUD operations", TaskStatus.IN_PROGRESS, null, null));
                service.create(new CreateTaskRequest("Configure project", "Set up Maven and Spring Boot", TaskStatus.DONE, TaskPriority.LOW, null));
            }
        };
    }
}
