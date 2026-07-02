insert into tasks (title, description, status, priority, due_date, created_at, updated_at)
values
    (
        'Review API requirements',
        'Confirm task management business rules before implementation.',
        'DONE',
        'HIGH',
        '2026-08-01',
        current_timestamp,
        current_timestamp
    ),
    (
        'Implement REST controller',
        'Expose CRUD endpoints under /api/v1/tasks.',
        'IN_PROGRESS',
        'HIGH',
        '2026-08-08',
        current_timestamp,
        current_timestamp
    ),
    (
        'Write service unit tests',
        'Cover title uniqueness, status transitions, and delete rules.',
        'TODO',
        'MEDIUM',
        '2026-08-15',
        current_timestamp,
        current_timestamp
    ),
    (
        'Document Swagger examples',
        'Verify OpenAPI descriptions and sample payloads.',
        'TODO',
        'LOW',
        '2026-08-22',
        current_timestamp,
        current_timestamp
    );
