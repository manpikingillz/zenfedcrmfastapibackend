from fastapi import APIRouter

from app.api.v1.endpoints.person import router as person_router
from app.api.v1.endpoints.auth import router as user_router

router = APIRouter()

router.include_router(person_router, tags=["Persons"])
router.include_router(user_router, tags=["users"])
