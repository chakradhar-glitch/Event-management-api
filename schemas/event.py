from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    title: str
    date: datetime
    location: str
    is_cancelled: bool

    class Config:
        orm_mode = True


class EventResponseModel(EventBase):
    id: int

    class Config:
        orm_mode = True


class Guest(BaseModel):
    name: str
    email: str
