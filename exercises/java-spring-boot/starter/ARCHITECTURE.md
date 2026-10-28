# Task API architecture and usage

This application is a single Java 17 / Spring Boot 3.2 REST service. Clients send
JSON over HTTP, the service applies task rules, and Spring Data JPA stores tasks
in an in-memory H2 database. Swagger UI provides an interactive API client.
There is no separate frontend or authentication layer. This is a local training
application. Dependency versions are defined in [pom.xml](pom.xml); the stack uses
Spring Data JPA, Hibernate, Jakarta Bean Validation, and SpringDoc OpenAPI.
For quick-start commands and examples, see [README.md](README.md).

## API workflow

Swagger UI and HTTP clients follow the same request flow:

```mermaid
flowchart TD
    Start[Start the server with the Maven wrapper] --> Explore[Open Swagger UI or use curl]
    Explore --> List[GET /api/v1/tasks]
    List --> Create[POST a task with a unique title]
    Create --> Inspect[GET the task using its returned id]
    Inspect --> Update[PUT the title and desired fields]
    Update --> Search[GET /api/v1/tasks/search?q=demo]
    Search --> Delete[DELETE the task when it is not IN_PROGRESS]
```

The API is available only at `/api/v1/tasks`; there is no unversioned alias.
Requests and responses use JSON, with ISO 8601 dates and timestamps.

PUT always requires `title`. Omitted or null `status` and `priority` retain their
current values. Omitted or null `description` and `dueDate` clear those fields.

| Operation | Method and canonical path | Success |
|---|---|---|
| List | `GET /api/v1/tasks?page=0&size=20` | 200, `TaskPage` |
| Search | `GET /api/v1/tasks/search?q=demo` | 200, `TaskPage` |
| Read | `GET /api/v1/tasks/{id}` | 200, `TaskResponse` |
| Create | `POST /api/v1/tasks` | 201, `TaskResponse` and Location |
| Update | `PUT /api/v1/tasks/{id}` | 200, `TaskResponse` |
| Delete | `DELETE /api/v1/tasks/{id}` | 204, no body |

Creation returns the `/api/v1/tasks/{id}` Location. Lists and searches are sorted
by ID, use zero-based pages, and accept page sizes 1–100 (default 20). A `TaskPage` contains `content`,
`page`, `size`, `totalElements`, and `totalPages`. Search trims `q` and matches a
case-insensitive literal substring in either title or description. `q` must be
nonblank and at most 500 characters before trimming.

## Components and boundaries

```mermaid
flowchart LR
    Client[Swagger UI or HTTP client] -->|HTTP and JSON| Controller[TaskController]
    subgraph Application[Spring Boot application]
        Controller -->|TaskRequest and parameters| Service[TaskService]
        Service -->|Entity queries and writes| Repository[TaskRepository]
        Repository --> JPA[Spring Data JPA and Hibernate]
        Service -->|TaskResponse| Controller
        Controller -->|Page envelope| Page[TaskPage]
        Handler[GlobalExceptionHandler]
        Controller -.->|Request errors| Handler
        Service -.->|Business or persistence errors| Handler
    end
    JPA --> Database[(H2 taskdb)]
    Controller -->|Success response| Client
    Handler -->|Problem Details JSON| Client
```

| Source location under `src/main/` | Responsibility |
|---|---|
| `java/com/example/taskapi/TaskApiApplication.java` | Application entry point |
| `java/com/example/taskapi/controller/TaskController.java` | Routes, input validation, pagination, HTTP statuses and Location |
| `java/com/example/taskapi/dto/` | Request, response, and page records defining the API payloads |
| `java/com/example/taskapi/service/TaskService.java` | Business rules, transaction boundaries, entity-to-response mapping |
| `java/com/example/taskapi/repository/TaskRepository.java` | JPA CRUD, title uniqueness lookups, and paginated search |
| `java/com/example/taskapi/entity/` | Persisted task model and status/priority enums |
| `java/com/example/taskapi/exception/` | Business exceptions and centralized HTTP error translation |
| `resources/application.properties` | H2, schema generation, JSON, and OpenAPI configuration |
| `resources/data.sql` | Three example tasks inserted at startup |

Controllers return DTOs rather than JPA entities. The service is read-only
transactional by default, with writable transactions for create, update, and
delete. JPA sessions are not kept open while rendering HTTP responses
(`spring.jpa.open-in-view=false`).

## Creating a task

