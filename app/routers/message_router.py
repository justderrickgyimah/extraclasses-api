from app.models.message_model import MessageCreate, MessageRead, MessageUpdate
from app.services.message_service import MessageService
from app.routers.rest_routers import GenericCRUDRouter
from fastapi import APIRouter


router = APIRouter()
service = MessageService()

message_router = GenericCRUDRouter[MessageCreate, MessageRead, MessageUpdate, MessageService, MessageCreate, MessageRead](router, service, MessageCreate, MessageRead)
