# Task Management API

A local Java 17 / Spring Boot task-management exercise with JPA, H2, Bean
Validation, and Swagger. The API base path is `/api/v1/tasks`.

## Quick start

Run from this directory with Java 17:

```bash
./mvnw spring-boot:run
```

The Maven wrapper downloads Maven on first use. Use `mvnw.cmd` on Windows.

- Swagger UI: http://localhost:8080/swagger-ui.html
- OpenAPI JSON: http://localhost:8080/api-docs
- H2 console: http://localhost:8080/h2-console
  (JDBC URL `jdbc:h2:mem:taskdb`, user `sa`, empty password)

```bash
curl http://localhost:8080/api/v1/tasks
curl -i http://localhost:8080/api/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Try the API","description":"Create a task","priority":"HIGH"}'
curl 'http://localhost:8080/api/v1/tasks/search?q=API&size=5'
```

Three sample tasks load at startup. H2 data resets on restart.

## Verification

```bash
./mvnw clean verify
```

On macOS with a newer default JDK:

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 17) ./mvnw clean verify
```

Tests and an 80% aggregate line coverage gate run during `verify`. Open
`target/site/jacoco/index.html` for the coverage report.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the API contract, business rules,
implementation diagrams, and [known limitations](ARCHITECTURE.md#known-limitations-and-review-follow-ups).
Agent contribution instructions are in [AGENTS.md](../AGENTS.md).
