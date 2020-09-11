from typing import Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: Optional[int] = None
    description: str
    done: Optional[bool] = False

class TaskManager(BaseModel):
    tasks: Dict[int, Task] = {}

manager = TaskManager()

@app.get("/")
def read_root():
    return {"App": "Task Manager"}

@app.post("/task/")
async def create_task(task: Task):
    i = len(manager.tasks) + 1
    task.id = i
    manager.tasks[i] = task
    return task

@app.put("/task/{task_id}")
async def update_task(task_id: int, task: Task):
    manager.tasks[task_id].description = task.description
    return manager.tasks[task_id]

@app.put("/task/done/{task_id}")
async def update_task_done(task_id: int):
    manager.tasks[task_id].done = True
    return manager.tasks[task_id]

@app.put("/task/undone/{task_id}")
async def update_task_undone(task_id: int):
    manager.tasks[task_id].done = False
    return manager.tasks[task_id]

@app.delete("/task/{task_id}")
async def delete_task(task_id: int):
    del manager.tasks[task_id]
    return {"task_id": task_id}

@app.get("/tasks/")
async def gets_tasks():
    return manager.tasks

@app.get("/tasks/done/")
async def gets_tasks_done():
    tasks_done: Dict[int, Task] = {}
    for task_id in manager.tasks:
        if manager.tasks[task_id].done:
            tasks_done[task_id]=manager.tasks[task_id]
    return tasks_done

@app.get("/tasks/undone/")
async def gets_tasks_undone():
    tasks_done: Dict[int, Task] = {}
    for task_id in manager.tasks:
        if not(manager.tasks[task_id].done):
            tasks_done[task_id]=manager.tasks[task_id]
    return tasks_done

