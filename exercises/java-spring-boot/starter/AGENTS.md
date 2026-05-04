# Task Management API Starter

This directory is the Spring Boot starter project for the Codex CLI training
course. It should stay small, readable, and useful as a teaching codebase.

## Project Purpose

- Build a production-shaped REST API for task management.
- Demonstrate how Codex can inspect, modify, test, and explain a real Java
  service.
- Preserve clear architectural boundaries so students can reason about changes.

## Architecture

Package root: `com.example.taskapi`

- `controller`: HTTP endpoints and request/response status handling.
- `service`: business rules and transaction boundaries.
- `repository`: Spring Data JPA persistence.
- `entity`: JPA model and enums.
- `dto`: API request/response records and mapping.
- `exception`: domain exceptions and global error handling.
- `config`: OpenAPI and framework configuration.

The API uses DTOs at the boundary. Do not expose JPA entities directly from
controllers.

## Domain Model

`Task` is the central entity.

- `id`: generated `Long`
- `title`: required, unique, max 100 chars
- `description`: optional, max 500 chars
- `status`: `TODO`, `IN_PROGRESS`, `DONE`
- `priority`: `LOW`, `MEDIUM`, `HIGH`
- `dueDate`: optional, must be future when supplied
- `createdAt`: managed on persist
- `updatedAt`: managed on persist/update

Business rules:

- New tasks default to `TODO` status and `MEDIUM` priority.
- Task titles must be unique, case-insensitively.
- Do not delete tasks in `IN_PROGRESS`.
- Do not move a `DONE` task back to `TODO`.
- Update `updatedAt` on modification.

## Dependencies And Tools

- Java source target: 17
- Build: Maven
- Framework: Spring Boot 3.2.0
- Web: `spring-boot-starter-web`
- Persistence: Spring Data JPA with Hibernate
- Database: H2 in-memory database
- Validation: Jakarta Bean Validation via `spring-boot-starter-validation`
- OpenAPI: `springdoc-openapi-starter-webmvc-ui` 2.3.0
- Testing: JUnit 5, Spring Boot test support, MockMvc, AssertJ, Mockito
- Coverage: JaCoCo 0.8.13 with an 80% line coverage check during `verify`

## Runtime Configuration

The active Spring configuration is in `src/main/resources/application.yml`.
There is also an `application.properties`; keep both files aligned if changing
configuration, or prefer consolidating to one format in a deliberate cleanup.

Hibernate is configured with:

```yaml
spring.jpa.hibernate.ddl-auto: create-drop
spring.jpa.defer-datasource-initialization: true
spring.sql.init.mode: always
```

That means Hibernate creates the H2 schema from the JPA entities, then
`data.sql` loads sample data.

## Commands

From this `starter` directory:

```bash
mvn test
mvn verify
mvn spring-boot:run
```

Use `mvn verify` when changing production code because it runs the JaCoCo
coverage check. `mvn test` is fine for a quick behavioral check.

Do not assume `./mvnw` exists in this directory. If a wrapper is added later,
prefer it, but this starter currently works with the installed `mvn`.

## Testing Expectations

- Add or update unit tests for service-layer business rules.
- Add or update controller/integration tests for endpoint behavior.
- Use focused E2E tests for full HTTP lifecycle coverage.
- Keep test data readable; prefer fixture helpers over duplicated setup.
- Preserve the 80% line coverage gate.

Current test groups:

- `unit/TaskServiceTest.java`
- `integration/TaskControllerIntegrationTest.java`
- `e2e/TaskApiE2ETest.java`
- `fixture/TaskTestData.java`

## IDE Inspection Notes

Some IDE inspection warnings are expected and are not automatically defects:

- JPA table/column warnings for `tasks` can appear because the schema is
  generated at runtime by Hibernate for H2. Runtime tests confirm table
  creation.
- `ResponseEntity.getBody()` nullability warnings in E2E tests are static
  analysis concerns. The tests assert successful status codes first. It is OK
  to make these assertions more explicit, but the warnings are not currently
  runtime failures.
- `TaskPriority` may appear unused to narrow inspections, but it is used by DTOs
  and tests and is part of the JSON API contract.
- Markdown, proofreading, SQL weak warnings, and similar IDE hints are cleanup
  candidates, not blockers.

## Coding Standards

- Keep controllers thin; put business decisions in services.
- Prefer constructor injection.
- Validate request DTOs with Jakarta validation annotations.
- Return meaningful domain errors through `GlobalExceptionHandler`.
- Keep exception messages useful for API clients and tests.
- Keep changes scoped to the requested behavior.
- Avoid unrelated refactors in starter code unless they clarify the lesson.

## Training Repo Context

This project is part of the broader O'Reilly Codex training materials. Exercise
starter code may intentionally include rough edges so students can practice
diagnosis and repair with Codex. Before removing a vulnerability, warning, or
teaching artifact, confirm it is not intentional course material.
