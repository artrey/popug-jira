import enum

from pydantic import BaseModel


class UserRoleEnumV1(enum.Enum):
    ADMIN = "Администратор"
    MANAGER = "Менеджер"
    ACCOUNTANT = "Бухгалтер"
    POPUG = "Попуг"


class UserRegisteredV1(BaseModel):
    public_id: str
    username: str
    first_name: str
    last_name: str
    role: UserRoleEnumV1
