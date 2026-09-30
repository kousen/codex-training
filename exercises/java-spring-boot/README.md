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
   - GET /api/v1/tasks/search - Search by title or description

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

## Implementation

The `starter/` directory now contains the implemented Spring Boot 4.1.1 API using Java 17.
See [the application README](starter/README.md) for its exact API contract, run commands,
and test/coverage instructions. The prompt progression below is retained as lab guidance.

The [architecture guide](starter/ARCHITECTURE.md) explains the implemented system
with Mermaid diagrams of its layers, request flow, and task lifecycle.

## Starting a fresh lab

Despite its name, `starter/` on this branch contains the completed reference
implementation. To practice building the API, extract only the Spring Boot 4
scaffold from the fixed commit below. Keep this README open for the requirements.

Run from the `codex-training` repository root in a POSIX shell (macOS/Linux):

```bash
(
  set -eu
  lab_dir=../task-api-lab
  mkdir "$lab_dir"
  git archive 8a9cd4dc77dfce3fa2c05e96fa28708b5df9c807 \
    exercises/java-spring-boot/starter/pom.xml \
    exercises/java-spring-boot/starter/mvnw \
    exercises/java-spring-boot/starter/mvnw.cmd \
    exercises/java-spring-boot/starter/.mvn \
    exercises/java-spring-boot/starter/src/main/java/com/example/taskapi/TaskApiApplication.java \
    exercises/java-spring-boot/starter/src/main/resources/application.properties \
    > "$lab_dir/scaffold.tar"
  tar -xf "$lab_dir/scaffold.tar" -C "$lab_dir" --strip-components=3
  rm "$lab_dir/scaffold.tar"
)
```

The command requires that commit to be available locally. It creates a new sibling
folder and stops if that folder already exists. It does not alter the completed
reference application or check out an older course version.

In `../task-api-lab`, select JDK 17 and run `./mvnw clean verify`. This scaffold has
only the main application class, configuration, dependencies, wrapper, and coverage
setup. It has no task endpoints, entities, sample-data initializer, or tests yet;
JaCoCo therefore skips reporting and checking until tests exist. There is no
`starter/` subdirectory in the extracted project: run commands at its root.
Create an `AGENTS.md` there using the Configuration Tips below, and initialize a
Git repository there if you want to practice commits. The source repository's
agent instructions are not included in this separate folder.

The earlier commit `0b407b1` preserves the original Spring Boot 3.2 scaffold for
historical comparison; it is not the recommended baseline for this updated lab.

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
Configure H2 database and initialize sample data through the service layer for development
```

### Step 8: Generate Tests
```
Generate comprehensive test suite including unit tests for services and integration tests for controllers with at least 80% coverage
```

### Step 9: Add Documentation
```
Configure Swagger UI and add detailed OpenAPI documentation for all endpoints
```

### Step 10: Performance & Security (optional, not implemented)

This is an extension exercise. Security and rate limiting were discussed as
possible next steps; caching should address a measured need or an explicit teaching
objective. None of these additions is implemented or approved for implementation.

```
Add caching, rate limiting, and basic security configuration
```

## Success Criteria

- [x] All endpoints working as specified
- [x] Validation rules enforced
- [x] Error handling implemented
- [x] Tests passing with at least 80% coverage
- [x] Swagger UI accessible at /swagger-ui.html
- [x] Controllers, DTOs, transactional services, and repositories have separate responsibilities

These checks cover the implemented lab scope, not production readiness. See the
[design review follow-ups](starter/ARCHITECTURE.md#design-review-follow-ups) for
known improvements.

## Advanced Challenges

1. Add authentication with Spring Security and JWT
2. Implement task assignment to users
3. Add file attachments to tasks
4. Create WebSocket notifications for task updates
5. Add audit logging for all operations

## Testing Your Implementation

```bash
# Run from the starter directory with JDK 17
cd starter

# Run the application
./mvnw spring-boot:run

# Run tests
./mvnw test

# Run tests, package the application, and generate coverage
./mvnw clean verify
open target/site/jacoco/index.html

# Access Swagger UI
open http://localhost:8080/swagger-ui.html

# Test with curl
curl -X GET http://localhost:8080/api/v1/tasks
curl -X POST http://localhost:8080/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Description","status":"TODO","priority":"HIGH"}'
```

JaCoCo generates HTML and XML reports under `starter/target/site/jacoco/` after tests run.
The build enforces at least 80% overall line coverage and 80% line/branch coverage
for each service class across the combined unit and integration test suite.
Use JDK 17 for this exercise. The wrapper downloads Maven 3.9.16 on first use;
a separate Maven installation is not required. On Windows, use `mvnw.cmd`.

## Configuration Tips

The existing AGENTS.md defines the project rules. A minimal example is:

```markdown
# Task Management API

## Tech Stack
- Spring Boot 4.1.1
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
