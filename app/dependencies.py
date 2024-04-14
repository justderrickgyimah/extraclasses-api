"""
Common dependencies
"""

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from fastapi.routing import APIRoute
import copy
from fastapi import APIRouter as FastAPIRouter



class APIRouter(FastAPIRouter):
    def add_api_route(self, path: str, route: APIRoute, **kwargs):
        include = kwargs.pop("include_in_schema", True)
        if path.endswith("/"):
            path = path[:-1]
        route_copy = copy.deepcopy(route)
        route_copy.include_in_schema = False
        super().add_api_route(path + "/", route_copy, include_in_schema=False, **kwargs)
        super().add_api_route(path, route, include_in_schema=include, **kwargs)
        

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        