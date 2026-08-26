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
   - GET /api/v1/tasks - List all tasks (with pagination)
   - GET /api/v1/tasks/{id} - Get single task
   - POST /api/v1/tasks - Create new task
   - PUT /api/v1/tasks/{id} - Update task
   - DELETE /api/v1/tasks/{id} - Delete task
   - GET /api/v1/tasks/search?query=... - Search by title or description

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
```
Analyze the current Spring Boot project structure and identify what needs to be added for a task management API
```

### Step 2: Create Domain Model
```
Create JPA entities for Task with proper annotations, validation, and auditing. Include Status and Priority enums
```

### Step 3: Implement Repository Layer
```
Create Spring Data JPA repository for Task with custom query methods for searching and filtering
```

### Step 4: Build Service Layer
```
Implement TaskService with business logic including validation rules and error handling
```

### Step 5: Create REST Controllers
```
Generate REST controllers with proper HTTP status codes, request/response DTOs, and OpenAPI annotations
```

### Step 6: Add Exception Handling
```
Create global exception handler with custom exceptions and meaningful error responses
```

### Step 7: Configure Database
```
Configure H2 database with initialization scripts and sample data for development
```

### Step 8: Generate Tests
```
Generate a comprehensive test suite including unit tests for services and integration tests for controllers with at least 80% line and branch coverage
```

### Step 9: Add Documentation
```
Configure Swagger UI and add detailed OpenAPI documentation for all endpoints
```

### Optional Step 10: Production Hardening
```
Review the completed API and recommend production-hardening improvements without implementing them
```

The core lab ends after Step 9. Caching, rate limiting, security, and production
infrastructure are optional follow-up topics rather than required features.

## Success Criteria

- [ ] All endpoints working as specified
- [ ] Validation rules enforced
- [ ] Error handling implemented
- [ ] Tests passing with at least 80% line and branch coverage
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
# Enter the Maven project
cd starter

# Run the application
mvn spring-boot:run

# Run tests, package the application, and enforce coverage
mvn verify

# Access Swagger UI
open http://localhost:8080/swagger-ui.html

# Test with curl
curl -X GET http://localhost:8080/api/v1/tasks
curl -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Description","status":"TODO","priority":"HIGH"}'
```

## Project Guidance

The exercise includes an `AGENTS.md` file with the project conventions Codex
should follow. The complete one-shot assignment is available in
`starter/TASK-API-PROMPT.md`; the progression above can be used instead when the
instructor wants students to build the application incrementally.
