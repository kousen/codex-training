# AGENTS.md

## Project Purpose
Production-style Spring Boot REST API for task management.

## Stack
- Spring Boot 3.2.x
- Java 17
- Maven
- Spring Web
- Spring Data JPA
- H2 for local development
- Bean Validation
- SpringDoc OpenAPI

## Architecture
Use layered architecture only:
- `controller`: HTTP concerns only
- `service`: business rules and orchestration
- `repository`: persistence
- `entity`: JPA entities only
- `dto`: request/response models
- `exception`: custom exceptions and global handlers
- `config`: Spring configuration

Never expose JPA entities directly from controllers.

## API Conventions
- Base path: `/api/v1`
- Resource path: `/api/v1/tasks`
- JSON only
- ISO-8601 dates and timestamps
- Use DTOs for all input and output
- Paginated list endpoints must accept `page`, `size`, and `sort`
- Allowed sort fields: `id`, `title`, `status`, `priority`, `dueDate`, `createdAt`, `updatedAt`

## Domain Rules
- Task title is required and unique
- Default status on create: `TODO`
- Default priority on create: `MEDIUM`
- Due date must be in the future when creating or updating
- `IN_PROGRESS` tasks cannot be deleted
- `DONE` tasks cannot move back to `TODO`
- `updatedAt` must change on every modification

## Implementation Rules
- Put business rules in services, not controllers
- Validate inputs with Bean Validation first, then service-level business rules
- Return meaningful 4xx errors for client mistakes
- Do not return generic 500 for validation or bad request scenarios
- Normalize user input where appropriate, such as trimming titles
- Keep OpenAPI docs accurate when adding query params or request bodies

## Persistence Rules
- Use Spring Data JPA repositories
- Prefer derived queries or parameterized JPQL
- Do not build SQL strings manually
- Keep entity mappings simple and explicit
- Preserve DB-level uniqueness for `title`

## Security Expectations
This project is not production-ready unless explicitly hardened.

For non-dev environments:
- disable H2 console
- disable verbose error messages
- disable SQL logging
- do not use `ddl-auto=create-drop`
- do not expose Swagger UI publicly unless intended
- add authentication and authorization before calling it secure
- add rate limiting before public exposure

## Testing Expectations
Minimum expected coverage:
- unit tests for service business rules
- integration tests for controller endpoints
- tests for error paths, not just happy paths
- tests for pagination and search behavior
- tests for invalid sort fields and validation failures

When changing behavior:
- update or add tests in the same change

## Useful Commands
- Run app: `mvn spring-boot:run`
- Run tests: `mvn test`
- Clean test run: `mvn clean test`

## Profiles
Prefer:
- `dev` for H2 console, Swagger UI, verbose logs
- `test` for automated tests
- `prod` for hardened defaults

Do not put dev-only settings in the default profile if avoidable.

## Documentation
Keep these current when behavior changes:
- OpenAPI annotations
- README
- architecture diagrams in `docs/`
- sample requests and responses if added

## Definition of Done
A change is not done unless:
- code compiles
- tests pass
- OpenAPI behavior matches implementation
- error handling is correct
- security posture is not weakened accidentally
