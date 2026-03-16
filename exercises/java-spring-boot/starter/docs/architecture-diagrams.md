# Task API Architecture Diagrams

This document summarizes the current Spring Boot task management API using Mermaid diagrams.

## System Overview

```mermaid
flowchart LR
    Client["Client Applications<br/>Browser, Postman, CLI"] -->|"HTTP JSON"| Controller["TaskController<br/>/api/v1/tasks"]
    Controller -->|"DTO validation"| Service["TaskService"]
    Service -->|"JPA operations"| Repository["TaskRepository"]
    Repository -->|"CRUD + search"| DB[("H2 In-Memory Database")]

    Controller --> Advice["GlobalExceptionHandler"]
    Service --> Entity["Task Entity<br/>Status + Priority"]
    Controller --> DTO["Request/Response DTOs"]

    OpenAPI["OpenAPI / Swagger UI"] -. "documents" .-> Controller
    Seeder["SampleDataInitializer"] --> Repository
```

## Package Structure

```mermaid
flowchart TD
    App["TaskApiApplication"]

    subgraph Config["Config"]
        OpenApiConfig["OpenApiConfig"]
        SampleDataInitializer["SampleDataInitializer"]
    end

    subgraph API["API"]
        TaskController["controller.TaskController"]
        TaskCreateRequest["dto.TaskCreateRequest"]
        TaskUpdateRequest["dto.TaskUpdateRequest"]
        TaskResponse["dto.TaskResponse"]
        ErrorResponse["dto.ErrorResponse"]
    end

    subgraph Business["Business"]
        TaskService["service.TaskService"]
        BusinessRuleViolationException["exception.BusinessRuleViolationException"]
        TaskNotFoundException["exception.TaskNotFoundException"]
        GlobalExceptionHandler["exception.GlobalExceptionHandler"]
    end

    subgraph Persistence["Persistence"]
        TaskRepository["repository.TaskRepository"]
        Task["entity.Task"]
        Status["entity.Status"]
        Priority["entity.Priority"]
    end

    App --> TaskController
    App --> TaskService
    App --> TaskRepository
    App --> OpenApiConfig
    App --> SampleDataInitializer

    TaskController --> TaskCreateRequest
    TaskController --> TaskUpdateRequest
    TaskController --> TaskResponse
    TaskController --> TaskService
    TaskController --> GlobalExceptionHandler

    TaskService --> TaskRepository
    TaskService --> Task
    TaskService --> BusinessRuleViolationException
    TaskService --> TaskNotFoundException

    TaskRepository --> Task
    Task --> Status
    Task --> Priority

    GlobalExceptionHandler --> ErrorResponse
```

## Request Flow

```mermaid
sequenceDiagram
    actor Client
    participant Controller as TaskController
    participant Service as TaskService
    participant Repo as TaskRepository
    participant DB as H2 Database
    participant Advice as GlobalExceptionHandler

    Client->>Controller: POST /api/v1/tasks
    Controller->>Controller: Validate request DTO
    Controller->>Service: createTask(request)
    Service->>Service: Enforce business rules
    Service->>Repo: save(task)
    Repo->>DB: INSERT task
    DB-->>Repo: persisted task
    Repo-->>Service: Task
    Service-->>Controller: TaskResponse
    Controller-->>Client: 201 Created + JSON

    alt Validation or business rule failure
        Controller->>Advice: Handle exception
        Advice-->>Client: ErrorResponse with 400 404 or 409
    end
```

## Domain Model

```mermaid
classDiagram
    class Task {
        +Long id
        +String title
        +String description
        +Status status
        +Priority priority
        +LocalDate dueDate
        +Instant createdAt
        +Instant updatedAt
        +onCreate()
        +onUpdate()
    }

    class Status {
        <<enumeration>>
        TODO
        IN_PROGRESS
        DONE
    }

    class Priority {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
    }

    Task --> Status
    Task --> Priority
```

## Search And CRUD Endpoints

```mermaid
flowchart TB
    Client["Client"] --> List["GET /api/v1/tasks"]
    Client --> Get["GET /api/v1/tasks/:id"]
    Client --> Create["POST /api/v1/tasks"]
    Client --> Update["PUT /api/v1/tasks/:id"]
    Client --> Delete["DELETE /api/v1/tasks/:id"]
    Client --> Search["GET /api/v1/tasks/search?q=..."]

    List --> TaskController
    Get --> TaskController
    Create --> TaskController
    Update --> TaskController
    Delete --> TaskController
    Search --> TaskController
```
