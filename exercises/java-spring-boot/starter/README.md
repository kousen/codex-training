# Task API Starter

This is the starting point for Lab 1: Spring Boot Task Management API.

## What's Included

- `pom.xml` - Maven configuration with all required dependencies
- `TaskApiApplication.java` - Spring Boot main class
- `application.yml` - Database and OpenAPI configuration

## What You'll Build

Using Codex, you'll add:
- Task entity with JPA annotations
- Status and Priority enums
- TaskRepository with custom queries
- TaskService with business logic
- TaskController with REST endpoints
- Exception handling
- Tests

## Quick Start

```bash
# Run the application
mvn spring-boot:run

# Access H2 console
open http://localhost:8080/h2-console

# Access Swagger UI (after adding endpoints)
open http://localhost:8080/swagger-ui.html
```

## First Codex Prompt

```
Create a Task entity with id, title, description, status, priority,
dueDate, createdAt, and updatedAt fields. Include Status and Priority enums.
```
