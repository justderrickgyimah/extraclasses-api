from sqlalchemy import Column, String, Date, ForeignKey, CheckConstraint
from app.database.database import Base
from uuid import uuid4

class User(Base):
    __tablename__ = 'user'

    user_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    role = Column(String, CheckConstraint("role IN ('admin','tutor','student','parent','guest')"))
    username = Column(String,nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    display_name = Column(String)
    profile_picture = Column(String)
    email = Column(String)
    phone_number = Column(String,nullable=True)
    DOB = Column(Date,nullable=True)
    


