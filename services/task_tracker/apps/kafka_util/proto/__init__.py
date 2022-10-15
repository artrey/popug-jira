import enum
import typing as ty

from pydantic.generics import GenericModel

T = ty.TypeVar("T")


class EventType(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    BUSINESS = "business"


class Message(GenericModel, ty.Generic[T]):
    entity: str
    event: EventType
    public_id: str
    data: ty.Optional[T]


from .tasks import *  # noqa: E402
from .users import *  # noqa: E402
