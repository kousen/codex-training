package com.example.taskapi.unit;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.UpdateTaskRequest;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.BusinessRuleException;
import com.example.taskapi.exception.DuplicateTaskTitleException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static com.example.taskapi.fixture.TaskFixtures.createRequest;
import static com.example.taskapi.fixture.TaskFixtures.task;
import static com.example.taskapi.fixture.TaskFixtures.updateRequest;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    private TaskRepository taskRepository;

    @InjectMocks
    private TaskService taskService;

    @Test
    void findsTaskById() {
        Task task = task(42L, Status.TODO);
        when(taskRepository.findById(42L)).thenReturn(Optional.of(task));

        TaskResponse response = taskService.findById(42L);

        assertThat(response.id()).isEqualTo(42L);
        assertThat(response.title()).isEqualTo("Prepare release");
    }

    @Test
    void reportsMissingTask() {
        when(taskRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.findById(99L))
                .isInstanceOf(TaskNotFoundException.class)
                .hasMessage("Task with id 99 was not found");
    }

    @Test
    void listsTasksWithPagination() {
        PageRequest pageable = PageRequest.of(0, 20);
        when(taskRepository.findAll(pageable))
                .thenReturn(new PageImpl<>(List.of(task(1L, Status.TODO)), pageable, 1));

        Page<TaskResponse> result = taskService.findAll(pageable);

        assertThat(result.getTotalElements()).isOne();
        assertThat(result.getContent()).extracting(TaskResponse::id).containsExactly(1L);
    }

    @Test
    void createsTaskWithDefaultsAndNormalizedTitle() {
        when(taskRepository.existsByTitleIgnoreCase("New task")).thenReturn(false);
        when(taskRepository.saveAndFlush(any(Task.class))).thenAnswer(invocation -> invocation.getArgument(0));

        TaskResponse response = taskService.create(createRequest("  New task  "));

        ArgumentCaptor<Task> captor = ArgumentCaptor.forClass(Task.class);
        verify(taskRepository).saveAndFlush(captor.capture());
        assertThat(captor.getValue().getTitle()).isEqualTo("New task");
        assertThat(response.status()).isEqualTo(Status.TODO);
        assertThat(response.priority().name()).isEqualTo("MEDIUM");
    }

    @Test
    void createsTaskWithExplicitStatusPriorityAndNoDueDate() {
        CreateTaskRequest request = new CreateTaskRequest(
                "Active task",
                "Already underway",
                Status.IN_PROGRESS,
                Priority.HIGH,
                null
        );
        when(taskRepository.existsByTitleIgnoreCase("Active task")).thenReturn(false);
        when(taskRepository.saveAndFlush(any(Task.class))).thenAnswer(invocation -> invocation.getArgument(0));

        TaskResponse response = taskService.create(request);

        assertThat(response.status()).isEqualTo(Status.IN_PROGRESS);
        assertThat(response.priority()).isEqualTo(Priority.HIGH);
        assertThat(response.dueDate()).isNull();
    }

    @Test
    void rejectsDuplicateTitleOnCreate() {
        when(taskRepository.existsByTitleIgnoreCase("New task")).thenReturn(true);

        assertThatThrownBy(() -> taskService.create(createRequest("New task")))
                .isInstanceOf(DuplicateTaskTitleException.class)
                .hasMessageContaining("New task");

        verify(taskRepository, never()).saveAndFlush(any());
    }

    @Test
    void rejectsNonFutureDueDateOnCreate() {
        CreateTaskRequest request = new CreateTaskRequest(
                "New task",
                null,
                null,
                null,
                LocalDate.now()
        );
        when(taskRepository.existsByTitleIgnoreCase("New task")).thenReturn(false);

        assertThatThrownBy(() -> taskService.create(request))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessage("Due date must be in the future");
    }

    @Test
    void updatesTask() {
        Task task = task(1L, Status.TODO);
        UpdateTaskRequest request = updateRequest(Status.IN_PROGRESS);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));
        when(taskRepository.existsByTitleIgnoreCaseAndIdNot("Prepare release", 1L)).thenReturn(false);
        when(taskRepository.saveAndFlush(task)).thenReturn(task);

        TaskResponse result = taskService.update(1L, request);

        assertThat(result.status()).isEqualTo(Status.IN_PROGRESS);
        assertThat(result.description()).isEqualTo("Updated checklist");
    }

    @Test
    void rejectsDuplicateTitleOnUpdate() {
        Task task = task(1L, Status.TODO);
        UpdateTaskRequest request = new UpdateTaskRequest(
                "Existing title",
                "Updated checklist",
                Status.IN_PROGRESS,
                Priority.MEDIUM,
                null
        );
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));
        when(taskRepository.existsByTitleIgnoreCaseAndIdNot("Existing title", 1L)).thenReturn(true);

        assertThatThrownBy(() -> taskService.update(1L, request))
                .isInstanceOf(DuplicateTaskTitleException.class)
                .hasMessageContaining("Existing title");

        verify(taskRepository, never()).saveAndFlush(any());
    }

    @Test
    void preventsDoneTaskReturningToTodo() {
        Task task = task(1L, Status.DONE);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));
        when(taskRepository.existsByTitleIgnoreCaseAndIdNot("Prepare release", 1L)).thenReturn(false);

        assertThatThrownBy(() -> taskService.update(1L, updateRequest(Status.TODO)))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessage("A DONE task cannot be changed back to TODO");
    }

    @Test
    void allowsDoneTaskToMoveToInProgress() {
        Task task = task(1L, Status.DONE);
        UpdateTaskRequest request = updateRequest(Status.IN_PROGRESS);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));
        when(taskRepository.existsByTitleIgnoreCaseAndIdNot("Prepare release", 1L)).thenReturn(false);
        when(taskRepository.saveAndFlush(task)).thenReturn(task);

        TaskResponse response = taskService.update(1L, request);

        assertThat(response.status()).isEqualTo(Status.IN_PROGRESS);
    }

    @Test
    void preventsDeletingInProgressTask() {
        Task task = task(1L, Status.IN_PROGRESS);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        assertThatThrownBy(() -> taskService.delete(1L))
                .isInstanceOf(BusinessRuleException.class)
                .hasMessage("An IN_PROGRESS task cannot be deleted");

        verify(taskRepository, never()).delete(any());
    }

    @Test
    void deletesTodoTask() {
        Task task = task(1L, Status.TODO);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        taskService.delete(1L);

        verify(taskRepository).delete(task);
    }

    @Test
    void searchesTitlesAndDescriptions() {
        PageRequest pageable = PageRequest.of(0, 20);
        when(taskRepository.findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase(
                "release", "release", pageable
        )).thenReturn(new PageImpl<>(List.of(task(1L, Status.TODO))));

        Page<TaskResponse> result = taskService.search("  release ", pageable);

        assertThat(result.getContent()).extracting(TaskResponse::id).containsExactly(1L);
    }
}
