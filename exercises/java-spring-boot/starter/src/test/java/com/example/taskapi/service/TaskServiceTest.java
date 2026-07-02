package com.example.taskapi.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.example.taskapi.entity.Priority;
import com.example.taskapi.entity.Status;
import com.example.taskapi.entity.Task;
import com.example.taskapi.exception.BusinessRuleViolationException;
import com.example.taskapi.exception.DuplicateTaskTitleException;
import com.example.taskapi.exception.TaskNotFoundException;
import com.example.taskapi.exception.TaskValidationException;
import com.example.taskapi.repository.TaskRepository;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    private TaskRepository taskRepository;

    private TaskService taskService;

    @BeforeEach
    void setUp() {
        taskService = new TaskService(taskRepository);
    }

    @Test
    void createTaskAppliesDefaultsAndSaves() {
        Task task = Task.updatePatch("Write tests", "Cover service logic", null, null, LocalDate.now().plusDays(7));
        when(taskRepository.findByTitleIgnoreCase("Write tests")).thenReturn(Optional.empty());
        when(taskRepository.save(task)).thenReturn(task);

        Task created = taskService.createTask(task);

        assertThat(created.getStatus()).isEqualTo(Status.TODO);
        assertThat(created.getPriority()).isEqualTo(Priority.MEDIUM);
        verify(taskRepository).save(task);
    }

    @Test
    void createTaskRejectsDuplicateTitle() {
        Task existing = persistedTask(1L, "Write tests", Status.TODO);
        Task duplicate = new Task("Write tests", null, Status.TODO, Priority.MEDIUM, LocalDate.now().plusDays(3));
        when(taskRepository.findByTitleIgnoreCase("Write tests")).thenReturn(Optional.of(existing));

        assertThatThrownBy(() -> taskService.createTask(duplicate))
                .isInstanceOf(DuplicateTaskTitleException.class)
                .hasMessageContaining("Write tests");

        verify(taskRepository, never()).save(any());
    }

    @Test
    void createTaskRejectsMissingTitle() {
        Task task = Task.updatePatch(" ", null, null, null, LocalDate.now().plusDays(1));

        assertThatThrownBy(() -> taskService.createTask(task))
                .isInstanceOf(TaskValidationException.class)
                .hasMessage("Task title is required");

        verify(taskRepository, never()).save(any());
    }

    @Test
    void createTaskRejectsPastDueDate() {
        Task task = new Task("Past task", null, Status.TODO, Priority.MEDIUM, LocalDate.now().minusDays(1));

        assertThatThrownBy(() -> taskService.createTask(task))
                .isInstanceOf(TaskValidationException.class)
                .hasMessage("Due date must be in the future");
    }

    @Test
    void getTaskByIdReturnsTaskWhenPresent() {
        Task task = persistedTask(1L, "Existing task", Status.TODO);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        assertThat(taskService.getTaskById(1L)).isSameAs(task);
    }

    @Test
    void getTaskByIdThrowsWhenMissing() {
        when(taskRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.getTaskById(99L))
                .isInstanceOf(TaskNotFoundException.class)
                .hasMessageContaining("99");
    }

    @Test
    void updateTaskChangesAllowedFields() {
        Task existing = persistedTask(1L, "Original", Status.TODO);
        Task updates = Task.updatePatch(
                "Updated",
                "New description",
                Status.IN_PROGRESS,
                Priority.HIGH,
                LocalDate.now().plusDays(10));
        when(taskRepository.findById(1L)).thenReturn(Optional.of(existing));
        when(taskRepository.findByTitleIgnoreCase("Updated")).thenReturn(Optional.empty());
        when(taskRepository.save(existing)).thenReturn(existing);

        Task updated = taskService.updateTask(1L, updates);

        assertThat(updated.getTitle()).isEqualTo("Updated");
        assertThat(updated.getDescription()).isEqualTo("New description");
        assertThat(updated.getStatus()).isEqualTo(Status.IN_PROGRESS);
        assertThat(updated.getPriority()).isEqualTo(Priority.HIGH);
        assertThat(updated.getDueDate()).isEqualTo(LocalDate.now().plusDays(10));
    }

    @Test
    void updateTaskAllowsKeepingSameTitle() {
        Task existing = persistedTask(1L, "Same title", Status.TODO);
        Task updates = Task.updatePatch("Same title", null, null, null, null);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(existing));
        when(taskRepository.findByTitleIgnoreCase("Same title")).thenReturn(Optional.of(existing));
        when(taskRepository.save(existing)).thenReturn(existing);

        taskService.updateTask(1L, updates);

        verify(taskRepository).save(existing);
    }

    @Test
    void updateTaskRejectsDoneBackToTodo() {
        Task existing = persistedTask(1L, "Done task", Status.DONE);
        Task updates = Task.updatePatch(null, null, Status.TODO, null, null);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(existing));

        assertThatThrownBy(() -> taskService.updateTask(1L, updates))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessage("Cannot change DONE task back to TODO");

        verify(taskRepository, never()).save(any());
    }

    @Test
    void deleteTaskDeletesNonInProgressTask() {
        Task task = persistedTask(1L, "Done task", Status.DONE);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        taskService.deleteTask(1L);

        verify(taskRepository).delete(task);
    }

    @Test
    void deleteTaskRejectsInProgressTask() {
        Task task = persistedTask(1L, "Active task", Status.IN_PROGRESS);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        assertThatThrownBy(() -> taskService.deleteTask(1L))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessage("Cannot delete task with status IN_PROGRESS");

        verify(taskRepository, never()).delete(any());
    }

    @Test
    void searchTasksNormalizesBlankKeyword() {
        LocalDate dueBefore = LocalDate.now().plusDays(30);
        when(taskRepository.search(null, Status.TODO, Priority.MEDIUM, dueBefore, null)).thenReturn(List.of());

        taskService.searchTasks("   ", Status.TODO, Priority.MEDIUM, dueBefore, null);

        verify(taskRepository).search(null, Status.TODO, Priority.MEDIUM, dueBefore, null);
    }

    @Test
    void getAllTasksDelegatesToRepository() {
        when(taskRepository.findAll()).thenReturn(List.of(persistedTask(1L, "Task", Status.TODO)));

        assertThat(taskService.getAllTasks()).hasSize(1);
    }

    @Test
    void getTasksByStatusDelegatesToRepository() {
        when(taskRepository.findByStatus(Status.TODO)).thenReturn(List.of(persistedTask(1L, "Task", Status.TODO)));

        assertThat(taskService.getTasksByStatus(Status.TODO)).hasSize(1);
    }

    @Test
    void getTasksByPriorityDelegatesToRepository() {
        when(taskRepository.findByPriority(Priority.HIGH)).thenReturn(List.of(persistedTask(1L, "Task", Status.TODO)));

        assertThat(taskService.getTasksByPriority(Priority.HIGH)).hasSize(1);
    }

    @Test
    void updateTaskRejectsLongDescription() {
        Task existing = persistedTask(1L, "Task", Status.TODO);
        Task updates = Task.updatePatch(null, "x".repeat(501), null, null, null);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(existing));

        assertThatThrownBy(() -> taskService.updateTask(1L, updates))
                .isInstanceOf(TaskValidationException.class)
                .hasMessage("Task description must be 500 characters or fewer");
    }

    private Task persistedTask(Long id, String title, Status status) {
        Task task = new Task(title, "Description", status, Priority.MEDIUM, LocalDate.now().plusDays(7));
        setId(task, id);
        return task;
    }

    private void setId(Task task, Long id) {
        try {
            java.lang.reflect.Field idField = Task.class.getDeclaredField("id");
            idField.setAccessible(true);
            idField.set(task, id);
        } catch (ReflectiveOperationException exception) {
            throw new IllegalStateException("Unable to set task id for test", exception);
        }
    }
}
