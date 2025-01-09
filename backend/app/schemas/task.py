from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    task_name: str
    due_date: datetime
    type: str

class TaskResponse(BaseModel):
    id: str
    task_name: str
    due_date: datetime
    status: str
    notified: bool
    type: str
