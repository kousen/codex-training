package com.example.taskapi.unit.service;

import com.example.taskapi.dto.TaskCreateRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.TaskUpdateRequest;
import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.BusinessRuleViolationException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import com.example.taskapi.support.TaskFixtures;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    private TaskRepository taskRepository;

    @InjectMocks
    private TaskService taskService;

    private Task existingTask;

    @BeforeEach
    void setUp() {
        existingTask = TaskFixtures.task(1L, "Existing task", Status.TODO, Priority.MEDIUM);
    }

    @Test
    void createTaskAppliesDefaultsWhenStatusAndPriorityAreMissing() {
        TaskCreateRequest request = TaskFixtures.createRequest("New task");
        when(taskRepository.existsByTitleIgnoreCase("New task")).thenReturn(false);
        when(taskRepository.save(any(Task.class))).thenAnswer(invocation -> {
            Task task = invocation.getArgument(0);
            task.setId(10L);
            return task;
        });

        TaskResponse response = taskService.createTask(request);

        ArgumentCaptor<Task> taskCaptor = ArgumentCaptor.forClass(Task.class);
        verify(taskRepository).save(taskCaptor.capture());
        Task savedTask = taskCaptor.getValue();
        assertThat(savedTask.getStatus()).isEqualTo(Status.TODO);
        assertThat(savedTask.getPriority()).isEqualTo(Priority.MEDIUM);
        assertThat(savedTask.getTitle()).isEqualTo("New task");
        assertThat(response.id()).isEqualTo(10L);
    }

    @Test
    void createTaskRejectsDuplicateTitle() {
        TaskCreateRequest request = TaskFixtures.createRequest("Existing task");
        when(taskRepository.existsByTitleIgnoreCase("Existing task")).thenReturn(true);

        assertThatThrownBy(() -> taskService.createTask(request))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessage("Task title must be unique");

        verify(taskRepository, never()).save(any(Task.class));
    }

    @Test
    void createTaskRejectsPastDueDate() {
        TaskCreateRequest request = new TaskCreateRequest(
                "Past due",
                "Invalid due date",
                null,
                null,
                LocalDate.now().minusDays(1)
        );
        when(taskRepository.existsByTitleIgnoreCase("Past due")).thenReturn(false);

        assertThatThrownBy(() -> taskService.createTask(request))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessage("Due date must be in the future");
    }

    @Test
    void updateTaskRejectsDoneToTodoTransition() {
        existingTask.setStatus(Status.DONE);
        TaskUpdateRequest request = TaskFixtures.updateRequest("Existing task", Status.TODO, Priority.HIGH);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(existingTask));
        when(taskRepository.existsByTitleIgnoreCaseAndIdNot("Existing task", 1L)).thenReturn(false);

        assertThatThrownBy(() -> taskService.updateTask(1L, request))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessage("A DONE task cannot be moved back to TODO");
    }

    @Test
    void deleteTaskRejectsInProgressTask() {
        existingTask.setStatus(Status.IN_PROGRESS);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(existingTask));

        assertThatThrownBy(() -> taskService.deleteTask(1L))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessage("Task with status IN_PROGRESS cannot be deleted");

        verify(taskRepository, never()).delete(any(Task.class));
    }

    @Test
    void getTaskByIdThrowsWhenMissing() {
        when(taskRepository.findById(anyLong())).thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.getTaskById(99L))
                .isInstanceOf(TaskNotFoundException.class)
                .hasMessage("Task not found with id 99");
    }

    @Test
    void getAllTasksReturnsPagedResponses() {
        when(taskRepository.findAll(any(PageRequest.class))).thenReturn(new PageImpl<>(List.of(existingTask)));

        var page = taskService.getAllTasks(PageRequest.of(0, 20));

        assertThat(page.getContent()).hasSize(1);
        assertThat(page.getContent().get(0).title()).isEqualTo("Existing task");
    }
}
