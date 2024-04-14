from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel
from app.database.database import Base
from sqlalchemy.orm import Session, class_mapper, noload
from sqlalchemy.orm.dynamic import AppenderQuery
from sqlalchemy.orm.session import make_transient
from sqlalchemy import inspect, or_
import warnings


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)



def get_most_recent_timestamp(
    model_instance: Any,
    most_recent: datetime = datetime(2000, 1, 1),
    visited: set = None,
) -> datetime:
    """
    Recursively finds the most recent timestamp from a given model instance and its related objects.

    Args:
        model_instance (Any): The model instance to start the search from.
        most_recent (datetime, optional): The current most recent timestamp. Defaults to datetime(2000, 1, 1).
        visited (set, optional): A set to keep track of visited model instances to avoid infinite recursion. Defaults to None.

    Returns:
        datetime: The most recent timestamp found.
    """
    if visited is None:
        visited = set()
    if id(model_instance) in visited:
        return most_recent
    visited.add(id(model_instance))
    if model_instance.__class__ == AppenderQuery:
        return most_recent
    mapper = class_mapper(model_instance.__class__)
    for prop in mapper.iterate_properties:
        if hasattr(prop, "columns"):
            for column in prop.columns:
                if column.name == "updated_on":
                    updated_on = getattr(model_instance, prop.key)
                    if updated_on is not None:
                        most_recent = max(most_recent, updated_on)
        else:
            value = getattr(model_instance, prop.key)
            if value is not None:
                if isinstance(value, list):
                    for item in value:
                        most_recent = get_most_recent_timestamp(
                            item, most_recent, visited
                        )
                else:
                    most_recent = get_most_recent_timestamp(value, most_recent, visited)
    return most_recent


def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"


