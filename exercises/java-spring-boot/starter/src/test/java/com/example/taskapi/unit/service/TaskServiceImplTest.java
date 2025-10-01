package com.example.taskapi.unit.service;

import static com.example.taskapi.builder.TaskBuilder.aTask;
import static com.example.taskapi.builder.TaskCreateRequestBuilder.aTaskCreateRequest;
import static com.example.taskapi.builder.TaskUpdateRequestBuilder.aTaskUpdateRequest;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.exception.InvalidTaskStateException;
import com.example.taskapi.exception.TaskConflictException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.impl.TaskServiceImpl;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

@ExtendWith(MockitoExtension.class)
class TaskServiceImplTest {

    private static final Instant FIXED_INSTANT = Instant.parse("2024-01-01T10:00:00Z");

    @Mock
    private TaskRepository taskRepository;

    private MutableClock clock;
    private TaskServiceImpl taskService;

    @BeforeEach
    void setUp() {
        clock = new MutableClock(FIXED_INSTANT, ZoneOffset.UTC);
        taskService = new TaskServiceImpl(taskRepository, clock);
    }

    @Test
    void createTask_shouldPersistWithDefaults() {
        TaskCreateRequest request = aTaskCreateRequest()
                .withTitle("  Unique Title  ")
                .withPriority(null)
                .withDueDate(LocalDate.of(2024, 1, 10))
                .build();

        when(taskRepository.findByTitleIgnoreCase("Unique Title"))
                .thenReturn(Optional.empty());
        when(taskRepository.save(any(Task.class))).thenAnswer(invocation -> {
            Task task = invocation.getArgument(0);
            task.setId(1L);
            return task;
        });

        TaskResponse response = taskService.createTask(request);

        ArgumentCaptor<Task> taskCaptor = ArgumentCaptor.forClass(Task.class);
        verify(taskRepository).save(taskCaptor.capture());
        Task savedTask = taskCaptor.getValue();

        assertThat(savedTask.getTitle()).isEqualTo("Unique Title");
        assertThat(savedTask.getStatus()).isEqualTo(TaskStatus.TODO);
        assertThat(savedTask.getPriority()).isEqualTo(TaskPriority.MEDIUM);
        assertThat(savedTask.getCreatedAt()).isEqualTo(FIXED_INSTANT);
        assertThat(savedTask.getUpdatedAt()).isEqualTo(FIXED_INSTANT);

        assertThat(response.id()).isEqualTo(1L);
        assertThat(response.status()).isEqualTo(TaskStatus.TODO);
        assertThat(response.priority()).isEqualTo(TaskPriority.MEDIUM);
    }

    @Test
    void createTask_shouldThrowWhenTitleNotUnique() {
        TaskCreateRequest request = aTaskCreateRequest().withTitle("Duplicate").build();

        when(taskRepository.findByTitleIgnoreCase("Duplicate"))
                .thenReturn(Optional.of(aTask().withTitle("Duplicate").build()));

        assertThatThrownBy(() -> taskService.createTask(request))
                .isInstanceOf(TaskConflictException.class)
                .hasMessage("Task title must be unique");
    }

