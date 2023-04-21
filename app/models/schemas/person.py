from typing import Optional
from pydantic import BaseModel


# Person schema for creating new Persons
class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    country_id: int


# Person schema for updating existing Persons
class PersonUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    country_id: Optional[int]


# Person schema for returning Persons in API responses
class PersonRetrieve(PersonCreate):
    id: int

    class Config:
        orm_mode = True


# Country schema for returning countries in API responses
class CountryRetrieve(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
