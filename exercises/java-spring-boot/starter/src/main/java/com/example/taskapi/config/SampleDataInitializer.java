package com.example.taskapi.config;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.repository.TaskRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.LocalDate;
import java.util.List;

@Configuration
public class SampleDataInitializer {

    @Bean
    CommandLineRunner loadSampleData(TaskRepository taskRepository) {
        return args -> {
            if (taskRepository.count() > 0) {
                return;
            }

            Task backlog = new Task();
            backlog.setTitle("Prepare project backlog");
            backlog.setDescription("Break the API work into initial stories");
            backlog.setStatus(Status.TODO);
            backlog.setPriority(Priority.HIGH);
            backlog.setDueDate(LocalDate.now().plusDays(3));

            Task docs = new Task();
            docs.setTitle("Write Swagger descriptions");
            docs.setDescription("Document the endpoints and error responses");
            docs.setStatus(Status.IN_PROGRESS);
            docs.setPriority(Priority.MEDIUM);
            docs.setDueDate(LocalDate.now().plusDays(5));

            Task tests = new Task();
            tests.setTitle("Add integration tests");
            tests.setDescription("Cover CRUD flows with MockMvc");
            tests.setStatus(Status.DONE);
            tests.setPriority(Priority.MEDIUM);
            tests.setDueDate(LocalDate.now().plusDays(7));

            taskRepository.saveAll(List.of(backlog, docs, tests));
        };
    }
}
