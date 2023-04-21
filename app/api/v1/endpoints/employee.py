from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.database.session import get_db
from app.models.schemas.employee import (
    EmployeeRetrieve, EmployeeCreate, EmployeeUpdate)
from app.models.sql.employee import Employee

router = APIRouter()


# Define the API endpoints
@router.get("/")
def read_root():
    return {"Hello": "<h1>Welcome to ZenFed</h1>"}


# Create an employee
@router.post("/employees/", response_model=EmployeeRetrieve)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# Read employees
@router.get("/employees/", response_model=List[EmployeeRetrieve])
def read_employees(skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db)):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees


# Read a single employee by ID
@router.get("/employees/{employee_id}", response_model=EmployeeRetrieve)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


# Update an employee
@router.put("/employees/{employee_id}", response_model=EmployeeRetrieve)
def update_employee(employee_id: int, employee: EmployeeUpdate,
                    db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in employee:
        setattr(db_employee, field, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# Delete an employee
@router.delete("/employees/{employee_id}", response_model=EmployeeRetrieve)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return db_employee
