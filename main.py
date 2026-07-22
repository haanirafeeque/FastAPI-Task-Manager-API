from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {
        "id":1,"title":"Study","Status" : False
    },
    {
        "id":2,"title":"Writing","Status":True
    }
]


class Task(BaseModel):
    title:str
    Status:bool

@app.get("/")
async def root():
    return{ "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def root():
    return{"Status": "OK"}

@app.get("/tasks")
async def get_task():
    return tasks

@app.get("/tasks/{id}")
async def get_task_id(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                         detail=  { "error": f"Task {id} not found" })


@app.post("/tasks")
async def create_tasks(task:Task):
    if task.title.strip() == "":
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=  { "error": "Title was left empty" })
        return  
    else:               
        id=len(tasks)+1
        new_tasks={
            "id":id,
            "title":task.title,
            "Status":task.Status
        }
        tasks.append(new_tasks)
        return new_tasks