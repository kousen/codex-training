# Task Management API

A Spring Boot 3.2 REST API for creating, searching, updating, and deleting tasks.
It uses Java 17, Spring Data JPA, Bean Validation, H2, and SpringDoc OpenAPI.

## API

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/v1/tasks` | List tasks with pagination |
| `GET` | `/api/v1/tasks/{id}` | Get one task |
| `POST` | `/api/v1/tasks` | Create a task |
| `PUT` | `/api/v1/tasks/{id}` | Replace a task |
| `DELETE` | `/api/v1/tasks/{id}` | Delete a task |
| `GET` | `/api/v1/tasks/search?query=text` | Search titles and descriptions |

List and search endpoints accept Spring pagination parameters such as
`page`, `size`, and `sort`. Page size defaults to 20 and is capped at 100.

New tasks default to `TODO` status and `MEDIUM` priority. Titles are unique,
new due dates must be in the future, `IN_PROGRESS` tasks cannot be deleted, and
`DONE` tasks cannot return directly to `TODO`.

## Quick Start

```bash
# Run the tests and enforce 80% line and branch coverage
mvn verify

# Run the application
mvn spring-boot:run

# Access H2 console
open http://localhost:8080/h2-console

# Access Swagger UI
open http://localhost:8080/swagger-ui.html
```

The OpenAPI JSON is available at `http://localhost:8080/api-docs`. The database
is initialized with three sample tasks each time the application starts. The
coverage report is generated at `target/site/jacoco/index.html`.
