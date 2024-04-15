# routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import UserCreate, UserRead
from app.dependencies import get_db
from app.services.user_service import UserService
from app.database.schemas.user_schema import User
from typing import List


router = APIRouter()
service = UserService(User)


@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return service.create(db, user)


@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: str, db: Session = Depends(get_db)):
    """Read a user by ID"""
    return service.read(db, user_id)


@router.get("/users", response_model=List[UserRead])
def read_all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search_string: str = None,
    columns: str = None,
):
    if columns is not None:
        columns = columns.replace(" ", "").strip().split(",")

    if search_string:
        response_data = service.search(
            db,
            skip=skip,
            limit=limit,
            search_string=search_string,
            columns=columns,
        )
        
    elif search_string is None and skip is not None and limit is not None:
        response_data = service.read_all_paginated(db, skip=skip, limit=limit)
        
    else:
        response_data = service.read_all(db)
        
    return response_data


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    """Update a user by ID"""
    return service.update(db, user_id, user)


@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user by ID"""
    return service.delete(db, user_id)
