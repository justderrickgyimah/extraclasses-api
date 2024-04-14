from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4
from app.utils.enums.enums import RoleEnum

class UserBase(BaseModel):
    username: str
    last_name: str
    first_name: str
    profile_picture: str
    email: str
    phone_number: str
    DOB: date
    role: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    user_id: str = str(uuid4())

class UserUpdate(BaseModel):
    profile_picture: str | None = None
    phone_number: str | None = None
    DOB: date | None = None
    role: str | None = None

    class Config:
        from_attributes = True
