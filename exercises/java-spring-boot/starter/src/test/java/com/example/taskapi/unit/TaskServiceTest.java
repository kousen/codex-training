package com.example.taskapi.unit;

import com.example.taskapi.dto.*;
import com.example.taskapi.entity.*;
import com.example.taskapi.exception.*;
import com.example.taskapi.repository.TaskRepository;
import com.example.taskapi.service.TaskService;
import java.time.*;
import java.util.*;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.*;
import static com.example.taskapi.support.TaskFixtures.*;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {
    @Mock TaskRepository repository;
    TaskService service;

    @BeforeEach void setup() { service = new TaskService(repository, CLOCK); }

    @Test void createsWithDefaultsAndTrimmedTitle() {
        when(repository.saveAndFlush(any())).thenAnswer(invocation -> invocation.getArgument(0));
        TaskResponse result = service.create(create("  My Task  "));
        assertThat(result.title()).isEqualTo("My Task");
        assertThat(result.status()).isEqualTo(TaskStatus.TODO);
        assertThat(result.priority()).isEqualTo(TaskPriority.MEDIUM);
        assertThat(result.createdAt()).isEqualTo(NOW);
        assertThat(result.updatedAt()).isEqualTo(NOW);
        assertThat(result.dueDate()).isNull();
        verify(repository).existsByTitleKey("my task");
    }

    @ParameterizedTest @EnumSource(TaskStatus.class)
    void acceptsExplicitStatusAndPriority(TaskStatus status) {
        when(repository.saveAndFlush(any())).thenAnswer(invocation -> invocation.getArgument(0));
        var result = service.create(new CreateTaskRequest("Task", null, status, TaskPriority.LOW, LocalDate.of(2030, 6, 16)));
        assertThat(result.status()).isEqualTo(status);
        assertThat(result.priority()).isEqualTo(TaskPriority.LOW);
        assertThat(result.dueDate()).isEqualTo(LocalDate.of(2030, 6, 16));
    }

    @ParameterizedTest @ValueSource(strings = {"2030-06-14", "2030-06-15"})
    void rejectsNonFutureDueDate(String date) {
        assertThatThrownBy(() -> service.create(new CreateTaskRequest("Task", null, null, null, LocalDate.parse(date))))
            .isInstanceOf(InvalidTaskException.class).hasMessageContaining("future");
        verifyNoInteractions(repository);
    }

    @Test void rejectsDuplicateOnCreate() {
        when(repository.existsByTitleKey("task")).thenReturn(true);
        assertThatThrownBy(() -> service.create(create(" TASK "))).isInstanceOf(TaskConflictException.class);
        verify(repository, never()).saveAndFlush(any());
    }

    @Test void getsTaskAsDto() {
        when(repository.findById(1L)).thenReturn(Optional.of(task(1, "Task", TaskStatus.TODO)));
        assertThat(service.get(1).id()).isEqualTo(1L);
    }

    @Test void missingTasksFailForReadUpdateAndDelete() {
        assertThatThrownBy(() -> service.get(1)).isInstanceOf(TaskNotFoundException.class).hasMessage("Task 1 was not found");
        assertThatThrownBy(() -> service.update(1, update("Task", TaskStatus.TODO))).isInstanceOf(TaskNotFoundException.class);
        assertThatThrownBy(() -> service.delete(1)).isInstanceOf(TaskNotFoundException.class);
    }

    @Test void listPreservesPaginationMetadataAndStableSort() {
        Pageable pageable = PageRequest.of(1, 2, Sort.by("id").ascending());
        when(repository.findAll(pageable)).thenReturn(new PageImpl<>(List.of(task(3, "Third", TaskStatus.TODO)), pageable, 3));
        var result = service.list(1, 2);
        assertThat(result.page()).isEqualTo(1);
        assertThat(result.size()).isEqualTo(2);
        assertThat(result.totalElements()).isEqualTo(3);
        assertThat(result.totalPages()).isEqualTo(2);
        assertThat(result.content()).extracting(TaskResponse::title).containsExactly("Third");
    }

    @Test void searchTrimsQueryAndPaginates() {
        Pageable pageable = PageRequest.of(0, 20, Sort.by("id").ascending());
        when(repository.findByTitleContainingIgnoreCaseOrDescriptionContainingIgnoreCase("work", "work", pageable))
            .thenReturn(new PageImpl<>(List.of(task(1, "Workshop", TaskStatus.TODO)), pageable, 1));
        assertThat(service.search(" work ", 0, 20).content()).hasSize(1);
    }

    @Test void rejectsPageOffsetsThatJpaCannotRepresent() {
        assertThatThrownBy(() -> service.list(Integer.MAX_VALUE, 100))
            .isInstanceOf(InvalidTaskException.class).hasMessageContaining("offset");
        verifyNoInteractions(repository);
    }

    @ParameterizedTest
    @CsvSource({"TODO,TODO", "TODO,IN_PROGRESS", "TODO,DONE", "IN_PROGRESS,TODO", "IN_PROGRESS,IN_PROGRESS", "IN_PROGRESS,DONE", "DONE,IN_PROGRESS", "DONE,DONE"})
    void allowedTransitionsPreserveCreationAndAdvanceUpdate(TaskStatus before, TaskStatus after) {
        Task entity = task(1, "Old", before);
        Instant created = entity.getCreatedAt();
        when(repository.findById(1L)).thenReturn(Optional.of(entity));
        when(repository.saveAndFlush(entity)).thenReturn(entity);
        var result = service.update(1, update(" New ", after));
        assertThat(result.title()).isEqualTo("New");
        assertThat(result.status()).isEqualTo(after);
        assertThat(result.priority()).isEqualTo(TaskPriority.HIGH);
        assertThat(result.description()).isEqualTo("Updated description");
        assertThat(result.dueDate()).isNull();
        assertThat(result.createdAt()).isEqualTo(created);
        assertThat(result.updatedAt()).isEqualTo(NOW);
        verify(repository).existsByTitleKeyAndIdNot("new", 1L);
    }

    @Test void rejectsDoneToTodo() {
        when(repository.findById(1L)).thenReturn(Optional.of(task(1, "Task", TaskStatus.DONE)));
        assertThatThrownBy(() -> service.update(1, update("Task", TaskStatus.TODO)))
            .isInstanceOf(TaskConflictException.class).hasMessageContaining("DONE");
        verify(repository, never()).saveAndFlush(any());
    }

    @Test void rejectsDuplicateOnUpdate() {
        when(repository.findById(1L)).thenReturn(Optional.of(task(1, "Task", TaskStatus.TODO)));
        when(repository.existsByTitleKeyAndIdNot("other", 1L)).thenReturn(true);
        assertThatThrownBy(() -> service.update(1, update("Other", TaskStatus.TODO))).isInstanceOf(TaskConflictException.class);
        verify(repository, never()).saveAndFlush(any());
    }

    @Test void sameClockTickStillAdvancesTimestampAndAllowsExistingPastDueDates() {
        Task entity = new Task("Task", null, TaskStatus.TODO, TaskPriority.MEDIUM, null, NOW);
        when(repository.findById(1L)).thenReturn(Optional.of(entity));
        when(repository.saveAndFlush(entity)).thenReturn(entity);
        var result = service.update(1, new UpdateTaskRequest("Task", null, TaskStatus.TODO, TaskPriority.LOW, LocalDate.of(2020, 1, 1)));
        assertThat(result.updatedAt()).isAfter(NOW);
        assertThat(result.dueDate()).isEqualTo(LocalDate.of(2020, 1, 1));
    }

    @ParameterizedTest @EnumSource(value = TaskStatus.class, names = {"TODO", "DONE"})
    void deletesAllowedStatuses(TaskStatus status) {
        Task entity = task(1, "Task", status);
        when(repository.findById(1L)).thenReturn(Optional.of(entity));
        service.delete(1);
        verify(repository).delete(entity);
        verify(repository).flush();
    }

    @Test void rejectsDeletingInProgress() {
        when(repository.findById(1L)).thenReturn(Optional.of(task(1, "Task", TaskStatus.IN_PROGRESS)));
        assertThatThrownBy(() -> service.delete(1)).isInstanceOf(TaskConflictException.class);
        verify(repository, never()).delete(any());
    }
}
