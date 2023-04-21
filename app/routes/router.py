from fastapi import APIRouter

from app.api.v1.endpoints.person import router as person_router

router = APIRouter()

router.include_router(person_router, tags=["Persons"])
