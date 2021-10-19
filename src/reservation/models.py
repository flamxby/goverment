from .database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Reservation(Base):
    __tablename__ = 'reservations'

    reservation_id = Column(Integer, primary_key=True, index=True)
    register_timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    owner = relationship("User", back_populates="reservations")

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    citizen_id = Column(String, unique=True, index=True)
    birth_date = Column(Date)
    occupation = Column(String)
    address = Column(String)
    password = Column(String)

    reservations = relationship("Reservation", back_populates="owner")

    