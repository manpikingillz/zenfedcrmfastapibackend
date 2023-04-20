from sqlalchemy.orm import Session

from .database import SessionLocal
from typing import List
from fastapi import FastAPI, Depends, HTTPException

from . import models, schemas
from .database import Base, engine

# Create the database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance
app = FastAPI()


# Define a dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define the API endpoints
@app.get("/")
def read_root():
    return {"Hello": "<h1>Welcome to ZenFed</h1>"}


# Create an employee
@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# Read employees
@app.get("/employees/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees


# Read a single employee by ID
@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


# Update an employee
@app.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in employee:
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Delete an employee
@app.delete("/employees/{employee_id}", response_model=schemas.Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return db_employee
