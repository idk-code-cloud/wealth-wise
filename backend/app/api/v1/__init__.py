from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(users_router)
