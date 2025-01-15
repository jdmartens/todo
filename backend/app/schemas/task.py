from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    task_name: str
    due_date: datetime
    status: str
    type: str

class TaskUpdate(BaseModel):
    id: str
    task_name: str
    due_date: datetime
    status: str
    type: str

class TaskResponse(BaseModel):
    id: str
    task_name: str
    due_date: datetime
    status: Optional[str] = None 
    notified: bool
    type: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data['id'],
            task_name=data['task_name'],
            due_date=datetime.fromisoformat(data['due_date']),
            notified=data['notified'],
            type=data['type']
        )
