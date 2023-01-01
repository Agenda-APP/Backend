from dataclasses import dataclass
from datetime import datetime

from src.enumerations import Status, Priority


@dataclass
class CategoryDTO:
    name: str


@dataclass
class TaskDTO:
    status: Status
    end_date: datetime
    description: str
    category: CategoryDTO
    priority: Priority
    user_id: int | None = None
