from fastapi import APIRouter

from app.api.v1.endpoints.person import router as person_router
from app.api.v1.endpoints.auth import router as user_router
from app.api.v1.endpoints.file_upload import router as file_router
from app.api.v1.endpoints.aws_file_upload import router as aws_file_upload_router

router = APIRouter()

router.include_router(person_router, tags=["Persons"])
router.include_router(user_router, tags=["users"])
router.include_router(file_router, tags=["Files"])
router.include_router(aws_file_upload_router, tags=["AWS File Upload"])
