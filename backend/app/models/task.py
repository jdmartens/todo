from datetime import datetime
from uuid import uuid4

class Task:
    def __init__(self, task_name: str, due_date: datetime, type: str):
        self.id = str(uuid4())
        self.task_name = task_name
        self.due_date = due_date
        self.status = "pending"
        self.notified = False
        self.type = type

    def to_dict(self):
        return {
            "id": self.id,
            "task_name": self.task_name,
            "due_date": self.due_date.isoformat(),
            "status": self.status,
            "notified": self.notified,
            "type": self.type
        }
