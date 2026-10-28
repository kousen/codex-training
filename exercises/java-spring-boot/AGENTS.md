# Task Management API Project

## Scope

This exercise implements a local Spring Boot task-management REST API in `starter/`.
It is a training application, not a production deployment. See `starter/README.md`
for usage and `starter/ARCHITECTURE.md` for request flow and lifecycle diagrams.

Use Sonar only when the user explicitly requests it.

## Technology Stack

- Java 17, Spring Boot 3.2.0
- Maven Wrapper (`starter/mvnw`, `starter/mvnw.cmd`)
- Spring Data JPA and Hibernate
- H2 in-memory database
- Jakarta Bean Validation
- SpringDoc OpenAPI UI 2.3.0
- JUnit 5, Mockito, AssertJ, MockMvc
- JaCoCo 0.8.12

Dependency versions in this exercise are intentional training inputs. Do not
upgrade them as unrelated maintenance.

## Project Structure

All application paths below are relative to `starter/`:

- `src/main/java/com/example/taskapi/TaskApiApplication.java`: entry point
- `controller/`: HTTP concerns, request validation, pagination, response codes
- `service/`: business rules and transaction boundaries
- `repository/`: Spring Data JPA queries
- `entity/`: Task, Status, Priority and JPA timestamp callbacks
- `dto/`: request/response records and stable pagination envelope
- `exception/`: business exceptions and Problem Details translation

The package directories above are under `src/main/java/com/example/taskapi/`.
There are currently no `config/` or `util/` packages.

- `src/main/resources/application.properties`: application configuration
- `src/main/resources/data.sql`: three sample tasks loaded after schema creation
- `src/test/java/com/example/taskapi/unit/`: service and error-handler tests
- `src/test/java/com/example/taskapi/integration/`: MockMvc and repository tests
- `src/test/java/com/example/taskapi/TaskFixtures.java`: shared test fixtures

Hibernate generates the schema with `ddl-auto=create-drop`. There is no
`schema.sql` or `application.yml`. H2 data resets when the application stops.

## API Contract

Use only `/api/v1/tasks`; there is no unversioned `/api/tasks` alias.

| Method | Path | Success |
|---|---|---|
| GET | `/api/v1/tasks` | 200, paginated tasks |
| GET | `/api/v1/tasks/{id}` | 200, task |
| POST | `/api/v1/tasks` | 201, task and Location header |
| PUT | `/api/v1/tasks/{id}` | 200, updated task |
| DELETE | `/api/v1/tasks/{id}` | 204 |
| GET | `/api/v1/tasks/search?q=text` | 200, paginated search results |

- JSON requests/responses; dates and timestamps use ISO 8601.
- IDs must be positive. Pages are zero-based; size defaults to 20, allowed 1–100.
- Lists and searches are sorted by ID. The page response contains `content`,
  `page`, `size`, `totalElements`, and `totalPages`.
- Search is a case-insensitive literal substring match on title or description.
  `q` must be nonblank and at most 500 characters.
- Errors use Problem Details: 400 for invalid input, 404 for missing tasks,
  409 for business conflicts, and a generic 500 for unexpected failures.
- OpenAPI JSON: `/api-docs`; Swagger UI: `/swagger-ui.html`.

## Domain and Business Rules

Task fields: generated `Long id`, `String title`, `String description`, `Status
status`, `Priority priority`, optional `LocalDate dueDate`, `Instant createdAt`,
and `Instant updatedAt`.

1. Title is required, trimmed before storage, and case-sensitive unique.
   Bean Validation checks the raw title length (maximum 100) before trimming.
   A database unique constraint also protects against duplicate inserts.
2. Description is optional, maximum 500 characters.
3. Status values: TODO, IN_PROGRESS, DONE. Creation defaults to TODO.
4. Priority values: LOW, MEDIUM, HIGH. Creation defaults to MEDIUM.
5. IN_PROGRESS tasks cannot be deleted.
6. The direct DONE-to-TODO transition is blocked; DONE-to-IN_PROGRESS is allowed.
7. A creation due date must be after today in UTC. Updates may set past dates.
8. PUT requires a title. Omitted/null status and priority retain existing values;
   omitted/null description and dueDate clear those fields.
9. JPA callbacks set both timestamps on insertion and change `updatedAt` when
   persisted fields change. An identical update does not advance the timestamp.

## Implementation and Testing

- Return DTOs, never JPA entities, from controllers.
- Keep business rules in the service; the class uses read-only transactions,
  overridden by writable create, update, and delete methods.
- Keep Bean Validation on both HTTP input and proxied service entry points.
- Use parameterized repository queries and bounded pagination.
- `spring.jpa.open-in-view=false`; map entities to DTOs inside service transactions.
- Test service rules with Mockito, HTTP behavior with `@SpringBootTest` and
  MockMvc, and database behavior with `@DataJpaTest`. Reuse `TaskFixtures`.
- `verify` enforces at least 80% aggregate application line coverage, excluding
  the launcher. This is not a per-class or unit-test-only coverage guarantee.
- Keep generated `target/` artifacts out of commits.

Run from `starter/` with Java 17:

```bash
./mvnw spring-boot:run
./mvnw clean verify
```

On macOS with a newer default JDK:

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 17) ./mvnw clean verify
```

Use `mvnw.cmd` on Windows. Coverage report: `target/site/jacoco/index.html`.

## Known Limitations and Review Follow-ups

- Boot's enabled Problem Details advice currently takes precedence over custom
  request-body validation handling. The documented field-level `errors` array
  is missing from HTTP responses; test the body when fixing handler ordering.
  Preserve framework 404, 405, and 415 handling when changing the advice.
- Task has no optimistic version field. Overlapping updates/deletes can overwrite
  changes or bypass status guards; transactions alone do not prevent this.
- Extreme page/size combinations can exceed JPA's integer offset and return 500.
- Timestamp precision differences across JVM/platform and H2 storage were flagged
  by review but have not been verified on Linux.
- The API is unauthenticated and is not explicitly bound to loopback. H2 console
  remote access is disabled, but that does not restrict the REST API listener.
- Caching, rate limiting, authentication/authorization, and production deployment
  configuration are outside the current local exercise scope.
