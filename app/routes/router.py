from fastapi import APIRouter

from app.api.v1.endpoints.employee import router as employee_router

router = APIRouter()

router.include_router(employee_router, tags=["Employees"])
