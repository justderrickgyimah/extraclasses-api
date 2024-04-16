from typing import List
from sqlalchemy import Column, String, Date, ForeignKey, Boolean
from app.database.database import Base
from uuid import uuid4
from sqlalchemy.orm import relationship

class TutorProfile(Base):
    __tablename__ = 'tutor_profile'

    tutor_profile_id = Column(String, primary_key=True, default=str(uuid4()))
    user_id = Column(String, ForeignKey('user.user_id'))
    profile_photo = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    display_name = Column(String)
    email = Column(String)
    tutor_title = Column(String)
    average_response_time = Column(String)
    short_bio = Column(String)
    about_me = Column(String)
    tutoring_style = Column(String)
    experience_years = Column(String)
    tutor_availability = relationship("TutorAvailability", back_populates="tutor_profile")
    tutor_qualification = relationship("TutorQualification", back_populates="tutor_profile")
    tutor_subject = relationship("TutorSubject", back_populates="tutor_profile")

    is_active = Column(Boolean, default=True)
    
    
    
# TutorAvailability
class TutorAvailability(Base):
    __tablename__ = 'tutor_availability'

    tutor_availability_id = Column(String, primary_key=True, default=str(uuid4()))
    tutor_profile_id = Column(String, ForeignKey('tutor_profile.tutor_profile_id'))
    day = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    is_active = Column(Boolean, default=True)
    
    tutor_profile = relationship("TutorProfile", back_populates="tutor_availability")
    
    
# TutorQualification
class TutorQualification(Base):
    __tablename__ = 'tutor_qualification'

    tutor_qualification_id = Column(String, primary_key=True, default=str(uuid4()))
    tutor_profile_id = Column(String, ForeignKey('tutor_profile.tutor_profile_id'))
    qualification_institution = Column(String)
    qualification_subject = Column(String)
    qualification_type = Column(String)
    qualification_grade = Column(String)
    
    is_active = Column(Boolean, default=True)
    
    tutor_profile = relationship("TutorProfile", back_populates="tutor_qualification")
    

# TutorSubject
class TutorSubject(Base):
    __tablename__ = 'tutor_subject'

    tutor_subject_id = Column(String, primary_key=True, default=str(uuid4()))
    tutor_profile_id = Column(String, ForeignKey('tutor_profile.tutor_profile_id'))
    subject = Column(String)
    level = Column(String)
    price = Column(String)
    
    is_active = Column(Boolean, default=True)
    
    tutor_profile = relationship("TutorProfile", back_populates="tutor_subject")
    
    
# TutorReview
class TutorReview(Base):
    __tablename__ = 'tutor_review'

    tutor_review_id = Column(String, primary_key=True, default=str(uuid4()))
    tutor_profile_id = Column(String, ForeignKey('tutor_profile.tutor_profile_id'))
    user_id = Column(String, ForeignKey('user.user_id'))
    review = Column(String)
    rating = Column(String)
    
    is_active = Column(Boolean, default=True)
    
    tutor_profile = relationship("TutorProfile", back_populates="tutor_review")
    user = relationship("User", back_populates="tutor_review")
    
