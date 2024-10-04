from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
# from .guest import GuestList


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(DateTime)
    location = Column(String)
    # there can be one organiser to a Event
    organiser_id = Column(Integer, ForeignKey('users.id'))
    is_cancelled = Column(Boolean, default=False)

    # a user can create many events: one to many
    owner = relationship('User', back_populates='events')

    # an event can have many guests : many to many
    guests = relationship('User', secondary='guest_list', back_populates='events_as_guest')
