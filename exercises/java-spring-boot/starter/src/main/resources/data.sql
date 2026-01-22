insert into tasks (title, description, status, priority, due_date, created_at, updated_at)
values ('Write README', 'Draft initial project documentation', 'TODO', 'MEDIUM', dateadd('DAY', 7, current_date), current_timestamp, current_timestamp);

insert into tasks (title, description, status, priority, due_date, created_at, updated_at)
values ('Set up CI', 'Add GitHub Actions workflow', 'IN_PROGRESS', 'HIGH', dateadd('DAY', 14, current_date), current_timestamp, current_timestamp);
