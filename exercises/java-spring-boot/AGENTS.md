# Task Management API: Agent Instructions

## Scope and References

Work in `starter/`, a local Java 17 / Spring Boot training application.

- Read [architecture and API behavior](starter/ARCHITECTURE.md) before changing
  endpoints, business rules, persistence, or error handling.
- Read its [known limitations](starter/ARCHITECTURE.md#known-limitations-and-review-follow-ups)
  before claiming a review finding is fixed or behavior is production-ready.
- Use [the README](starter/README.md) for quick-start instructions and examples.
- Treat `starter/pom.xml` as the source for dependency versions. Exercise
  dependencies are intentional training inputs; avoid unrelated upgrades.
- Use Sonar only when the user explicitly requests it.

## Implementation Rules

- Keep the API at `/api/v1/tasks`; do not restore an unversioned alias.
- Return DTOs from controllers, never JPA entities.
- Keep HTTP concerns in controllers and business rules/transactions in services.
- Keep Bean Validation on HTTP input and proxied service entry points.
- Use parameterized repository queries and bounded pagination.
- Map entities to DTOs inside service transactions; keep open-in-view disabled.
- Preserve framework 404, 405, and 415 responses when changing exception advice.
- Update architecture documentation when behavior or known limitations change.
  Keep these instructions focused on how to work; avoid duplicating API details.

## Verification

Run from `starter/` using Java 17:

```bash
./mvnw spring-boot:run
./mvnw clean verify
```

On macOS with a newer default JDK:

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 17) ./mvnw clean verify
```

Use `mvnw.cmd` on Windows. Add service tests for business rules, full-context
MockMvc tests for HTTP behavior, and `@DataJpaTest` tests for persistence changes.
Reuse `src/test/java/com/example/taskapi/TaskFixtures.java`.

`verify` enforces 80% aggregate application line coverage, excluding the launcher.
The report is `target/site/jacoco/index.html`. Keep generated `target/` files out
of commits. Documentation-only edits need link and consistency checks.
