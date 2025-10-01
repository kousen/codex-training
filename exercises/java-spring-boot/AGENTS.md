# Task Management API Project

## Overview
Building a production-ready REST API for task management using Spring Boot.

## Technology Stack
- **Framework**: Spring Boot 3.5.3
- **Language**: Java 17
- **Build Tool**: Maven
- **Database**: H2 (in-memory for development)
- **ORM**: Spring Data JPA
- **Validation**: Jakarta Bean Validation
- **Documentation**: SpringDoc OpenAPI 2.7.0
- **Testing**: JUnit 5, Mockito, AssertJ, REST Assured

## Project Structure
```
src/
├── main/
│   ├── java/com/example/taskapi/
│   │   ├── controller/      # REST controllers
│   │   ├── service/         # Business logic
│   │   ├── repository/      # Data access layer
│   │   ├── entity/          # JPA entities
│   │   ├── dto/             # Data transfer objects
│   │   ├── exception/       # Custom exceptions
│   │   ├── config/          # Configuration classes
│   │   └── util/            # Utility classes
│   └── resources/
│       ├── application.yml   # Application configuration
│       ├── data.sql         # Initial data
│       └── schema.sql       # Database schema
└── test/
    └── java/com/example/taskapi/
        ├── integration/      # Integration tests
        └── unit/            # Unit tests
```

## API Conventions
- Base URL: `/api/v1`
- JSON request/response format
- ISO 8601 date formats
- HTTP status codes:
  - 200 OK - Successful GET
  - 201 Created - Successful POST
  - 204 No Content - Successful DELETE
  - 400 Bad Request - Validation errors
  - 404 Not Found - Resource not found
  - 409 Conflict - Business rule violation
  - 500 Internal Server Error - Unexpected errors

## Coding Standards
- Use DTOs (Java records) for API requests/responses
- Never expose entities directly
- Service layer handles all business logic
- Controllers only handle HTTP concerns
- Comprehensive input validation
- Meaningful exception messages
- Logging at appropriate levels
- Unit test coverage minimum 80%

## Entity Relationships
```
Task
├── id: Long (auto-generated)
├── title: String (required, max 100)
├── description: String (max 500)
├── status: Enum (TODO, IN_PROGRESS, DONE)
├── priority: Enum (LOW, MEDIUM, HIGH)
├── dueDate: LocalDate (optional)
├── createdAt: Instant (auto-managed)
└── updatedAt: Instant (auto-managed)
```

## Business Rules
1. Task title is mandatory and unique
2. Default status is TODO when creating
3. Default priority is MEDIUM when creating
4. Cannot delete task with status IN_PROGRESS
5. Cannot change DONE task back to TODO
6. Due date must be in the future when creating
7. Updated timestamp changes on any modification

## Testing Strategy
- Unit tests for all service methods
- Integration tests for all endpoints
- Test data builders for readable tests
- Parameterized tests for edge cases
- MockMvc for controller tests
- @DataJpaTest for repository tests
- @SpringBootTest for full integration tests

## Security Considerations
- Input validation on all endpoints
- SQL injection prevention via parameterized queries
- XSS prevention via output encoding
- Rate limiting on API endpoints (future)
- Authentication/authorization (future)

## Performance Guidelines
- Pagination for list endpoints (default 20, max 100)
- Lazy loading for relationships
- Database indexes on frequently queried fields
- Response caching where appropriate
- Async processing for long operations

## Current Development Focus
Implementing core CRUD operations with proper validation, error handling, and comprehensive test coverage. Following TDD approach where possible.