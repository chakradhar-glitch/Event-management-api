from sqlalchemy import Column, String,ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from database.database import Base
# from models.event import Event
# from models.user import User


class GuestList(Base):
    __tablename__ = 'guest_list'
    event_id = Column('event_id',Integer, ForeignKey('events.id'), primary_key=True)
    guest_id = Column('guest_id', Integer,ForeignKey('users.id'), primary_key=True)

