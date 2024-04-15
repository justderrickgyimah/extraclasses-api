from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models.user_model import UserRead
from uuid import uuid4

class MessageBase(BaseModel):
    sender_id: str
    receiver_id: str
    message: str
    date_sent: datetime
    date_read: Optional[datetime]

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    message_id: str
    sender: UserRead
    receiver: UserRead

class MessageUpdate(BaseModel):
    message: str
    date_read: Optional[datetime]
    
    class Config:
        from_attributes = True