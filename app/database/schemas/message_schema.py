from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database.database import Base
from uuid import uuid4

class Message(Base):
    __tablename__ = 'message'

    message_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    sender_id = Column(String, ForeignKey('user.user_id'))
    receiver_id = Column(String, ForeignKey('user.user_id'))
    message = Column(String)
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    date_sent = Column(DateTime)
    date_read = Column(DateTime, nullable=True)
    
    
    def __repr__(self):
        return f"<Message(message_id={self.message_id}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, message={self.message})>"
