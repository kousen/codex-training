# Task Management API

Java 17 / Spring Boot 3.2 application with JPA, H2, Bean Validation and Swagger.

See [Architecture and usage](ARCHITECTURE.md) for Mermaid diagrams of the request
flow, components, and task lifecycle.

```bash
./mvnw spring-boot:run
./mvnw clean verify
```

The Maven wrapper downloads Maven automatically on first use. On Windows, use
`mvnw.cmd` instead of `./mvnw`.

Use Java 17 for the build. On macOS, if a newer JDK is your default:

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 17) ./mvnw clean verify
```

`verify` runs service unit tests, full-context MockMvc controller tests, repository
integration tests, and an 80% line coverage gate. The report is at
`target/site/jacoco/index.html` (the application launcher is excluded).

| Method | Path | Result |
|---|---|---|
| GET | `/api/v1/tasks?page=0&size=20` | Page of tasks, sorted by ID |
| GET | `/api/v1/tasks/{id}` | Single task |
| POST | `/api/v1/tasks` | Create; 201 with Location header |
| PUT | `/api/v1/tasks/{id}` | Update task |
| DELETE | `/api/v1/tasks/{id}` | Delete; 204 |
| GET | `/api/v1/tasks/search?q=spring` | Search title or description, with pagination |

Pages are zero-based; page size must be 1–100 (default 20). Responses contain
`content`, `page`, `size`, `totalElements`, and `totalPages`. Search is a
case-insensitive literal substring match; `q` must be nonblank and at most 500 characters.

```bash
curl http://localhost:8080/api/v1/tasks
curl -i http://localhost:8080/api/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Try the API","description":"Create a task","priority":"HIGH"}'
curl 'http://localhost:8080/api/v1/tasks/search?q=API&size=5'
```

Titles are required, trimmed, case-sensitive unique, and at most 100 characters.
Descriptions are optional, at most 500 characters. Status defaults to `TODO`,
priority to `MEDIUM`. Due dates are optional ISO dates and must be after today
in UTC on creation. Updates may retain past due dates. PUT requires a title;
omitted/null status and priority retain their values, while omitted/null
description and dueDate clear them. DONE tasks cannot transition directly to
TODO; IN_PROGRESS tasks cannot be deleted. Timestamps are managed by JPA;
`updatedAt` changes when persisted fields change.

Errors use Problem Details JSON with HTTP 400 for invalid input, 404 for missing
tasks, 409 for business conflicts, and 500 with a generic message for unexpected
failures. Validation errors include an `errors` array.

- Swagger UI: http://localhost:8080/swagger-ui.html
- OpenAPI JSON: http://localhost:8080/api-docs
- H2 console: http://localhost:8080/h2-console
  (JDBC URL `jdbc:h2:mem:taskdb`, user `sa`, empty password)

Three sample tasks are loaded from `data.sql` at startup. H2 data is in memory
and resets on restart. This is a local training application: authentication,
rate limiting, and production deployment configuration are outside this exercise.
