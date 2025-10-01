# Lab 1: Spring Boot Task Management API

## Objective
Use Codex to build a complete REST API for task management with Spring Boot.

## Requirements

Build a Spring Boot application that includes:

1. **Domain Model**
   - Task entity with fields: id, title, description, status, priority, dueDate, createdAt, updatedAt (with auditing callbacks)
   - Status enum: TODO, IN_PROGRESS, DONE
   - Priority enum: LOW, MEDIUM, HIGH

2. **REST Endpoints**
   - GET /api/v1/tasks - List tasks with pagination (default size 20, max 100)
   - GET /api/v1/tasks/{id} - Retrieve a single task
   - POST /api/v1/tasks - Create a new task
   - PUT /api/v1/tasks/{id} - Update an existing task
   - DELETE /api/v1/tasks/{id} - Delete a task

3. **Data Layer**
   - H2 in-memory database (schema/data managed by `schema.sql` and `data.sql`)
   - Spring Data JPA repository with title uniqueness lookups
   - Database initialization script pre-populating sample tasks

4. **Business Logic**
   - Service layer with strict business rules
   - Task title must be unique (case-insensitive)
   - Default status TODO and priority MEDIUM on create
   - Future-dated due dates only
   - Cannot delete tasks in progress
   - Cannot transition DONE tasks back to TODO
   - Automatic timestamp management

5. **Validation & Error Handling**
   - Input validation using Bean Validation annotations on record DTOs
   - Global exception handler producing structured error payloads
   - Meaningful error responses covering validation, conflicts, and not-found cases

6. **Documentation**
   - OpenAPI/Swagger documentation served by SpringDoc (`/api-docs`, `/swagger-ui.html`)
   - API versioning via `/api/v1` base path

7. **Testing**
   - Unit tests for services with parameterized edge cases
   - Integration tests covering all endpoints and validation scenarios
   - Repository slice tests
   - Test data builders for readable fixtures

## Starting Point

The `starter/` directory contains a complete Spring Boot project you can inspect, extend, or rebuild using Codex.

## Codex Prompts Progression

### Step 1: Analyze Project Structure
```bash
codex "Analyze the current Spring Boot project structure and identify what needs to be added for a task management API"
```

### Step 2: Create Domain Model
```bash
codex "Create JPA entities for Task with proper annotations, validation, and auditing. Include Status and Priority enums"
```

### Step 3: Implement Repository Layer
```bash
codex "Create Spring Data JPA repository for Task with methods to enforce unique titles"
```

### Step 4: Build Service Layer
```bash
codex "Implement TaskService enforcing business rules (unique titles, future due dates, status restrictions) with meaningful exceptions"
```

### Step 5: Create REST Controllers
```bash
codex "Generate REST controllers that map to `/api/v1/tasks`, use record-based DTOs, and annotate endpoints for OpenAPI"
```

### Step 6: Add Exception Handling
```bash
codex "Create global exception handler with custom exceptions and meaningful error responses"
```

### Step 7: Configure Database
```bash
codex "Configure H2 with `schema.sql` + `data.sql` seeding and show how to defer initialization in `application.yml`"
```

### Step 8: Generate Tests
```bash
codex "Generate comprehensive test suite including unit tests for services and integration tests for controllers with at least 80% coverage"
```

### Step 9: Add Documentation
```bash
codex "Configure SpringDoc to expose `/api-docs` and customize Swagger UI metadata"
```

### Step 10: Performance & Security
```bash
codex "Discuss potential next steps such as rate limiting or Spring Security integration"
```

## Success Criteria

- [ ] All CRUD endpoints working as specified
- [ ] Validation rules enforced
- [ ] Error handling implemented
- [ ] Tests passing with >80% coverage
- [ ] Swagger UI accessible at http://localhost:8080/swagger-ui.html
- [ ] Code follows Spring Boot best practices

## Advanced Challenges

1. Add authentication with Spring Security and JWT
2. Implement task assignment to users
3. Add file attachments to tasks
4. Create WebSocket notifications for task updates
5. Add audit logging for all operations

## Testing Your Implementation

```bash
# Run the application
mvn spring-boot:run

# Run tests
mvn test

# Check test coverage
mvn jacoco:report

# Access Swagger UI
open http://localhost:8080/swagger-ui.html

# Test with curl
curl -X GET http://localhost:8080/api/v1/tasks
curl -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Description","status":"TODO","priority":"HIGH"}'
```

## Configuration Tips

Create an AGENTS.md file in the project root:

```markdown
# Task Management API

## Tech Stack
- Spring Boot 3.5
- Java 17
- H2 Database
- Spring Data JPA
- Spring Validation
- SpringDoc OpenAPI 2.7

## Conventions
- RESTful API design
- DTOs for request/response
- Service layer for business logic
- Repository pattern for data access
- Global exception handling
- Comprehensive testing

## Current Focus
Building CRUD operations for task management with proper validation and error handling.
```