    @Test
    void createTask_shouldThrowWhenDueDateNotFuture() {
        TaskCreateRequest request = aTaskCreateRequest()
                .withDueDate(LocalDate.of(2023, 12, 31))
                .build();

        when(taskRepository.findByTitleIgnoreCase("New Task"))
                .thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.createTask(request))
                .isInstanceOf(InvalidTaskStateException.class)
                .hasMessage("Due date must be in the future");
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1})
    void createTask_shouldRejectNonFutureDueDates(int offsetDays) {
        LocalDate dueDate = LocalDate.now(clock).plusDays(offsetDays);
        TaskCreateRequest request = aTaskCreateRequest()
                .withDueDate(dueDate)
                .build();

        when(taskRepository.findByTitleIgnoreCase("New Task"))
                .thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.createTask(request))
                .isInstanceOf(InvalidTaskStateException.class)
                .hasMessage("Due date must be in the future");
    }

    @Test
    void updateTask_shouldApplyChanges() {
        Task existingTask = aTask()
                .withId(1L)
                .withStatus(TaskStatus.IN_PROGRESS)
                .withPriority(TaskPriority.LOW)
                .withTitle("Original Title")
                .withUpdatedAt(FIXED_INSTANT.minusSeconds(60))
                .build();

        TaskUpdateRequest request = aTaskUpdateRequest()
                .withTitle("Updated Title")
                .withPriority(TaskPriority.HIGH)
                .withStatus(TaskStatus.DONE)
                .withDueDate(LocalDate.of(2024, 1, 20))
                .build();

        clock.setInstant(FIXED_INSTANT.plusSeconds(120));
        when(taskRepository.findById(1L)).thenReturn(Optional.of(existingTask));
        when(taskRepository.findByTitleIgnoreCaseAndIdNot("Updated Title", 1L)).thenReturn(Optional.empty());
        when(taskRepository.save(existingTask)).thenReturn(existingTask);

        TaskResponse response = taskService.updateTask(1L, request);

        assertThat(response.title()).isEqualTo("Updated Title");
        assertThat(response.status()).isEqualTo(TaskStatus.DONE);
        assertThat(response.priority()).isEqualTo(TaskPriority.HIGH);
        assertThat(existingTask.getUpdatedAt()).isEqualTo(FIXED_INSTANT.plusSeconds(120));

        verify(taskRepository).save(existingTask);
    }

    @Test
    void updateTask_shouldThrowWhenTitleConflicts() {
        Task existingTask = aTask().withId(1L).build();
        TaskUpdateRequest request = aTaskUpdateRequest().withTitle("Duplicate").build();

        when(taskRepository.findById(1L)).thenReturn(Optional.of(existingTask));
        when(taskRepository.findByTitleIgnoreCaseAndIdNot("Duplicate", 1L))
                .thenReturn(Optional.of(aTask().withId(2L).withTitle("Duplicate").build()));

        assertThatThrownBy(() -> taskService.updateTask(1L, request))
                .isInstanceOf(TaskConflictException.class)
                .hasMessage("Task title must be unique");
    }

    @Test
    void updateTask_shouldThrowWhenChangingDoneBackToTodo() {
        Task existingTask = aTask()
                .withId(1L)
                .withStatus(TaskStatus.DONE)
                .build();
        TaskUpdateRequest request = aTaskUpdateRequest()
                .withTitle("Still Done")
                .withStatus(TaskStatus.TODO)
                .build();

        when(taskRepository.findById(1L)).thenReturn(Optional.of(existingTask));
        when(taskRepository.findByTitleIgnoreCaseAndIdNot("Still Done", 1L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.updateTask(1L, request))
                .isInstanceOf(InvalidTaskStateException.class)
                .hasMessage("Cannot change a completed task back to TODO");
    }

    @Test
    void deleteTask_shouldThrowWhenInProgress() {
        Task task = aTask().withStatus(TaskStatus.IN_PROGRESS).withId(5L).build();
        when(taskRepository.findById(5L)).thenReturn(Optional.of(task));

        assertThatThrownBy(() -> taskService.deleteTask(5L))
                .isInstanceOf(InvalidTaskStateException.class)
                .hasMessage("Cannot delete task in progress");
    }

    @Test
    void deleteTask_shouldRemoveEntity() {
        Task task = aTask().withId(7L).build();
        when(taskRepository.findById(7L)).thenReturn(Optional.of(task));

        taskService.deleteTask(7L);

        verify(taskRepository).delete(task);
    }

    @Test
    void getTask_shouldThrowWhenNotFound() {
        when(taskRepository.findById(anyLong())).thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.getTask(42L))
                .isInstanceOf(TaskNotFoundException.class)
                .hasMessage("Task with id 42 not found");
    }

    @Test
    void getTasks_shouldReturnPagedResults() {
        when(taskRepository.findAll(any(Pageable.class)))
                .thenReturn(org.springframework.data.domain.Page.empty());

        taskService.getTasks(PageRequest.of(0, 20));

        verify(taskRepository, times(1)).findAll(any(Pageable.class));
    }

    private static class MutableClock extends Clock {
        private Instant instant;
        private ZoneId zone;

        MutableClock(Instant instant, ZoneId zone) {
            this.instant = instant;
            this.zone = zone;
        }

        void setInstant(Instant instant) {
            this.instant = instant;
        }

        @Override
        public ZoneId getZone() {
            return zone;
        }

        @Override
        public Clock withZone(ZoneId zone) {
            return new MutableClock(instant, zone);
        }

        @Override
        public Instant instant() {
            return instant;
        }
    }
}
