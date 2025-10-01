INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at)
VALUES ('Initial Project Setup', 'Configure the base Spring Boot project structure', 'TODO', 'MEDIUM', DATEADD('DAY', 7, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at)
VALUES ('Draft API Specification', 'Outline endpoints and request/response models', 'IN_PROGRESS', 'HIGH', DATEADD('DAY', 14, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