def pydantic_to_sqlalchemy_model(schema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = dict(schema)
    for key, value in parsed_schema.items():
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                parsed_schema[key] = [
                    item.Meta.orm_model(**pydantic_to_sqlalchemy_model(item))
                    for item in value
                ]
            elif is_pydantic(value):
                parsed_schema[key] = value.Meta.orm_model(
                    **pydantic_to_sqlalchemy_model(value)
                )
        except AttributeError as e:
            print(e)
            raise AttributeError(
                f"Found nested Pydantic model in {schema.__class__} under {key} but Meta.orm_model was not specified."
            )
    return parsed_schema


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD object that allows database operations.

    This class provides basic CRUD (Create, Read, Update, Delete) functionality for interacting with a database.
    It is designed to be inherited by specific CRUD classes for different database models.

    Args:
        ModelType (Type): The type of the database model.
        CreateSchemaType (Type): The type of the schema used for creating new objects.
        UpdateSchemaType (Type): The type of the schema used for updating existing objects.

    Attributes:
        model (Type[ModelType]): The database model associated with this CRUD object.

    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, input_object: CreateSchemaType) -> ModelType:
        """
        Basic insertion (can also handle parents with children nested inside as per pydantic model)

        params:
            - input_object: an object conforming to the pydantic model defined by CreateSchemaType
        """
        db_object = self.model(**pydantic_to_sqlalchemy_model(input_object))
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    def bulk_create(
        self, db: Session, input_objects: List[CreateSchemaType]
    ) -> List[ModelType]:
        """
        Basic insertion (can also handle parents with children nested inside as per pydantic model)

        params:
            - input_object: an object conforming to the pydantic model defined by CreateSchemaType
        """
        db_objects = [
            self.model(**pydantic_to_sqlalchemy_model(input_object))
            for input_object in input_objects
        ]
        # add the primary key to the objects (if not already present)
        for db_object in db_objects:
            if self.model.__tablename__ + "_id" not in db_object.__dict__.keys():
                db_object.__dict__[self.model.__tablename__ + "_id"] = uuid4()
        db.add_all(db_objects)
        db.commit()
        [db.refresh(db_object) for db_object in db_objects]
        return db_objects

    def create_by_parent_id(
        self,
        db: Session,
        parent_id: UUID,
        parent_table: str,
        input_object: CreateSchemaType,
    ) -> ModelType:
        """
        Basic insertion with a provided foreign key (can also handle parents with children nested inside as per pydantic model)

        params:
            - input_object: an object conforming to the pydantic model defined by CreateSchemaType
        """
        db_object = self.model(**pydantic_to_sqlalchemy_model(input_object))
        db_object.__dict__[parent_table + "_id"] = parent_id
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    def bulk_create_by_parent_id(
        self,
        db: Session,
        parent_id: UUID,
        parent_table: str,
        input_objects: List[CreateSchemaType],
    ) -> List[ModelType]:
        """
        Basic insertion with a provided foreign key (can also handle parents with children nested inside as per pydantic model)

        params:
            - input_object: an object conforming to the pydantic model defined by CreateSchemaType
        """
        db_objects = [
            self.model(**pydantic_to_sqlalchemy_model(input_object))
            for input_object in input_objects
        ]
        # add the primary key to the objects (if not already present)
        for db_object in db_objects:
            if self.model.__tablename__ + "_id" not in db_object.__dict__.keys():
                db_object.__dict__[self.model.__tablename__ + "_id"] = uuid4()
            db_object.__dict__[parent_table + "_id"] = parent_id
        db.add_all(db_objects)
        db.commit()

        [db.refresh(db_object) for db_object in db_objects]
        return db_objects

    def read(
        self,
        db: Session,
        id: UUID,
        children: bool = False,
        is_active: bool = True,
    ) -> Optional[ModelType]:
        """
        Standard read by primary key (id)

        params:
            - id: the UUID corresponding to the primary key field of the table
            - children (False): optionally return child entities of the read object
            - is_active (True): if True, return only data with is_active == True
        """
        # TODO: include date validity logic (query from history if data not present?)

        query = db.query(self.model)

        if not children:
            query = query.options(noload("*"))

        # if upddated_on column is present then sort by this column in descending order
        if "updated_on" in self.model.__dict__.keys():
            query = query.order_by(self.model.__dict__["updated_on"].desc())

        # if is_active column is present then make sure we only select active data
        if "is_active" in self.model.__dict__.keys() and is_active:
            query = query.filter(self.model.__dict__["is_active"])

        query = query.filter(
            self.model.__dict__[self.model.__tablename__ + "_id"] == id
        )
        return query.first()

    def read_versions(self, db: Session, id: UUID) -> List[ModelType]:
        """
        read all the versions of an entry with a given primary key
        """

        head = self.read(db, id, is_active=False)
        if head is None:
            return []
        versions = head.versions
        return [version.version_parent for version in versions.all()]

    def count_versions(self, db: Session, id: UUID) -> int:
        """
        count the number of versions of an entry with a given primary key
        """

        versions = self.read(db, id, is_active=False).versions.count()
        return versions

    def read_by_filter(
        self, db: Session, filter: Dict, children: bool = False, is_active: bool = True
    ) -> List[ModelType]:
        """
        Reads a record by a given filter.

        Args:
            db (Session): The database session.
            filter (Dict): A dictionary where the key is the column name and the value is the value or list of values to filter on.
            children (bool, optional): Whether to return child objects of the selected entities. Defaults to False.
            is_active (bool, optional): Whether to filter by the 'is_active' column. Defaults to True.

        Returns:
            List[ModelType]: The selected record(s) or None if no records match the filter.
        """
        query = db.query(self.model)

        if not children:
            query = query.options(noload("*"))

        if "is_active" in self.model.__dict__.keys() and is_active:
            query = query.filter(self.model.__dict__["is_active"])

        for key, value in filter.items():
            if type(value) is list:
                query = query.filter(self.model.__dict__[key].in_(value))
            else:
                query = query.filter(self.model.__dict__[key] == value)

        if "updated_on" in self.model.__dict__.keys():
            query = query.order_by(self.model.__dict__["updated_on"].desc())

        return query.all()

    def read_all(
        self, db: Session, children: bool = False, is_active: bool = True
    ) -> List[ModelType]:
        """
        Read all records in a given table.

        Args:
            db (Session): The database session.
            children (bool, optional): Optionally return child entities of the read data. Defaults to False.
            is_active (bool, optional): Filter records based on their active status. Defaults to True.

        Returns:
            List[ModelType]: A list of all records in the table.
        """
        # TODO: include date validity logic (query from history if data not present?)

        query = db.query(self.model)

        if children is False:
            query = query.options(noload("*"))

        if "is_active" in self.model.__dict__.keys() and is_active:
            query = query.filter(self.model.is_active)

        if "updated_on" in self.model.__dict__.keys():
            query = query.order_by(self.model.__dict__["updated_on"].desc())

        return query.all()  # .all()

    def read_all_by_parent_id(
        self,
        db: Session,
        parent_id: UUID,
        parent_table: str,
        children: bool = False,
        is_active: bool = True,
    ):
        """
        Read all records by a foreign key given by parent_id and parent_table.

        Args:
            db (Session): The database session.
            parent_id (UUID): The value of the foreign key.
            parent_table (str): The name of the table to which the foreign key refers.
            children (bool, optional): Optionally return child entities of the selected data. Defaults to False.
            is_active (bool, optional): Filter records based on their active status. Defaults to True.

        Returns:
            List[ModelType]: A list of model instances.

        Example:
            read_all_by_parent_id(db, parent_id=1, parent_table="parent_table", children=True)
        """

        query = db.query(self.model)

        if not children:
            query = query.options(noload("*"))

        query = query.filter(self.model.__dict__[parent_table + "_id"] == parent_id)

        if is_active and "is_active" in self.model.__dict__.keys():
            query = query.filter(self.model.__dict__["is_active"])

        if "updated_on" in self.model.__dict__.keys():
            query = query.order_by(self.model.__dict__["updated_on"].desc())

        return query.all()

    def read_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        children: bool = False,
        is_active: bool = True,
    ) -> List[ModelType]:
        """
        Read paginated records from a table ordered by primary key.

        Args:
            db (Session): The database session.
            skip (int, optional): Number of records to skip initially. Defaults to 0.
            limit (int, optional): The maximum number of records to return. Defaults to 100.
            children (bool, optional): Optionally return child entities of the selected data. Defaults to False.

        Returns:
            List[ModelType]: A list of model instances.

        Todo:
            - Include date validity logic (query from history if data not present?)

        Example:
            read_multi(db, skip=10, limit=20, children=True)
        """

        query = db.query(self.model)

        if children is False:
            query = query.options(noload("*"))

        if is_active and "is_active" in self.model.__dict__.keys():
            query = query.filter(self.model.__dict__["is_active"])

        if "updated_on" in self.model.__dict__.keys():
            query = query.order_by(
                self.model.__dict__["updated_on"],
            )

        query = query.offset(skip).limit(limit)

        return query.all()

    def search(
        self,
        db: Session,
        search_string: str = None,
        columns: List[str] = None,
        children: bool = False,
        is_active: bool = True,
        limit: int = 100,
        skip: int = 0,
    ):
        """
        Search for records in a table by a string within a specified list of columns, if no columns are specified, search all columns.

        Args:
            db (Session): The database session.
            search_string (str): The string to search for.
            columns (List[str]): The columns to search in.
            children (bool, optional): Optionally return child entities of the selected data. Defaults to False.
            is_active (bool, optional): Filter records based on their active status. Defaults to True.
            limit (int, optional): The maximum number of records to return. Defaults to 100.
            skip (int, optional): Number of records to skip initially. Defaults to 0.

        Returns:
            List[ModelType]: A list of model instances.

        Example:
            search(db, "search_string", ["column1", "column2"], children=True, limit=100, skip=0)
        """
        query = db.query(self.model)

        if children is None:
            query = query.options(noload("*"))

        if is_active and "is_active" in self.model.__dict__.keys():
            query = query.filter(self.model.__dict__["is_active"])

        # if no columns are specified, search in all columns
        if search_string is not None:
            if columns is None:
                columns_list = self.model.__table__.columns
                search_conditions = [
                    column.ilike(f"%{search_string}%") for column in columns_list
                ]

            # if columns are specified, check if they exist in the table
            elif columns is not None:
                for column in columns:
                    if column not in self.model.__table__.columns:
                        raise ValueError(
                            f"Column {column} not found in table {self.model.__tablename__}"
                        )

                # if columns are specified, search only in those columns
                columns_list = [
                    col for col in columns if col in self.model.__table__.columns
                ]
                search_conditions = [
                    getattr(self.model, column).ilike(f"%{search_string}%")
                    for column in columns_list
                ]

            # apply the search conditions
            query = query.filter(or_(*search_conditions)).order_by(
                self.model.__dict__[self.model.__tablename__ + "_id"]
            )

        results = query.offset(skip).limit(limit).all()
        return results

    def _update_dict_fields(self, db, record, input_object, _insert_child=True):
        """
        Recursively updates the fields in a SQLAlchemy object to match the fields specified in the input dictionary.
        If the object does not exist in the database, it will be inserted (upserted) if _insert_child is True.

        Args:
            db: The database session.
            record: The SQLAlchemy object to be updated.
            input_object: A dictionary of fields to update.
            _insert_child: If True, insert child objects that are not already present.

        Returns:
            The updated SQLAlchemy object.
        """
        # Update fields
        for field, value in input_object.items():
            # If field value is a list, its child attribute
            if hasattr(record, field) and isinstance(value, list):
                # Get the related model class
                related_model_class = getattr(
                    record.__class__, field
                ).property.mapper.class_

                # Fetch the existing collection from the record
                existing_instances = getattr(record, field)
                existing_instances_dict = {
                    getattr(
                        instance, related_model_class.__tablename__ + "_id"
                    ): instance
                    for instance in existing_instances
                }

                # Iterate over the related objects in the input
                for related_object_dict in value:
                    if type(related_object_dict) is not dict:
                        # SQLAlchemy object - coerce to dict
                        related_object_dict = related_object_dict.__dict__
                    try:
                        related_object_id = related_object_dict[
                            related_model_class.__tablename__ + "_id"
                        ]
                        if related_object_id in existing_instances_dict:
                            # The related object exists in the collection, update it
                            related_object_instance = existing_instances_dict[
                                related_object_id
                            ]
                            related_object_instance = self._update_dict_fields(
                                db, related_object_instance, related_object_dict
                            )
                        elif _insert_child:
                            # The related object doesn't exist in the collection, create a new instance
                            related_object_instance = related_model_class(
                                **pydantic_to_sqlalchemy_model(related_object_dict)
                            )
                            existing_instances.append(related_object_instance)
                    except KeyError:
                        # no id, so insert
                        related_object_instance = related_model_class(
                            **pydantic_to_sqlalchemy_model(related_object_dict)
                        )
                        existing_instances.append(related_object_instance)

                # Set the updated collection on the record
                setattr(record, field, existing_instances)
            else:
                setattr(record, field, value)
        return record

    def is_sqlalchemy(self, obj):
        """returns True if an object is a SQLAlchemy model instance"""
        return hasattr(obj, "_sa_instance_state")
    
             
        
    def update_from_db_record(
        self, db: Session, update_dict: dict, last_modified: datetime = None
    ):
        """
        Update a database record from a dict of keys and values to update.
        If update_dict contains a primary key, then the record with that primary key will be updated.
        If update_dict does not contain a primary key, then a new record will be created
        Update_dict can contain nested dicts to update child objects.
        Child records in update_dict are 'upserted' in the same way as the main record.
        If last_modified is provided, then the update will only be performed if the record (or any child records)
        has not been modified since last_modified.

        Args:
            db (Session): The database session.
            update_dict (dict): A dict of fields to update.
            last_modified (datetime, optional): A datetime object specifying the last time the record was modified. Defaults to None.

        Returns:
            ModelType: The updated record.
        """
        try:
            existing = (
                db.query(self.model)
                .filter(
                    self.model.__dict__[self.model.__tablename__ + "_id"]
                    == update_dict[self.model.__tablename__ + "_id"]
                )
                .first()
            )
        except KeyError:
            # no primary key - create a new record
            existing = self.model()
        if last_modified:
            make_transient(existing)
            # get the last modified date of the record and all its children
            most_recent_timestamp = get_most_recent_timestamp(existing)
            # if the most recent timestamp is later than last_modified, then raise an error
            if most_recent_timestamp > last_modified:
                raise ValueError(
                    f"Record {existing} has been modified since {last_modified}. Aborting update."
                )
            # db.merge(existing)
            existing = (
                db.query(self.model)
                .filter(
                    self.model.__dict__[self.model.__tablename__ + "_id"]
                    == update_dict[self.model.__tablename__ + "_id"]
                )
                .first()
            )
        # bring existing up to date
        existing = self._update_dict_fields(db, existing, update_dict)
        # update the record
        _ = self._recursive_merge(db, existing)
        # commit the changes
        db.commit()
        # return the updated record
        return existing

    def bulk_update_from_db_record(
        self, db: Session, update_dicts: List[dict], last_modified: datetime = None
    ):
        """utility function to perform update_from_db_record over a list of updates
        note that 'last_modified' here should be the maximum last_modified of all the records in update_dicts
        if the update contains a change to is_active, then these records are soft deleted with cascade using self.soft_delete

        Args:
            db (Session): The database session.
            update_dicts (List[dict]): A list of dicts of fields to update.
            last_modified (datetime, optional): A datetime object specifying the last time the record was modified. Defaults to None.

        Returns:
            List[ModelType]: The updated records.
        """
        records = []
        for update_dict in update_dicts:
            # check if the update_dict has 'is_active'
            if "is_active" in update_dict:
                if not update_dict["is_active"]:
                    record = self.soft_delete(
                        db,
                        update_dict[self.model.__tablename__ + "_id"],
                        metadata=update_dict,
                    )
                    records.append(record)
                    continue
                else:
                    record = self.update_from_db_record(
                        db, update_dict, last_modified=last_modified
                    )
                    records.append(record)
            else:
                record = self.update_from_db_record(
                    db, update_dict, last_modified=last_modified
                )
                records.append(record)
        return records

    def update_or_insert(
        self,
        db: Session,
        input_object_list: List[UpdateSchemaType],
        last_modified: datetime = None,
    ):
        """
        Update a record selected by primary key or insert if primary key is None.

        Args:
            db (Session): The database session.
            input_object_list (List[UpdateSchemaType]): A list of dict with the fields to be updated.
            last_modified (datetime, optional): A datetime object specifying the last time the record was modified. Defaults to None.

        Returns:
            List[ModelType]: The updated or inserted records.
        """
        warnings.warn(
            "update_or_insert function is deprecated - use bulk_update_from_db_record or update_from_db_record instead",
            FutureWarning,
        )
        db_objects = []
        for input_object in input_object_list:
            if type(input_object) is dict:
                id = input_object[self.model.__tablename__ + "_id"]
            elif is_pydantic(input_object):
                id = input_object.__dict__[self.model.__tablename__ + "_id"]
            else:
                # SQLAlchemy object - coerce to dict
                id = input_object.__dict__[self.model.__tablename__ + "_id"]
            updated = self.update(db, id, input_object, upsert=True)
            db_objects.append(updated)

        return db_objects

    def update(
        self,
        db: Session,
        id,
        input_object: UpdateSchemaType,
        upsert=False,
    ):
        """
        Update a record selected by primary key.

        Args:
            db (Session): The database session.
            id: The primary key of the record to be updated.
            input_object (UpdateSchemaType): A dict with the fields to be updated.
            upsert (bool, optional): If True, insert records with no id (and if id == None or not found). Defaults to False.

        Returns:
            ModelType: The updated record.
        """
        warnings.warn(
            "function update is deprecated - use update_from_db_record instead",
            FutureWarning,
        )
        if id is None and upsert:
            # create record
            if type(input_object) is dict:
                db_object = self.model(**pydantic_to_sqlalchemy_model(input_object))
            elif is_pydantic(input_object):
                db_object = self.model(
                    **pydantic_to_sqlalchemy_model(
                        input_object.model_dump(exclude_unset=True)
                    )
                )
            else:
                # is a sqlaclhemy object already
                db_object = input_object
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            id = db_object.__dict__[self.model.__tablename__ + "_id"]
        else:
            # else Fetch the record
            record = (
                db.query(self.model)
                .filter(self.model.__dict__[self.model.__tablename__ + "_id"] == id)
                .first()
            )

            # If record not found, return None
            if record is None and upsert:
                # create record
                if type(input_object) is dict:
                    db_object = self.model(**pydantic_to_sqlalchemy_model(input_object))
                else:
                    db_object = self.model(
                        **pydantic_to_sqlalchemy_model(
                            input_object.model_dump(exclude_unset=True)
                        )
                    )
                db.add(db_object)
            else:
                if type(input_object) is dict:
                    self._update_dict_fields(
                        db, record, input_object, _insert_child=upsert
                    )
                elif is_pydantic(input_object):
                    self._update_dict_fields(
                        db,
                        record,
                        input_object.model_dump(exclude_unset=True),
                        _insert_child=upsert,
                    )
                else:
                    self._update_dict_fields(
                        db,
                        record,
                        input_object.__dict__,
                        _insert_child=upsert,
                    )
            db.commit()

        # Return updated record
        return (
            db.query(self.model)
            .filter(self.model.__dict__[self.model.__tablename__ + "_id"] == id)
            .first()
        )

    def _get_relationships(self, model):
        """
        Get the names of the relationships in a model.

        Args:
            model: The model to get the relationships from.

        Returns:
            List[str]: The names of the relationships.
        """
        inspector = inspect(model)
        relationships = inspector.relationships.items()
        cascade_relationships = [
            name for name, rel in relationships if "delete" in rel.cascade
        ]
        return cascade_relationships

    def delete(self, db: Session, id: UUID, metadata=None) -> ModelType:
        """
        Soft delete a record by primary key (sets is_active = False).

        Args:
            db (Session): The database session.
            id (UUID): The primary key of the record to soft delete.
            metadata (dict, optional): A dict of metadata to be added to the record along with deletion (e.g. user info). Defaults to None.

        Returns:
            ModelType: The deleted record.

        Notes:
            delete() does not cascade to child records. Use soft_delete_with_cascade() to cascade.
            deprecated: use soft_delete_with_cascade() instead - will be removed in future
        """
        warnings.warn(
            "function delete is deprecated - use soft_delete_with_cascade instead",
            FutureWarning,
        )
        if metadata:
            record = self.update(db, id, metadata.update({"is_active": False}))
        else:
            record = self.update(db, id, {"is_active": False})
        return record

    def recursively_set_inactive(self, record, metadata=None):
        """
        Recursively set is_active = False for all child records (and set metadata if present).

        Args:
            record: The record to set inactive.
            metadata (dict, optional): A dict of metadata to be added to the record along with setting it inactive. Defaults to None.
        """
        cascade_relationships = self._get_relationships(record.__class__)
        for rel_name in cascade_relationships:
            related_records = getattr(record, rel_name)
            for related in related_records:
                if metadata:
                    for key, value in metadata.items():
                        if hasattr(related, key):
                            setattr(related, key, value)
                if hasattr(related, "is_active"):
                    related.is_active = False
                self.recursively_set_inactive(related)

    def soft_delete(
        self, db: Session, id: UUID, metadata: dict = None, cascade: bool = True
    ):
        """
        Soft delete a record by primary key with cascade (sets is_active = False for all child records).
        This is the primary method that should be used to 'delete' records.

        Args:
            db (Session): The database session.
            id (UUID): The primary key of the record to soft delete.
            metadata (dict, optional): A dict of metadata to be added to the record along with deletion (e.g. user info). Defaults to None.
            cascade (bool, optional): Whether to cascade to child records. Defaults to True.

        Returns:
            ModelType: The soft deleted record.
        """
        record = db.query(self.model).get(id)
        if record:
            if metadata:
                for key, value in metadata.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
            if hasattr(record, "is_active"):
                record.is_active = False
            if cascade:
                self.recursively_set_inactive(record, metadata=metadata)
            db.commit()
        return record

    def hard_delete(self, db: Session, id: UUID) -> ModelType:
        """
        Permanently deletes a record by primary key.

        Args:
            db (Session): The database session.
            id (UUID): The primary key of the record to hard delete.

        Returns:
            ModelType: The deleted object.
        """
        object = (
            db.query(self.model)
            .filter(self.model.__dict__[self.model.__tablename__ + "_id"] == id)
            .first()
        )
        db.delete(object)
        db.commit()
        return object
