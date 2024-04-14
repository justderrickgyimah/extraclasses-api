from sqlalchemy import Column, String, Date, ForeignKey, CheckConstraint, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database.database import Base
from typing import List
from sqlalchemy.orm import relationship



class TutorProfile(Base):
    __tablename__ = 'tutor_profile'

    tutor_profile_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('user.user_id'))
    first_name = Column(String)
    last_name = Column(String)
    profile_picture = Column(String)
    bio = Column(String)
    experience_years = Column(Integer)
    ratings_average = Column(Float)
    total_reviews = Column(Integer)
    hourly_rate = Column(Float)
    teaching_style = Column(String)
    verification_status = Column(Boolean)
    active_status = Column(Boolean)

    user = relationship("User", back_populates="tutor_profile")
    qualification = relationship("TutorQualification", back_populates="tutor_profile")
    availability = relationship("TutorAvailability", back_populates="tutor_profile")
    subject = relationship("TutorSubject", back_populates="tutor_profile")
    
    
class TutorQualification(Base):
    __tablename__ = 'tutor_qualification'

    tutor_qualification_id = Column(String, primary_key=True)
    tutor_profile_id = Column(String, ForeignKey('tutor_profile.tutor_profile_id'))
    qualification = Column(String)
    institution = Column(String)
    completion_year = Column(Date)
    verified = Column(Boolean)

    tutor_profile = relationship("TutorProfile", back_populates="tutor_qualification")
    
    
class TutorAvailability(Base):
    __tablename__ = 'tutor_availability'

    tutor_availability_id = Column(String, primary_key=True)
    tutor_profile_id = Column(String, ForeignKey('tutor_profile.tutor_profile_id'))
    day = Column(String)
    start_time = Column(Date)
    end_time = Column(Date)

    tutor_profile = relationship("TutorProfile", back_populates="tutor_availability")
    
    
class TutorSubject(Base):
    __tablename__ = 'tutor_subject'

    tutor_subject_id = Column(String, primary_key=True)
    tutor_profile_id = Column(String, ForeignKey('tutor_profile.tutor_profile_id'))
    subject = Column(String)
    level = Column(String)
    price = Column(Float)
    

    tutor_profile = relationship("TutorProfile", back_populates="tutor_subject")