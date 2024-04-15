from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Type, List, Generic, TypeVar
import re

from app.dependencies import get_db

TCreateModel = TypeVar("TCreateModel")
TReadModel = TypeVar("TReadModel")
TUpdateModel = TypeVar("TUpdateModel")
TService = TypeVar("TService")
TInputModel = TypeVar("TInputModel")
TOutputModel = TypeVar("TOutputModel")

def snake_case(name: str) -> str:
    # Convert CamelCase to snake_case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class GenericCRUDRouter(Generic[TCreateModel, TReadModel, TUpdateModel, TService, TInputModel, TOutputModel]):
    def __init__(
        self,
        router: APIRouter,
        service: Type[TService],
        input_model: Type[TInputModel],
        output_model: Type[TOutputModel],
    ):
        self.router = router
        self.service = service
        self.input_model = input_model
        self.output_model = output_model

        self._add_routes()

    
    def _add_routes(self):
        endpoint_name = snake_case(self.input_model.__name__)

        @self.router.post(f"/{endpoint_name}", response_model=self.output_model)
        def create(input_object: self.input_model, db: Session = Depends(get_db)):
            """Create a new item"""
            return self.service.create(db, input_object)

        


