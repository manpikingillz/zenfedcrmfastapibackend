from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# SQLAlchemy model definitions for our database tables
class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String)


# define an Employee model
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    salary = Column(Integer)
    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Country', backref='employees')