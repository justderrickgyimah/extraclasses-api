from app.models.user_model import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService
from app.routers.rest_routers import GenericCRUDRouter
from fastapi import APIRouter


router = APIRouter()
service = UserService()

user_router = GenericCRUDRouter[UserCreate, UserRead, UserUpdate, UserService, UserCreate, UserRead](router, service, UserCreate, UserRead)