"""
crud_service_base for all common services 
"""

from app.database.crud.base import CRUDBase
from typing import List, Dict, Any
import warnings
from sqlalchemy.orm import Session
from uuid import UUID


class CRUDServiceBase():
    def __init__(self, CRUD: CRUDBase):
        self.CRUD = CRUD
        self._tablename = CRUD.model.__tablename__
        
    def create(self, db: Session, input_object):
        """Create an entity in the database"""
        try:
            return self.CRUD.create(db, input_object)
        except Exception as e:
            warnings.warn(f"Failed to create {self._tablename} in the database")
            raise e
        
    def create_multi(self, db: Session, input_objects: List[Dict[str, Any]]):
        """Create multiple entities in the database"""
        try:
            return self.CRUD.create_multi(db, input_objects)
        except Exception as e:
            warnings.warn(f"Failed to create {self._tablename} in the database")
            raise e
        
    def create_from_dict(self, db: Session, input_dict: Dict[str, Any]):
        """Create an entity in the database from a dictionary"""
        try:
            return self.CRUD.create_from_dict(db, input_dict)
        except Exception as e:
            warnings.warn(f"Failed to create {self._tablename} in the database")
            raise e
        
    def read(self, db: Session, id: UUID):
        """Read an entity from the database"""
        try:
            return self.CRUD.read(db, id)
        except Exception as e:
            warnings.warn(f"Failed to read {self._tablename} from the database")
            raise e
        
    def read_multi(self, db: Session, ids: List[UUID]):
        """Read multiple entities from the database"""
        try:
            return self.CRUD.read_multi(db, ids)
        except Exception as e:
            warnings.warn(f"Failed to read {self._tablename} from the database")
            raise e
        
    def read_all(self, db: Session):
        """Read all entities from the database"""
        try:
            return self.CRUD.read_all(db)
        except Exception as e:
            warnings.warn(f"Failed to read {self._tablename} from the database")
            raise e
        
    def read_all_paginated(self, db: Session, skip: int = 0, limit: int = 100):
        """Read all entities from the database paginated"""
        try:
            return self.CRUD.read_multi(db, skip, limit)
        except Exception as e:
            warnings.warn(f"Failed to read {self._tablename} from the database")
            raise e
        
    def read_by_field(self, db: Session, field: str, value: Any):
        """Read an entity from the database by a field"""
        try:
            return self.CRUD.read_by_field(db, field, value)
        except Exception as e:
            warnings.warn(f"Failed to read {self._tablename} from the database")
            raise e
        
    def update(self, db: Session, id: UUID, input_object):
        """Update an entity in the database"""
        try:
            return self.CRUD.update(db, id, input_object)
        except Exception as e:
            warnings.warn(f"Failed to update {self._tablename} in the database")
            raise e
        
    def update_by_field(self, db: Session, field: str, value: Any, input_object):
        """Update an entity in the database by a field"""
        try:
            return self.CRUD.update_by_field(db, field, value, input_object)
        except Exception as e:
            warnings.warn(f"Failed to update {self._tablename} in the database")
            raise e
        
    def update_multi(self, db: Session, ids: List[UUID], input_objects):
        """Update multiple entities in the database"""
        try:
            return self.CRUD.update_multi(db, ids, input_objects)
        except Exception as e:
            warnings.warn(f"Failed to update {self._tablename} in the database")
            raise e
        
    def delete(self, db: Session, id: UUID):
        """Delete an entity from the database"""
        try:
            return self.CRUD.delete(db, id)
        except Exception as e:
            warnings.warn(f"Failed to delete {self._tablename} from the database")
            raise e
        
    def delete_multi(self, db: Session, ids: List[UUID]):
        """Delete multiple entities from the database"""
        try:
            return self.CRUD.delete_multi(db, ids)
        except Exception as e:
            warnings.warn(f"Failed to delete {self._tablename} from the database")
            raise e
        
    def delete_by_field(self, db: Session, field: str, value: Any):
        """Delete an entity from the database by a field"""
        try:
            return self.CRUD.delete_by_field(db, field, value)
        except Exception as e:
            warnings.warn(f"Failed to delete {self._tablename} from the database")
            raise e
        
    def delete_all(self, db: Session):
        """Delete all entities from the database"""
        try:
            return self.CRUD.delete_all(db)
        except Exception as e:
            warnings.warn(f"Failed to delete {self._tablename} from the database")
            raise e
        
    def search(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        children: bool = False,
        search_string: str = None,
        columns: List[str] = None,
    ):
        """search through a list of columns for the search string using the search function"""

        try:
            records = self.CRUD.search(
                db=db,
                skip=skip,
                limit=limit,
                children=children,
                search_string=search_string,
                columns=columns,
            )
            if not records:
                return []
            return records
        except Exception as e:
            warnings.warn(f"Failed to search {self._tablename} in the database")
            raise e
