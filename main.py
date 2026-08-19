from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
    
from database import init_database

app = FastAPI()

@app.on_event("startup")
def startup():
    init_database()


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
    f=cur.execute("SELECT * FROM TASKS")
    res=f.fetchall()
    tasks=[]
    for i in res:
        tasks.append({"id":i[0],"title":i[1],"Status":i[2]})
    return tasks


@app.get("/tasks/{id}")
async def get_task_id(id:int):
    f=cur.execute(f"Select * From TASKS WHERE ID = ?",(id,))
    r=f.fetchone()
    if r == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                                 detail=  { "error": f"Task {id} not found" })
    return {"id":r[0],"title":r[1],"Status":r[2]}




@app.post("/tasks")
async def create_tasks(task:Task):
    if task.title.strip() == "":
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=  { "error": "Title was left empty" })
        return  
    else:               
        cur.execute("INSERT INTO tasks (title, done) VALUES (?, 0)",(task.title,))
        con.commit()
        return
        




@app.put("/tasks/{id}")
async def update_tasks(id:int ,updated_task:update_task ):
        f=cur.execute("SELECT * FROM TASKS WHERE ID = ?",(id,))
        r=f.fetchone()
        if r == None:
             raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                                     detail=  { "error": f"Task {id} not found" })
        if updated_task.title == None and updated_task.Status == None:
                    raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail=  { "error": "Title/Status was left empty" })
        if updated_task.title is not None :
            f=cur.execute("UPDATE TASKS SET TITLE = ? WHERE ID =?",(updated_task.title,id))
            con.commit()

        if updated_task.Status is not None :
            f=cur.execute("UPDATE TASKS SET DONE = ? WHERE ID =?",(updated_task.Status,id))
            con.commit()
        f=cur.execute("SELECT * FROM TASKS WHERE ID =?",(id,))
        r=f.fetchone()
        return {"id":r[0],"title":r[1],"Status":r[2]}
        
   



@app.delete("/tasks/{id}")
async def delete_tasks(id:int):
    f=cur.execute("SELECT * FROM TASKS WHERE ID = ?",(id,))
    r=f.fetchone()
    if r == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, 
                                  detail=  { "error": f"Task {id} not found" })
    else:
        f=cur.execute("DELETE FROM TASKS WHERE ID = ?",(id,))
        con.commit()
        raise HTTPException (status_code=status.HTTP_204_NO_CONTENT,
                                    detail= {"Success": "The task was deleted Succesfull"})  

