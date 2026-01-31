REST API demo project written in Python

# Docs

API documentation is available at http://127.0.0.1:8000/docs#/ when running the app locally.

# Useful commands

## Build docker image for dev

docker build -t py_rest_demo -f Dockerfile.dev .

## Run docker image for dev

docker run --rm -p 8000:8000 -v $(pwd)/app:/app -e SECRET_KEY=gouda_kaas py_rest_demo

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

curl -i -X PUT "http://127.0.0.1:8000/tasks/52066650752017374089771338888820989312" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{

    "title": "Drink milk",
    "description": "Drink absurd amount of milk",
    "due_date": "2025-03-01"

  }'

## Delete task (Requires token)

curl -i -X DELETE "http://127.0.0.1:8000/tasks/52066650752017374089771338888820989312" \
  -H "Authorization: Bearer $TOKEN"
