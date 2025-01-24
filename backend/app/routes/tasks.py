from fastapi import APIRouter, HTTPException, Query
from schemas.task import TaskComplete, TaskCreate, TaskUpdate, TaskResponse
from models.task import Task
from services import dynamodb
from typing import List

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks(status: str = Query(default="pending")):
    tasks = dynamodb.get_all_tasks(status)
    return [TaskResponse(**task) for task in tasks]

@router.post("/tasks/", response_model=TaskResponse)
async def add_task(task: TaskCreate):
    new_task = Task(task_name=task.task_name, due_date=task.due_date, type=task.type)
    dynamodb.add_task(new_task)
    return TaskResponse(**new_task.to_dict())

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def edit_task(task_id: str, task: TaskUpdate):
    try:
        updated_task = dynamodb.update_task(task_id, task)
        return TaskResponse(**updated_task)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: str, task: TaskComplete):
    try:
        updated_task = dynamodb.complete_task(task_id)
        return TaskResponse.from_dict(updated_task)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/task/{task_id}")
async def get_task(task_id: str):
    try:
        task = dynamodb.get_task(task_id)
        return TaskResponse(**task)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        dynamodb.delete_task(task_id)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")