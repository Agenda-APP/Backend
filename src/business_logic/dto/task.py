from dataclasses import dataclass
from datetime import datetime

from enumerations import Priority, Status


@dataclass
class CategoryDTO:
    name: str


@dataclass
class TaskDTO:
    user_id: int
    status: Status
    end_date: datetime
    description: str
    category: str
    priority: Priority
