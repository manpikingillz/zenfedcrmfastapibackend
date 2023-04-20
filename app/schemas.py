from typing import Optional
from pydantic import BaseModel


# Employee schema for creating new employees
class EmployeeCreate(BaseModel):
    name: str
    age: int
    country_id: int


# Employee schema for updating existing employees
class EmployeeUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    country_id: Optional[int]


# Employee schema for returning employees in API responses
class Employee(EmployeeCreate):
    id: int

    class Config:
        orm_mode = True


# Country schema for returning countries in API responses
class Country(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
