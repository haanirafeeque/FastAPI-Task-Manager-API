# FastAPI Task Manager

A simple Task Manager REST API built with **FastAPI** and **SQLite** to practice CRUD operations and REST API development.

## Features

* Create, Read, Update, and Delete tasks
* SQLite database for persistent storage
* Request validation with Pydantic
* HTTP exception handling
* Interactive API documentation with Swagger UI

## Tech Stack

* Python
* FastAPI
* SQLite
* Pydantic
* Uvicorn

## API Endpoints

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/`           | API information         |
| GET    | `/health`     | Health check            |
| GET    | `/tasks`      | Get all tasks           |
| GET    | `/tasks/{id}` | Get a task by ID        |
| POST   | `/tasks`      | Create a new task       |
| PUT    | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task           |

## Run Locally

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

The application automatically creates a `tasks.db` SQLite database on the first run.

## API Documentation

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

> **Note:** Tasks are stored in a SQLite database (`tasks.db`), so data persists between server restarts.
