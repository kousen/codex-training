# Lab 1: Spring Boot Task Management API

## Objective
Use Codex to build a complete REST API for task management with Spring Boot.

## Requirements

Build a Spring Boot application that includes:

1. **Domain Model**
   - Task entity with fields: id, title, description, status, priority, dueDate, createdAt, updatedAt
   - Status enum: TODO, IN_PROGRESS, DONE
   - Priority enum: LOW, MEDIUM, HIGH

2. **REST Endpoints**
   - GET /api/tasks - List all tasks (with pagination)
   - GET /api/tasks/{id} - Get single task
   - POST /api/tasks - Create new task
   - PUT /api/tasks/{id} - Update task
   - DELETE /api/tasks/{id} - Delete task
   - GET /api/tasks/search - Search by title or description

3. **Data Layer**
   - H2 in-memory database
   - Spring Data JPA repositories
   - Database initialization with sample data

4. **Business Logic**
   - Service layer with business rules
   - Task cannot be deleted if status is IN_PROGRESS
   - Automatic timestamp management

5. **Validation & Error Handling**
   - Input validation using Bean Validation
   - Global exception handler
   - Meaningful error responses

6. **Documentation**
   - OpenAPI/Swagger documentation
   - API versioning (/api/v1/)

7. **Testing**
   - Unit tests for services
   - Integration tests for controllers
   - Test data fixtures

## Starting Point

The `starter/` directory contains a basic Spring Boot project structure.

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
codex "Create Spring Data JPA repository for Task with custom query methods for searching and filtering"
```

### Step 4: Build Service Layer
```bash
codex "Implement TaskService with business logic including validation rules and error handling"
```

### Step 5: Create REST Controllers
```bash
codex "Generate REST controllers with proper HTTP status codes, request/response DTOs, and OpenAPI annotations"
```

### Step 6: Add Exception Handling
```bash
codex "Create global exception handler with custom exceptions and meaningful error responses"
```

### Step 7: Configure Database
```bash
codex "Configure H2 database with initialization scripts and sample data for development"
```

### Step 8: Generate Tests
```bash
codex "Generate comprehensive test suite including unit tests for services and integration tests for controllers with at least 80% coverage"
```

### Step 9: Add Documentation
```bash
codex "Configure Swagger UI and add detailed OpenAPI documentation for all endpoints"
```

### Step 10: Performance & Security
```bash
codex "Add caching, rate limiting, and basic security configuration"
```

## Success Criteria

- [ ] All endpoints working as specified
- [ ] Validation rules enforced
- [ ] Error handling implemented
- [ ] Tests passing with >80% coverage
- [ ] Swagger UI accessible at /swagger-ui.html
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
./mvnw spring-boot:run

# Run tests
./mvnw test

# Check test coverage
./mvnw jacoco:report

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
- Spring Boot 3.2
- Java 17
- H2 Database
- Spring Data JPA
- Spring Validation
- SpringDoc OpenAPI

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