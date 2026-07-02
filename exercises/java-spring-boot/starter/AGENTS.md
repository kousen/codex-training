# Task API Starter Infrastructure

This starter now contains a complete Spring Boot task management API for the Codex CLI training lab. These notes document the infrastructure choices in this directory and should be treated as local guidance in addition to the parent `../AGENTS.md`.

## Runtime Stack

- Spring Boot 3.2.0, Java 17, Maven
- Spring Web MVC for REST endpoints
- Spring Data JPA with H2 for local development
- Jakarta Bean Validation for request and entity validation
- SpringDoc OpenAPI for Swagger UI and `/api-docs`
- Spring Security with HTTP Basic for protected write operations
- Spring Cache backed by Caffeine
- Custom servlet filter for in-memory rate limiting
- JaCoCo coverage gate at 80% line coverage

## Local Endpoints

- API base path: `/api/v1`
- Task collection: `/api/v1/tasks`
- Swagger UI: `/swagger-ui.html`
- OpenAPI JSON: `/api-docs`
- H2 console: `/h2-console`

## Development Credentials

API write operations use HTTP Basic authentication.

- Username: `admin`
- Password: `changeme`

Only `POST`, `PUT`, and `DELETE` task endpoints require these credentials. `GET /api/v1/tasks/**`, Swagger UI, OpenAPI JSON, and the H2 console are public in the local development configuration.

The H2 console uses database credentials, not API credentials.

- JDBC URL: `jdbc:h2:mem:taskdb`
- User: `sa`
- Password: blank

## Database

The application uses explicit SQL initialization scripts:

- `src/main/resources/schema.sql` owns the `tasks` table and indexes.
- `src/main/resources/data.sql` inserts development sample tasks.
- `spring.jpa.hibernate.ddl-auto` is `none`; do not rely on Hibernate to create the schema.
- `spring.sql.init.mode` is `always` so sample data is available on startup.

Keep entity mappings and `schema.sql` in sync when changing persistence fields.

## Caching

Caching is enabled by `CacheConfig` and configured in `application.yml` with Caffeine.

Current cache names:

- `task`
- `tasks`
- `taskSearches`

`TaskService` caches read methods and evicts all task caches on create, update, and delete. If new read methods are added, cache them only when their parameters are stable and make sure all write paths invalidate stale data.

## Rate Limiting

`RateLimitingFilter` applies to `/api/v1/**` requests.

Defaults in `application.yml`:

- Enabled: `true`
- Requests: `100`
- Window: `1m`

The limiter uses `X-Forwarded-For` when present, otherwise `remoteAddr`. It is intentionally in-memory for lab simplicity and should not be treated as distributed production rate limiting.

## Security

`SecurityConfig` defines the request rules:

- Permit Swagger/OpenAPI and H2 console.
- Permit `GET /api/v1/tasks/**`.
- Require HTTP Basic authentication for mutating task endpoints.
- Disable CSRF for this stateless JSON API.
- Allow same-origin frames so the H2 console works locally.

OpenAPI declares the `basicAuth` security scheme in `OpenApiConfig`, and write operations in `TaskController` reference it.

## Error Handling

`GlobalExceptionHandler` returns `ErrorResponse` for validation failures, not-found cases, business-rule conflicts, rate limiting, malformed JSON, unsupported media types, unsupported methods, and unexpected errors.

Expected status codes:

- `400` validation, malformed JSON, or bad parameter values
- `401` missing or invalid credentials on protected endpoints
- `404` missing task
- `409` duplicate title or invalid business transition
- `429` rate limit exceeded
- `500` unexpected failures

## Testing And Verification

Run the full verification suite before handing off infrastructure changes:

```bash
mvn verify
```

The suite includes:

- `TaskServiceTest` for business logic
- `TaskControllerIntegrationTest` for MockMvc endpoint behavior and security
- `TaskRepositoryTest` for JPA/search behavior
- `RateLimitingFilterTest` for limiter behavior

The JaCoCo coverage gate runs during `verify` and must remain at or above 80% line coverage.

## Implementation Guidance

- Keep controllers thin; convert DTOs to entities and delegate business logic to `TaskService`.
- Do not expose JPA entities directly from the API response contract.
- Keep infrastructure configuration in `config/`; request filters belong in `web/`.
- When adding write operations, update caching eviction, security expectations, OpenAPI docs, and tests together.
- When changing sample data or schema, verify both `/api/v1/tasks` and the H2 console still work after application startup.
