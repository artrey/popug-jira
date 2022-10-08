import dataclasses
import typing as ty

T = ty.TypeVar("T")


@dataclasses.dataclass
class Message(ty.Generic[T]):
    entity: str
    event: str  # create | update | delete | business
    public_id: str
    data: T


@dataclasses.dataclass
class User:
    username: str
    first_name: str
    last_name: str
    role: str
