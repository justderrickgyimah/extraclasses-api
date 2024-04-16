"""
main.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_router
from app.routers import message_router
from app.routers import tutor_router
from app.dependencies import get_db
from app.database.database import Base, engine


app = FastAPI()

app.include_router(user_router.router, tags=["User"], prefix="/user")
app.include_router(message_router.router, tags=["Message"], prefix="/message")

app.include_router(tutor_router.router1, tags=["Tutor"], prefix="/tutor")
app.include_router(tutor_router.router2, tags=["Tutor Availability"], prefix="/tutor")
app.include_router(tutor_router.router3, tags=["Tutor Qualification"], prefix="/tutor")
app.include_router(tutor_router.router4, tags=["Tutor Subject"], prefix="/tutor")
app.include_router(tutor_router.router5, tags=["Tutor Review"], prefix="/tutor")


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins
)


Base.metadata.create_all(engine)