```mermaid
sequenceDiagram
    actor Client
    participant Controller as TaskController
    participant Service as TaskService
    participant Repository as TaskRepository
    participant DB as H2 via Hibernate
    Client->>Controller: POST /api/v1/tasks with TaskRequest JSON
    Note over Controller,Service: Bean Validation checks request constraints
    Controller->>Service: create(request)
    Service->>Service: Check future due date in UTC
    Service->>Repository: existsByTitle(trimmed title)
    Repository->>DB: Look up title
    DB-->>Repository: Existence result
    Repository-->>Service: false
    Service->>Service: Build Task with defaults and supplied fields
    Service->>Repository: saveAndFlush(task)
    Note over Repository,DB: PrePersist sets timestamps and DB enforces unique title
    Repository->>DB: INSERT task
    DB-->>Repository: Generated id and persisted task
    Repository-->>Service: Task
    Service-->>Controller: TaskResponse
    Controller-->>Client: 201 Created with Location and JSON
```

This diagram shows the successful path. Validation failures return **400**,
missing tasks return **404**, and business conflicts return **409**. Errors use
Problem Details JSON. Request-body validation currently
returns a generic detail without field-level errors; see
[known limitations](#known-limitations-and-review-follow-ups). Recognized database
title-uniqueness failures also become 409, covering duplicate inserts that race past the service check.
Unexpected errors are logged and return a generic **500** response.

## Task data and lifecycle

A `Task` has a generated `Long` ID, a required unique title (maximum 100
characters), optional description (maximum 500), status, priority, optional
`LocalDate` due date, and `Instant` creation/update timestamps. Titles are trimmed
before storage and uniqueness is case-sensitive. Priority is `LOW`, `MEDIUM`,
or `HIGH`, defaulting to `MEDIUM` on creation. Bean Validation measures the raw
title length before trimming; a database unique constraint also enforces title
uniqueness. JPA callbacks set timestamps on insertion and update `updatedAt`
when persisted fields change. An identical update does not advance the timestamp.

```mermaid
stateDiagram-v2
    state "TODO" as Todo
    state "IN_PROGRESS" as InProgress
    state "DONE" as Done
    Todo --> InProgress: PUT status
    Todo --> Done: PUT status
    InProgress --> Todo: PUT status
    InProgress --> Done: PUT status
    Done --> InProgress: PUT status
    Todo --> [*]: DELETE
    Done --> [*]: DELETE
    note right of Done
        Direct DONE to TODO returns 409
    end note
    note right of InProgress
        DELETE returns 409
    end note
```

The diagram shows status changes and deletion. Creation defaults to `TODO` but
also accepts an explicit valid status. Updates may retain the existing status.
The implementation blocks only the direct `DONE` to `TODO` transition, so a
`DONE` task can move through `IN_PROGRESS` to `TODO`.

On creation, a supplied due date must be after today in UTC. Updates can retain
or set past due dates. IDs must be positive. Search queries must be nonblank and
at most 500 characters.

## Storage and verification

H2 runs inside the application process at `jdbc:h2:mem:taskdb`. Hibernate uses
`create-drop`, and `data.sql` runs after schema creation. **Tasks are lost when
the process stops**, and the three sample tasks are restored on the next start.
The H2 console is at `/h2-console` (user `sa`, empty password), with remote console
access disabled. Configuration lives in `src/main/resources/application.properties`;
there is no `application.yml` or `schema.sql`. This configuration is for local training.

Run the checks without starting a standalone server:

```bash
./mvnw clean verify
```

Tests under `src/test/java/com/example/taskapi/` use JUnit 5 and AssertJ, and cover
service rules with Mockito, HTTP behavior with `@SpringBootTest` and MockMvc,
repository behavior with `@DataJpaTest`, and exception translation. Shared fixtures
live in `TaskFixtures.java`; tests are organized into `unit/` and `integration/`.
JaCoCo enforces an 80% aggregate application line coverage gate, excluding the
launcher. This is not a per-class or unit-test-only coverage guarantee.
Its report is at `target/site/jacoco/index.html`.

## Known limitations and review follow-ups

- Boot's enabled Problem Details advice takes precedence over custom request-body
  validation handling, so the custom field-level `errors` array is missing from
  HTTP responses. A fix needs response-body assertions and must preserve framework
  404, 405, and 415 handling.
- Task has no optimistic version field. Overlapping updates/deletes can overwrite
  changes or bypass status guards; transactions alone do not prevent this.
- Extreme page/size combinations can exceed JPA's integer offset and return 500.
- Timestamp precision differences across JVM/platform and H2 storage were flagged
  by review but have not been verified on Linux.
- The API is unauthenticated and is not explicitly bound to loopback. H2 console
  remote access is disabled, but that does not restrict the REST API listener.
- Caching, rate limiting, authentication/authorization, and production deployment
  configuration are outside the current local exercise scope.
