package com.example.taskapi.config;

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
        var runner = config.sampleTasks(service, repository, CLOCK);
        runner.run();
        var captor = ArgumentCaptor.forClass(CreateTaskRequest.class);
        verify(service, times(3)).create(captor.capture());
        assertThat(captor.getAllValues().get(0).dueDate()).isEqualTo(java.time.LocalDate.of(2030, 6, 22));
        when(repository.count()).thenReturn(3L);
        runner.run();
        verifyNoMoreInteractions(service);
    }
}
