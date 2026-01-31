REST API demo project written in Python for Qpurpose

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
# Docs

API documentation is available at http://127.0.0.1:8000/docs#/ when running the app locally.

# Useful commands

## Build docker image for dev

docker build -t qpurpose -f Dockerfile.dev .

## Run docker image for dev

docker run --rm -p 8000:8000 -v $(pwd)/app:/app -e SECRET_KEY=gouda_kaas qpurpose

## Create user

curl -i -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{

    "username": "larssaalbrink@gmail.com",
    "password": "kaaskop"

  }'

## Get token (and store it in TOKEN env var)

export TOKEN=$(curl -s -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=larssaalbrink@gmail.com" \
  -d "password=kaaskop" | jq -r '.access_token')

## Create task (Requires token)

curl -i -X POST "http://127.0.0.1:8000/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{

    "title": "Eat cheese",
    "description": "Eat all cheese currently in the fridge",
    "due_date": "2025-02-21"

  }'

## Get tasks (Requires token)

curl http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer $TOKEN"

## Update task (Requires token)

curl -i -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{

    "title": "Drink milk",
    "description": "Drink absurd amount of milk",
    "due_date": "2025-03-01"

  }'

## Delete task (Requires token)

curl -i -X DELETE "http://127.0.0.1:8000/tasks/143576189474197533500373928514628228997" \
  -H "Authorization: Bearer $TOKEN"
