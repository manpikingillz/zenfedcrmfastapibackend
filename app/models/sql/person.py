from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


# SQLAlchemy model definitions for our database tables
class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String)


# define an Person model
class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(255))
    phone_number = Column(String(20))
    address = Column(String(255))
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country', backref='persons')
