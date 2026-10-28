package com.example.taskapi.unit;

import com.example.taskapi.dto.*;
import com.example.taskapi.entity.*;
import com.example.taskapi.exception.*;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Optional;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.*;
import static com.example.taskapi.TaskFixtures.*;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {
    @Mock TaskRepository repository;
    @InjectMocks TaskService service;

    @Test void createsWithDefaultsAndTrimsTitle() {
        when(repository.saveAndFlush(any())).thenAnswer(call -> call.getArgument(0));
        TaskResponse result = service.create(new TaskRequest("  New task  ", null, null, null, null));
        assertThat(result.title()).isEqualTo("New task");
        assertThat(result.status()).isEqualTo(Status.TODO);
        assertThat(result.priority()).isEqualTo(Priority.MEDIUM);
        assertThat(result.dueDate()).isNull();
        verify(repository).existsByTitle("New task");
    }

    @Test void createsWithExplicitValues() {
        when(repository.saveAndFlush(any())).thenAnswer(call -> call.getArgument(0));
        var result = service.create(request("New task", Status.IN_PROGRESS));
        assertThat(result.status()).isEqualTo(Status.IN_PROGRESS);
        assertThat(result.priority()).isEqualTo(Priority.HIGH);
        assertThat(result.description()).isEqualTo("Sample description");
        assertThat(result.dueDate()).isAfter(LocalDate.now());
    }

    @ParameterizedTest @ValueSource(ints = {-1, 0})
    void rejectsDueDateNotInFuture(int offset) {
        var request = new TaskRequest("New", null, null, null, LocalDate.now(ZoneOffset.UTC).plusDays(offset));
        assertThatThrownBy(() -> service.create(request)).isInstanceOf(IllegalArgumentException.class);
        verifyNoInteractions(repository);
    }

    @Test void rejectsDuplicateCreate() {
        when(repository.existsByTitle("New")).thenReturn(true);
        assertThatThrownBy(() -> service.create(request("New", Status.TODO)))
                .isInstanceOf(TaskConflictException.class);
        verify(repository, never()).saveAndFlush(any());
    }

    @Test void listsAndSearches() {
        Pageable pageable = PageRequest.of(0, 20);
        when(repository.findAll(pageable)).thenReturn(new PageImpl<>(List.of(task(Status.TODO))));
        when(repository.findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase("text", "text", pageable))
                .thenReturn(new PageImpl<>(List.of(task(Status.DONE))));
        assertThat(service.list(pageable).getContent()).hasSize(1);
        assertThat(service.search(" text ", pageable).getContent().get(0).status()).isEqualTo(Status.DONE);
    }

    @Test void getsTask() {
        when(repository.findById(1L)).thenReturn(Optional.of(task(Status.TODO)));
        assertThat(service.get(1).title()).isEqualTo("Sample task");
    }

    @Test void missingTaskFailsForEveryOperation() {
        assertThatThrownBy(() -> service.get(1)).isInstanceOf(TaskNotFoundException.class);
        assertThatThrownBy(() -> service.update(1, request("New", Status.TODO))).isInstanceOf(TaskNotFoundException.class);
        assertThatThrownBy(() -> service.delete(1)).isInstanceOf(TaskNotFoundException.class);
    }

    @Test void updatesAndPreservesOmittedEnums() {
        Task task = task(Status.DONE);
        when(repository.findById(1L)).thenReturn(Optional.of(task));
        when(repository.saveAndFlush(task)).thenReturn(task);
        var result = service.update(1, new TaskRequest(" Updated ", null, null, null, null));
        assertThat(result.title()).isEqualTo("Updated");
        assertThat(result.status()).isEqualTo(Status.DONE);
        assertThat(result.priority()).isEqualTo(Priority.MEDIUM);
        assertThat(result.description()).isNull();
    }

    @Test void preventsReopeningDoneAsTodo() {
        when(repository.findById(1L)).thenReturn(Optional.of(task(Status.DONE)));
        assertThatThrownBy(() -> service.update(1, request("New", Status.TODO)))
                .isInstanceOf(TaskConflictException.class);
    }

    @Test void preventsDuplicateUpdate() {
        when(repository.findById(1L)).thenReturn(Optional.of(task(Status.TODO)));
        when(repository.existsByTitleAndIdNot("New", 1L)).thenReturn(true);
        assertThatThrownBy(() -> service.update(1, request("New", Status.DONE)))
                .isInstanceOf(TaskConflictException.class);
    }

    @ParameterizedTest @EnumSource(Status.class)
    void deleteRespectsStatus(Status status) {
        Task task = task(status);
        when(repository.findById(1L)).thenReturn(Optional.of(task));
        if (status == Status.IN_PROGRESS) {
            assertThatThrownBy(() -> service.delete(1)).isInstanceOf(TaskConflictException.class);
            verify(repository, never()).delete(any());
        } else {
            service.delete(1);
            verify(repository).delete(task);
        }
    }
}
