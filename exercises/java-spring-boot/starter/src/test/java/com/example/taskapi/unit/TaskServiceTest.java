package com.example.taskapi.unit;

import static com.example.taskapi.entity.TaskPriority.MEDIUM;
import static com.example.taskapi.entity.TaskStatus.DONE;
import static com.example.taskapi.entity.TaskStatus.IN_PROGRESS;
import static com.example.taskapi.entity.TaskStatus.TODO;
import static com.example.taskapi.fixture.TaskTestData.createRequest;
import static com.example.taskapi.fixture.TaskTestData.task;
import static com.example.taskapi.fixture.TaskTestData.updateRequest;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskMapper;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.DuplicateTaskTitleException;
import com.example.taskapi.exception.TaskConflictException;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import java.time.Instant;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    private TaskRepository taskRepository;

    private TaskService taskService;

    @BeforeEach
    void setUp() {
        taskService = new TaskService(taskRepository, new TaskMapper());
    }

    @Test
    void createTaskAppliesDefaultStatusAndPriority() {
        TaskCreateRequest request = createRequest("Plan lab");
        when(taskRepository.existsByTitleIgnoreCase("Plan lab")).thenReturn(false);
        when(taskRepository.save(any(Task.class))).thenAnswer(invocation -> {
            Task task = invocation.getArgument(0);
            task.setId(1L);
            task.setCreatedAt(Instant.parse("2026-05-04T12:00:00Z"));
            task.setUpdatedAt(Instant.parse("2026-05-04T12:00:00Z"));
            return task;
        });

        TaskResponse response = taskService.createTask(request);

        assertThat(response.id()).isEqualTo(1L);
        assertThat(response.status()).isEqualTo(TODO);
        assertThat(response.priority()).isEqualTo(MEDIUM);

        ArgumentCaptor<Task> taskCaptor = ArgumentCaptor.forClass(Task.class);
        verify(taskRepository).save(taskCaptor.capture());
        assertThat(taskCaptor.getValue().getTitle()).isEqualTo("Plan lab");
    }

    @Test
    void createTaskRejectsDuplicateTitle() {
        TaskCreateRequest request = createRequest("Plan lab");
        when(taskRepository.existsByTitleIgnoreCase("Plan lab")).thenReturn(true);

        assertThatThrownBy(() -> taskService.createTask(request))
                .isInstanceOf(DuplicateTaskTitleException.class)
                .hasMessageContaining("Plan lab");

        verify(taskRepository, never()).save(any(Task.class));
    }

    @Test
    void updateTaskRejectsDoneTaskReturningToTodo() {
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task(1L, "Publish notes", DONE)));
        when(taskRepository.existsByTitleIgnoreCaseAndIdNot("Publish notes", 1L)).thenReturn(false);

        assertThatThrownBy(() -> taskService.updateTask(1L, updateRequest("Publish notes", TODO)))
                .isInstanceOf(TaskConflictException.class)
                .hasMessageContaining("DONE task back to TODO");
    }

    @Test
    void deleteTaskRejectsInProgressTask() {
        Task task = task(1L, "Review code", IN_PROGRESS);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        assertThatThrownBy(() -> taskService.deleteTask(1L))
                .isInstanceOf(TaskConflictException.class)
                .hasMessageContaining("IN_PROGRESS");

        verify(taskRepository, never()).delete(task);
    }

    @Test
    void searchTaskRejectsBlankQuery() {
        assertThatThrownBy(() -> taskService.searchTasks("  ", org.springframework.data.domain.Pageable.unpaged()))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Search query is required");
    }
}
