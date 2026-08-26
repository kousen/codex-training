INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at)
VALUES ('Review API design', 'Review the v1 task API contract', 'IN_PROGRESS', 'HIGH', DATEADD('DAY', 3, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at)
VALUES ('Write integration tests', 'Cover successful requests and meaningful errors', 'TODO', 'MEDIUM', DATEADD('DAY', 7, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at)
VALUES ('Publish documentation', 'Verify the OpenAPI documentation before release', 'DONE', 'LOW', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
