import enum

from pydantic import BaseModel

from schemes_generator import BaseEventV1


class UserRoleEnumV1(enum.Enum):
    ADMIN = "Администратор"
    MANAGER = "Менеджер"
    ACCOUNTANT = "Бухгалтер"
    POPUG = "Попуг"


class UserDataV1(BaseModel):
    public_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: UserRoleEnumV1


class UserCreatedV1(BaseEventV1[UserDataV1]):
    pass


class UserUpdatedV1(BaseEventV1[UserDataV1]):
    pass


class UserDeletedDataV1(BaseModel):
    public_id: str


class UserDeletedV1(BaseEventV1[UserDeletedDataV1]):
    pass
