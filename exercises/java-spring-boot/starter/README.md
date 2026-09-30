# Task Management API

Implemented REST API using Spring Boot 4.1.1, Java 17, Spring Data JPA, H2,
Jakarta Bean Validation, SpringDoc 3.1.1, and JaCoCo.

See the [architecture guide](ARCHITECTURE.md) for Mermaid diagrams of the application
layers, request flow, and task lifecycle, plus persistence and testing details.

For a fresh implementation exercise, follow the [scaffold extraction instructions](../README.md#starting-a-fresh-lab).
The `starter/` folder in this branch is the completed reference application.

## Run

From this directory, with JDK 17 selected:

```bash
./mvnw spring-boot:run
```

The Maven 3.9.11 wrapper downloads Maven on first use. Windows users can use
`mvnw.cmd` instead of `./mvnw`. No separate Maven installation is needed.

- API: <http://localhost:8080/api/v1/tasks>
- Swagger UI: <http://localhost:8080/swagger-ui.html>
- OpenAPI JSON: <http://localhost:8080/api-docs>
- H2 console: <http://localhost:8080/h2-console>

For the H2 console use JDBC URL `jdbc:h2:mem:taskdb`, username `sa`, and an empty
password. This development database is in memory and resets on restart.
Three example tasks are seeded at startup. To start with an empty database:

```bash
./mvnw spring-boot:run -Dspring-boot.run.arguments=--app.sample-data.enabled=false
```

## API contract

| Method | Path | Success |
| --- | --- | --- |
| GET | `/api/v1/tasks?page=0&size=20` | 200, paginated tasks |
| GET | `/api/v1/tasks/{id}` | 200, one task |
| POST | `/api/v1/tasks` | 201, task and `Location` header |
| PUT | `/api/v1/tasks/{id}` | 200, replaced task |
| DELETE | `/api/v1/tasks/{id}` | 204, empty response |
| GET | `/api/v1/tasks/search?q=work&page=0&size=20` | 200, paginated matches |

Pages are zero-based, default size is 20, and allowed sizes are 1–100.
Offsets (`page * size`) above 2,147,483,647 are rejected with 400.
Results are ordered by ID ascending. Lists and search return:

```json
{
  "content": [],
  "page": 0,
  "size": 20,
  "totalElements": 0,
  "totalPages": 0
}
```

Search is a case-insensitive literal substring match against title or description.
The required `q` parameter is trimmed, must be nonblank, and has a 500-character
limit. `%` and `_` are literal characters, not search wildcards.

Create a task:

```bash
curl -i http://localhost:8080/api/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Write API tests","description":"Cover the business rules","priority":"HIGH"}'
```

Use the returned ID to update or delete it:

```bash
curl -X PUT http://localhost:8080/api/v1/tasks/4 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Write API tests","status":"DONE","priority":"HIGH"}'
curl -X DELETE http://localhost:8080/api/v1/tasks/4
```

### Validation and business rules

- Title is required, nonblank, and at most 100 characters. Surrounding whitespace
  is removed. Uniqueness ignores case using `Locale.ROOT`, and is enforced in the
  service and by a database unique constraint on the normalized title.
- Description is optional and at most 500 characters.
- Status values are `TODO`, `IN_PROGRESS`, and `DONE`. Creation defaults to `TODO`
  when status is omitted or null; an explicitly supplied valid status is accepted.
- Priority values are `LOW`, `MEDIUM`, and `HIGH`. Creation defaults to `MEDIUM`
  when omitted or null.
- Optional due dates use `YYYY-MM-DD` and must be strictly after today in UTC on
  creation. Updates may retain or set past dates to represent overdue work.
- `PUT` replaces all editable fields. Title, status, and priority are required;
  omitted/null description and due date are cleared.
- `DONE` cannot move directly to `TODO`. Other status transitions are allowed.
- `IN_PROGRESS` tasks cannot be deleted.
- IDs must be positive. Missing tasks return 404.
- `createdAt` and `updatedAt` are server-managed UTC instants. Creation time is
  preserved and update time advances on every successful update, even in the same
  clock tick. Optimistic locking rejects conflicting concurrent writes with 409.

### Error responses

Errors use a consistent JSON structure, with field-specific validation messages
where available:

```json
{
  "timestamp": "2030-06-15T12:00:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Request validation failed",
  "path": "/api/v1/tasks",
  "fieldErrors": {"title": "must not be blank"}
}
```

Invalid input returns 400, missing tasks 404, and duplicate titles or business-rule
conflicts 409. Unexpected failures return a generic 500 message; details stay in
server logs. Responses expose DTOs, never persistence entities or internal versions.

## Tests and coverage

```bash
./mvnw clean verify
open target/site/jacoco/index.html
```

The suite includes Mockito service tests, full-context MockMvc endpoint tests,
`@DataJpaTest` repository tests, and error/seed-data tests. Test clocks are fixed
so date and timestamp assertions do not depend on the day the tests run. Endpoint
tests disable sample data and use a separate in-memory database.

`verify` produces HTML/XML coverage reports under `target/site/jacoco/` and enforces
at least 80% overall line coverage plus 80% line and branch coverage for each
service class. The gate measures the combined suite, including integration tests.

## Structure and scope

Controllers handle HTTP and DTO validation; the transactional service applies
business rules; repositories handle persistence. Hibernate creates the development
schema. A conditional startup initializer seeds sample tasks through the service,
so no separate `schema.sql` or `data.sql` is needed.

Configuration lives exclusively in `src/main/resources/application.properties`.
Open Session in View is disabled; DTOs are mapped inside service transactions.
This lab has no authentication, rate limiting, or caching. Those are optional
extensions, not approved implementation work. See the
[design review follow-ups](ARCHITECTURE.md#design-review-follow-ups) for known
improvements and the distinction between implemented decisions and proposals.
Treat task text as plain text when displaying it in a browser; clients must escape
it for their rendering context rather than insert it as HTML.
