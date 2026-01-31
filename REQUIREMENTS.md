# TASK DESCRIPTION

## Objective

### Develop a Python-based RESTful API for managing tasks with emphasis on

- Data modeling
- ORM usage (e.g. SQLAlchemy)
- Secure authentication
- Automated testing (unit + DB integration)

### Functional Requirements

- User Management
  * POST /register: Register a new user with username and password
  * POST /login: Authenticate user, return a JWT token
- Task Management
  * GET /tasks: Return the list of tasks created by the authenticated user
  * POST /tasks: Create a new task which may contain fields like title, description, due_date, is_completed, etc.
  * PUT /tasks/{task_id}: Update a task
  * DELETE /tasks/{task_id}: Delete a task

### Bonus Points

  - Unit test using pytest
  - Containerization using Docker

### Deliverables

- Source code in a zip file.
- A README.md file detailing
  * Setup instructions (Python env and/or Docker)
  * API documentation
  * Briefly explanation of design decisions and assumptions

### Technical Requirements

- Language: Python 3.11+
- Framework: No specific requirement
- Database: SQLite or Postgres
- Auth: JWT-based
