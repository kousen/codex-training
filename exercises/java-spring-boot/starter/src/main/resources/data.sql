INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at)
VALUES
    ('Write workshop outline', 'Draft the hands-on flow for the Codex training lab', 'TODO', 'HIGH', DATEADD('DAY', 7, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Review starter project', 'Check the Spring Boot starter dependencies and package layout', 'IN_PROGRESS', 'MEDIUM', DATEADD('DAY', 3, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Publish lab notes', 'Finalize the task API exercise notes for students', 'DONE', 'LOW', DATEADD('DAY', 14, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
