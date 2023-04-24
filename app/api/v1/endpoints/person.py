from typing import List, Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.database.session import get_db
from app.models.schemas.person import (
    PersonRetrieve, PersonCreate, PersonUpdate)
from app.models.sql.person import Person
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Define the API endpoints
@router.get("/")
def read_root():
    return {"Hello": "Welcome to ZenFed CRM Persons Endpoints"}


# Create an person
@router.post("/persons/", response_model=PersonRetrieve)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


# Read persons
@router.get("/persons/", response_model=List[PersonRetrieve])
def read_persons(
        token: Annotated[str, Depends(oauth2_scheme)],
        skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db)):
    persons = db.query(Person).offset(skip).limit(limit).all()
    return {'person': persons, "token": token}


# Read a single person by ID
@router.get("/persons/{person_id}", response_model=PersonRetrieve)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


# Update an person
@router.put("/persons/{person_id}", response_model=PersonRetrieve)
def update_person(person_id: int, person: PersonUpdate,
                  db: Session = Depends(get_db)):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    for field, value in person:
        setattr(db_person, field, value)
    db.commit()
    db.refresh(db_person)
    return db_person


# Delete an person
@router.delete("/persons/{person_id}", response_model=PersonRetrieve)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(db_person)
    db.commit()
    return db_person
