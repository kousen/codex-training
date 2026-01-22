package com.example.taskapi.unit;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.example.taskapi.dto.CreateTaskRequest;
import com.example.taskapi.dto.TaskResponse;
import com.example.taskapi.dto.UpdateTaskRequest;
import com.example.taskapi.entity.Task;
import com.example.taskapi.entity.TaskPriority;
import com.example.taskapi.entity.TaskStatus;
import com.example.taskapi.exception.BadRequestException;
import com.example.taskapi.exception.ConflictException;
import com.example.taskapi.exception.ResourceNotFoundException;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.impl.TaskServiceImpl;
import java.time.Instant;
import java.time.LocalDate;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

@ExtendWith(MockitoExtension.class)
class TaskServiceImplTest {

    @Mock
    private TaskRepository taskRepository;

    @InjectMocks
    private TaskServiceImpl taskService;

    @Test
    void createRejectsDuplicateTitle() {
        CreateTaskRequest request = new CreateTaskRequest("Duplicate", null, null, null);

        when(taskRepository.existsByTitle("Duplicate")).thenReturn(true);

        assertThatThrownBy(() -> taskService.create(request))
                .isInstanceOf(ConflictException.class)
                .hasMessageContaining("unique");
    }

    @Test
    void createRejectsPastDueDate() {
        CreateTaskRequest request = new CreateTaskRequest("Task", null, null, LocalDate.now());

        when(taskRepository.existsByTitle("Task")).thenReturn(false);

        assertThatThrownBy(() -> taskService.create(request))
                .isInstanceOf(BadRequestException.class)
                .hasMessageContaining("future");
    }

    @Test
    void createDefaultsStatusAndPriority() {
        CreateTaskRequest request = new CreateTaskRequest("New Task", null, null, LocalDate.now().plusDays(3));

        Task saved = baseTask(1L, "New Task", TaskStatus.TODO, TaskPriority.MEDIUM);
        when(taskRepository.existsByTitle("New Task")).thenReturn(false);
        when(taskRepository.save(any(Task.class))).thenReturn(saved);

        TaskResponse response = taskService.create(request);

        assertThat(response.status()).isEqualTo(TaskStatus.TODO);
        assertThat(response.priority()).isEqualTo(TaskPriority.MEDIUM);
    }

    @Test
    void getByIdThrowsWhenMissing() {
        when(taskRepository.findById(42L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> taskService.getById(42L))
                .isInstanceOf(ResourceNotFoundException.class);
    }

    @Test
    void listReturnsMappedPage() {
        Task task = baseTask(1L, "List Task", TaskStatus.TODO, TaskPriority.LOW);
        Page<Task> page = new PageImpl<>(java.util.List.of(task));
        when(taskRepository.findAll(PageRequest.of(0, 20))).thenReturn(page);

        Page<TaskResponse> response = taskService.list(PageRequest.of(0, 20));

        assertThat(response.getContent()).hasSize(1);
        assertThat(response.getContent().get(0).title()).isEqualTo("List Task");
    }

    @Test
    void updateRejectsDuplicateTitleChange() {
        Task task = baseTask(1L, "Old Title", TaskStatus.TODO, TaskPriority.MEDIUM);
        UpdateTaskRequest request = new UpdateTaskRequest("New Title", null, null, null, null);

        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));
        when(taskRepository.existsByTitle("New Title")).thenReturn(true);

        assertThatThrownBy(() -> taskService.update(1L, request))
                .isInstanceOf(ConflictException.class)
                .hasMessageContaining("unique");
    }

    @Test
    void updateRejectsDoneToTodo() {
        Task task = baseTask(1L, "Done Task", TaskStatus.DONE, TaskPriority.MEDIUM);
        UpdateTaskRequest request = new UpdateTaskRequest(null, null, TaskStatus.TODO, null, null);

        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        assertThatThrownBy(() -> taskService.update(1L, request))
                .isInstanceOf(ConflictException.class)
                .hasMessageContaining("DONE");
    }

    @Test
    void updateRejectsPastDueDate() {
        Task task = baseTask(1L, "Due Task", TaskStatus.TODO, TaskPriority.MEDIUM);
        UpdateTaskRequest request = new UpdateTaskRequest(null, null, null, null, LocalDate.now());

        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        assertThatThrownBy(() -> taskService.update(1L, request))
                .isInstanceOf(BadRequestException.class)
                .hasMessageContaining("future");
    }

    @Test
    void deleteRejectsInProgress() {
        Task task = baseTask(1L, "Active Task", TaskStatus.IN_PROGRESS, TaskPriority.MEDIUM);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        assertThatThrownBy(() -> taskService.delete(1L))
                .isInstanceOf(ConflictException.class)
                .hasMessageContaining("IN_PROGRESS");
        verify(taskRepository, never()).delete(any(Task.class));
    }

    @Test
    void deleteRemovesTask() {
        Task task = baseTask(1L, "Delete Task", TaskStatus.TODO, TaskPriority.MEDIUM);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        taskService.delete(1L);

        verify(taskRepository).delete(eq(task));
    }

    private Task baseTask(Long id, String title, TaskStatus status, TaskPriority priority) {
        Task task = new Task();
        task.setId(id);
        task.setTitle(title);
        task.setStatus(status);
        task.setPriority(priority);
        task.setCreatedAt(Instant.now());
        task.setUpdatedAt(Instant.now());
        return task;
    }
}
