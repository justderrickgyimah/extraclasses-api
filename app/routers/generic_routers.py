from fastapi import APIRouter, HTTPException
from typing import List, Type, Any, Dict
from pydantic import BaseModel


class GenericRouter:
    def __init__(self, db: Type[Any], model: Type[BaseModel]):
        self.router = APIRouter()
        self.db = db()
        self.model = model
        
    