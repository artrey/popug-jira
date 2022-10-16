import enum

from pydantic import BaseModel

from schemes_generator import BaseEventV1


class UserRoleEnumV1(enum.Enum):
    ADMIN = "Администратор"
    MANAGER = "Менеджер"
    ACCOUNTANT = "Бухгалтер"
    POPUG = "Попуг"


class UserRegisteredDataV1(BaseModel):
    public_id: str
    username: str
    first_name: str
    last_name: str
    role: UserRoleEnumV1


class UserRegisteredV1(BaseEventV1[UserRegisteredDataV1]):
    pass
