"""
main.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_router, tutor_router
from app.dependencies import get_db
from app.database.database import Base, engine


app = FastAPI()

app.include_router(user_router.router)
app.include_router(tutor_router.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins
)


Base.metadata.create_all(engine)

