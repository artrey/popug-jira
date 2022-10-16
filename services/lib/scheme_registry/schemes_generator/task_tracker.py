import datetime as dt
import enum

from pydantic import BaseModel


class TaskStatusEnumV1(enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskCreatedV1(BaseModel):
    public_id: str
    title: str
    status: TaskStatusEnumV1
    executor_public_id: str
    created_at: dt.datetime
    updated_at: dt.datetime
