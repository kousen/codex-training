# Task Management API

## Purpose

This exercise builds a Spring Boot task-management REST API for the Codex CLI
training course. Keep the implementation approachable for students while using
professional Java and Spring practices.

The complete student assignment is in `starter/TASK-API-PROMPT.md`. This file
defines durable project conventions rather than repeating the assignment.

## Technology

- Java 17
- Spring Boot 3.2
- Maven
- Spring Web
- Spring Data JPA
- Jakarta Bean Validation
- H2 for local development
- SpringDoc OpenAPI
- JUnit 5, Mockito, AssertJ, and MockMvc
- JaCoCo coverage enforcement

Do not upgrade Java, framework, dependency, or plugin versions unless explicitly
requested.

## Working Directory and Commands

Run application commands from `starter/`.

```bash
cd starter

# Compile, test, package, and enforce coverage
mvn verify

# Run the application
mvn spring-boot:run
```

A change is not complete until `mvn verify` passes.

## Architecture

Preserve the existing request flow:

```text
controller -> service -> repository -> database
                 |
                 -> DTO/entity mapping
```

- Controllers handle HTTP concerns only.
- Services own transactions and business rules.
- Repositories contain persistence operations.
- JPA entities are internal and must not be returned directly from controllers.
- Request and response DTOs define the API contract.
- Use constructor injection.
- Use read-only transactions for queries.
- Prefer straightforward code over unnecessary abstractions or frameworks.

The current package-by-layer structure is appropriate for one aggregate. If the
application grows to include users, projects, or other aggregates, prefer
packaging by feature rather than adding more global technical-layer packages.

## API Conventions

- Base path: `/api/v1`
- JSON request and response bodies
- ISO-8601 dates and timestamps
- Pagination defaults to 20 and must not exceed 100
- `POST` returns `201 Created` with a `Location` header
- `DELETE` returns `204 No Content`
- Validation failures return `400 Bad Request`
- Missing resources return `404 Not Found`
- Business-rule and uniqueness conflicts return `409 Conflict`
- Unexpected errors return `500 Internal Server Error` without internal details

Preserve normal framework 400 and 404 responses. Log unexpected exceptions
before returning a generic error response. Update OpenAPI documentation and
integration tests whenever the API contract changes.

## Domain Invariants

- Task titles are required and no longer than 100 characters.
- Descriptions are optional and no longer than 500 characters.
- New tasks default to `TODO` status.
- New tasks default to `MEDIUM` priority.
- A new task's due date must be in the future.
- `IN_PROGRESS` tasks cannot be deleted.
- `DONE` tasks cannot transition directly to `TODO`.
- Updated timestamps change whenever a task is modified.
- Normalize titles before checking uniqueness.
- Keep database constraints consistent with service-level rules.

If users or projects are introduced, reconsider globally unique task titles
before extending the schema. Use optimistic locking when concurrent updates
become part of the requirements.

## Persistence and Configuration

- H2 and `data.sql` are development conveniences.
- Seed data must remain deterministic and development-only.
- SQL initialization must occur after Hibernate creates the development schema.
- Keep one authoritative application configuration format. Do not duplicate
  settings across properties and YAML files.
- Keep the H2 console, SQL logging, and verbose error details out of production
  profiles.
- For production persistence, use database migrations and test against the same
  database engine used in production.

## Testing

- Unit-test service methods and every business-rule branch.
- Use MockMvc integration tests for endpoint behavior.
- Test successful requests and meaningful failures.
- Use reusable test fixtures where helpful.
- Prefer isolated test setup over dependence on hard-coded seed IDs.
- Maintain at least 80% line coverage and 80% branch coverage.
- Do not weaken or remove coverage gates to make a build pass.

## Definition of Done

Before finishing a change:

1. Run `mvn verify` from `starter/`.
2. Confirm all tests and coverage checks pass.
3. Run `git diff --check`.
4. Update the README and OpenAPI documentation if behavior changed.
5. Summarize the implementation, verification, assumptions, and remaining risks.

## Scope Control

Do not add the following without an explicit request:

- Authentication or authorization
- Caching
- Rate limiting
- Messaging or event-driven infrastructure
- Microservices
- External production databases
- Deployment infrastructure
- Large dependency upgrades

Do not modify intentional training vulnerabilities unless an exercise explicitly
asks for it.
