package com.example.taskapi.entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Locale;

@Entity
@Table(name = "tasks", uniqueConstraints = @UniqueConstraint(name = "uk_tasks_title_key", columnNames = "title_key"))
public class Task {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, length = 100)
    private String title;
    @Column(name = "title_key", nullable = false, length = 300)
    private String titleKey;
    @Column(length = 500)
    private String description;
    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 20)
    private TaskStatus status;
    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 10)
    private TaskPriority priority;
    private LocalDate dueDate;
    @Column(nullable = false, updatable = false)
    private Instant createdAt;
    @Column(nullable = false)
    private Instant updatedAt;
    @Version
    private Long version;

    protected Task() { }

    public Task(String title, String description, TaskStatus status, TaskPriority priority,
                LocalDate dueDate, Instant now) {
        setTitle(title);
        this.description = description;
        this.status = status;
        this.priority = priority;
        this.dueDate = dueDate;
        this.createdAt = now.truncatedTo(ChronoUnit.MICROS);
        this.updatedAt = this.createdAt;
    }

    public static String normalizeTitle(String title) {
        return title.strip().toLowerCase(Locale.ROOT);
    }

    private void setTitle(String title) {
        this.title = title.strip();
        this.titleKey = normalizeTitle(title);
    }

    public void update(String title, String description, TaskStatus status, TaskPriority priority,
                       LocalDate dueDate, Instant now) {
        setTitle(title);
        this.description = description;
        this.status = status;
        this.priority = priority;
        this.dueDate = dueDate;
        // Match database microsecond precision; even same-tick edits advance the timestamp.
        Instant candidate = now.truncatedTo(ChronoUnit.MICROS);
        this.updatedAt = candidate.isAfter(updatedAt) ? candidate : updatedAt.plus(1, ChronoUnit.MICROS);
    }

    public Long getId() { return id; }
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public TaskStatus getStatus() { return status; }
    public TaskPriority getPriority() { return priority; }
    public LocalDate getDueDate() { return dueDate; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
}
