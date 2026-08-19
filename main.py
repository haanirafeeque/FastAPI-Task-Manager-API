from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from database import (
    init_database,
    get_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
)


app = FastAPI()


@app.on_event("startup")
def startup():
    init_database()


class Task(BaseModel):
    title: str


class UpdateTask(BaseModel):
    title: str | None = None
    Status: bool | None = None


@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
async def health():
    return {
        "Status": "OK"
    }


# GET ALL TASKS
@app.get("/tasks")
async def get_all_tasks():
    return get_tasks()


# GET TASK BY ID
@app.get("/tasks/{id}")
async def get_task_id(id: int):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Task not found"
            }
        )

    return task


# CREATE TASK
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_tasks(task: Task):

    if task.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Title was left empty"
            }
        )

    return create_task(task.title)


# UPDATE TASK
@app.put("/tasks/{id}")
async def update_tasks(id: int, updated_task: UpdateTask):

    if updated_task.title is None and updated_task.Status is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Title/Status was left empty"
            }
        )

    # Get the current task first
    current_task = get_task_by_id(id)

    if current_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": f"Task {id} not found"
            }
        )

    # Keep existing values if only one field is supplied
    title = (
        updated_task.title
        if updated_task.title is not None
        else current_task["title"]
    )

    done = (
        updated_task.Status
        if updated_task.Status is not None
        else current_task["Status"]
    )

    updated = update_task(id, title, done)

    return updated


# DELETE TASK
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tasks(id: int):

    deleted = delete_task(id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": f"Task {id} not found"
            }
        )

    return None