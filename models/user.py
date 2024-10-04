from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base


# from .event import Event
# from .guest import GuestList
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    hashed_password = Column(String)
    email = Column(String)

    # one to many a user can create many events
    events = relationship('Event', back_populates='owner')

    # a user as a guest can be invited to many events: many to many
    events_as_guest = relationship("Event", secondary="guest_list", back_populates="guests")
