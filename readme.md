# FastAPI Task Manager

A simple Task Manager REST API built with **FastAPI** to practice CRUD operations and REST API fundamentals.

## Features

* Create, Read, Update, and Delete tasks
* Request validation with Pydantic
* HTTP exception handling
* Interactive API documentation with Swagger UI

## Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn

## Endpoints



## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| POST | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task |
## Run Locally

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Open the API documentation at:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

> **Note:** This project uses an in-memory list to store tasks, so data is reset whenever the server restarts.
