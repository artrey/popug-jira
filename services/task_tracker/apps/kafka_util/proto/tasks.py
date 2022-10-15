import datetime as dt

from pydantic import BaseModel


class Task(BaseModel):
    title: str
    status: str
    executor_public_id: str
    created_at: dt.datetime
    updated_at: dt.datetime
