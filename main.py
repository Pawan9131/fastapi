# import modules
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


# Create an instance of the FastAPI application
app = FastAPI()


# Define a Pydantic model to represent the structure of a task
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[int] = None
    completed: bool = False

# An empty list to store task objects
tasks = []
task_counter = 1


# Define endpoint to retrieve the list of all tasks
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Define endpoint to add a new task to the list
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    global task_counter
    task.id = task_counter
    tasks.append(task)
    task_counter += 1
    return task

# Define endpoint to retrieve the details of a task by its ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Define endpoint to update the details of a task by its ID
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task = next((t for t in tasks if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated_task.title
    task.description = updated_task.description
    task.due_date = updated_task.due_date
    task.priority = updated_task.priority
    task.completed = updated_task.completed
    return task

# Define endpoint to delete a task by its ID
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return {"message": "Task deleted successfully"}


# Define endpoint to retrieve the list of tasks due on a specific date
@app.get("/tasks/due/{due_date}", response_model=List[Task])
def get_tasks_by_due_date(due_date: date):
    return [t for t in tasks if t.due_date == due_date]


# Define endpoint to retrieve the list of tasks with a specific priority
@app.get("/tasks/priority/{priority}", response_model=List[Task])
def get_tasks_by_priority(priority: int):
    return [t for t in tasks if t.priority == priority]
