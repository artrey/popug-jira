import enum

from pydantic import BaseModel

from schemes_generator import BaseEventV1


class TaskStatusEnumV1(enum.Enum):
    IN_PROGRESS = "В работе"
    COMPLETED = "Завершена"


class TaskDataV1(BaseModel):
    public_id: str
    title: str
    status: TaskStatusEnumV1
    executor_public_id: str


class TaskCreatedV1(BaseEventV1[TaskDataV1]):
    pass


class TaskUpdatedV1(BaseEventV1[TaskDataV1]):
    pass


class TaskDataV2(BaseModel):
    public_id: str
    title: str
    jira_id: str
    status: TaskStatusEnumV1
    executor_public_id: str


class TaskCreatedV2(BaseEventV1[TaskDataV2]):
    pass


class TaskUpdatedV2(BaseEventV1[TaskDataV2]):
    pass


class TaskAssignedDataV1(BaseModel):
    public_id: str
    executor_public_id: str


class TaskAssignedV1(BaseEventV1[TaskAssignedDataV1]):
    pass


class TaskCompletedDataV1(BaseModel):
    public_id: str
    executor_public_id: str


class TaskCompletedV1(BaseEventV1[TaskCompletedDataV1]):
    pass
