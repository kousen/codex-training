package com.example.taskapi.unit;

import com.example.taskapi.config.SampleDataConfiguration;
import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import static com.example.taskapi.support.TaskFixtures.*;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

class SampleDataConfigurationTest {
    @Test void seedsOnlyEmptyDatabaseWithFutureDueDate() throws Exception {
        var repository = mock(TaskRepository.class);
        var service = mock(TaskService.class);
        var config = new SampleDataConfiguration();
        // Invoke the package-private @Bean factory through Spring's reflection helper.
        var runner = (org.springframework.boot.CommandLineRunner) org.springframework.test.util.ReflectionTestUtils.invokeMethod(
            config, "sampleTasks", service, repository, CLOCK);
        runner.run();
        var captor = ArgumentCaptor.forClass(CreateTaskRequest.class);
        verify(service, times(3)).create(captor.capture());
        assertThat(captor.getAllValues().get(0).dueDate()).isEqualTo(java.time.LocalDate.of(2030, 6, 22));
        when(repository.count()).thenReturn(3L);
        runner.run();
        verifyNoMoreInteractions(service);
    }
}
