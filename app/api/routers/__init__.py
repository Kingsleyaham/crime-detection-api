from fastapi import APIRouter

from app.api.routers import auth, users, shifts, violence_detection

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(shifts.router, prefix="/shifts", tags=["Shifts"])
router.include_router(violence_detection.router, prefix="/detect", tags=['Violence'])