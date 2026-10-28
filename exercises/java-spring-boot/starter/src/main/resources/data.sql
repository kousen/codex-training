INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at) VALUES
('Learn Spring Boot', 'Build a task management REST API', 'TODO', 'HIGH', DATEADD('DAY', 7, CURRENT_DATE), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Write service tests', 'Cover business rules with JUnit and Mockito', 'IN_PROGRESS', 'MEDIUM', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Review API design', 'Confirm DTOs and versioned endpoints', 'DONE', 'LOW', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
