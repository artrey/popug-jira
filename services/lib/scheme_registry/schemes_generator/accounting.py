from pydantic import BaseModel

from schemes_generator import BaseEventV1


class TaskDataV1(BaseModel):
    public_id: str
    cost_assign: int
    cost_complete: int


class TaskUpdatedV1(BaseEventV1[TaskDataV1]):
    pass


class AccountDataV1(BaseModel):
    public_id: str
    balance: int
    owner_public_id: str


class AccountCreatedV1(BaseEventV1[AccountDataV1]):
    pass


class AccountUpdatedV1(BaseEventV1[AccountDataV1]):
    pass
