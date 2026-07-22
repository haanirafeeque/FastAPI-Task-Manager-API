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

class update_task(BaseModel):
    title:str | None = None
    Status:bool | None = None

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
            "Status":False
        }
        tasks.append(new_tasks)
        return new_tasks
    
@app.post("/tasks/{id}")
async def update_tasks(id:int ,updated_task:update_task ):
    for task in tasks:
        if task["id"] == id:
            if updated_task.title == None and updated_task.Status == None:
                raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail=  { "error": "Title/Status was left empty" })
                return
            elif updated_task.title is not None :
                task["title"] = updated_task.title
                return task
            elif updated_task.Status is not None or updated_task.title==None:
                task["Status"] = updated_task.Status
                return task
    raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                         detail=  { "error": f"Task {id} not found" })

@app.delete("/tasks/{id}")
async def delete_tasks(id:int):
    flag=0
    for task in tasks:
        if task["id"] == id:
            flag=1
            tasks.remove(task)
    if flag == 0:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                         detail=  { "error": f"Task {id} not found" })
        return
    if flag == 1 :
        for task in tasks:
            if task["id"]>id:
                task["id"] -=1
        raise HTTPException (status_code=status.HTTP_204_NO_CONTENT,
                             detail= {"Success": "The task was deleted Succesfull"})
        return