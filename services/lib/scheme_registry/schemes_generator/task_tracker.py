import datetime as dt
import enum

from pydantic import BaseModel

from schemes_generator import BaseEventV1


class TaskStatusEnumV1(enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskCreatedDataV1(BaseModel):
    public_id: str
    title: str
    status: TaskStatusEnumV1
    executor_public_id: str
    created_at: dt.datetime
    updated_at: dt.datetime


class TaskCreatedV1(BaseEventV1[TaskCreatedDataV1]):
    pass
