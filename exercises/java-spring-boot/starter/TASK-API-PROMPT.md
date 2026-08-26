# Task Management API Student Prompt

```text
Build a complete Spring Boot task-management REST API in the existing project.

First inspect the project, its pom.xml, existing source files, and any AGENTS.md instructions. Preserve the existing Java, Spring Boot, and Maven versions unless a change is necessary.

Requirements

Domain model:
- Task entity with:
  - id: Long, generated
  - title: required, maximum 100 characters
  - description: optional, maximum 500 characters
  - status: TODO, IN_PROGRESS, or DONE
  - priority: LOW, MEDIUM, or HIGH
  - dueDate: optional LocalDate
  - createdAt and updatedAt: automatically maintained Instant values
- New tasks default to TODO status and MEDIUM priority.
- Task titles must be unique, ignoring case and surrounding whitespace.
- A new task's due date must be in the future.
- An IN_PROGRESS task cannot be deleted.
- A DONE task cannot be changed directly back to TODO.

API:
- Use `/api/v1/tasks` as the base path.
- Implement:
  - GET `/api/v1/tasks` — paginated task listing
  - GET `/api/v1/tasks/{id}` — retrieve one task
  - POST `/api/v1/tasks` — create a task
  - PUT `/api/v1/tasks/{id}` — replace a task
  - DELETE `/api/v1/tasks/{id}` — delete a task
  - GET `/api/v1/tasks/search?query=...` — search title and description
- Pagination should default to 20 records and allow no more than 100.
- Return HTTP 201 with a Location header after creation.
- Return HTTP 204 after successful deletion.
- Never expose JPA entities directly. Use request and response DTOs.
- Use Bean Validation for request validation.
- Keep controllers focused on HTTP concerns and business rules in the service layer.

Persistence:
- Use Spring Data JPA and an H2 in-memory database.
- Initialize the development database from `src/main/resources/data.sql` with at least three representative tasks.
- Ensure data initialization occurs after Hibernate creates the schema.

Error handling:
- Add global exception handling.
- Return correct 400, 404, 409, and 500 status codes.
- Return a consistent JSON error structure containing:
  - timestamp
  - status
  - error
  - message
  - request path
  - field validation errors when applicable
- Do not expose internal exception details in 500 responses.

Documentation:
- Add SpringDoc OpenAPI documentation.
- Make Swagger UI available at `/swagger-ui.html`.
- Document the endpoints, important responses, and business rules.
- Update the README with build, test, run, Swagger, and H2-console instructions.

Testing:
- Add focused unit tests for every service method and business rule.
- Add MockMvc integration tests for every endpoint.
- Include tests for validation failures, missing tasks, duplicate titles, malformed enum values, pagination, searching, timestamps, and forbidden status transitions.
- Use reusable test fixtures where helpful.
- Configure JaCoCo to enforce at least 80% line coverage and 80% branch coverage during `mvn verify`.

Implementation guidance:
- Use constructor injection.
- Use transactions appropriately, with read-only transactions for queries.
- Avoid unnecessary frameworks, caching, authentication, rate limiting, microservices, or other features outside these requirements.
- Do not merely describe the implementation: create all required files and code.
- Run `mvn verify` when finished.
- Continue fixing compilation, test, and coverage failures until the build passes.
- Finish by summarizing the implementation, verification results, and any assumptions.

Optional quality improvements:
- These are stretch goals, not part of the required implementation. Do not implement them unless explicitly requested after the core application passes `mvn verify`.
- Add optimistic locking with a version field.
- Consolidate application configuration into one authoritative format.
- Preserve framework-generated 404 responses for unknown routes.
- Log unexpected exceptions before returning a generic 500 response.
- Enforce case-insensitive title uniqueness at the database level so concurrent requests cannot bypass it.
```
