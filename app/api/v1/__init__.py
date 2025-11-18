from fastapi import APIRouter
from app.api.v1 import auth, users, basic, students

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(basic.router, prefix="", tags=["basic"])
