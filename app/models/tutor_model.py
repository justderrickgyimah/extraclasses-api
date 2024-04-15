from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4

# tutor profile
class TutorProfileBase(BaseModel):
    first_name: str
    last_name: str
    profile_picture: str
    bio: str
    experience_years: int
    ratings_average: float
    total_reviews: int
    hourly_rate: float
    teaching_style: str
    verification_status: bool
    active_status: bool
    
    
class TutorProfileCreate(TutorProfileBase):
    pass

class TutorProfileRead(TutorProfileBase):
    tutor_profile_id: str = str(uuid4())

class TutorProfileUpdate(BaseModel):
    profile_picture: str
    bio: str
    experience_years: int
    ratings_average: float
    total_reviews: int
    hourly_rate: float
    teaching_style: str
    verification_status: bool
    active_status: bool
    
    class Config:
        from_attributes = True

# tutor qualification
class TutorQualificationBase(BaseModel):
    qualification: str
    institution: str
    completion_year: date
    verified: bool
    

class TutorQualificationCreate(TutorQualificationBase):
    pass


class TutorQualificationRead(TutorQualificationBase):
    tutor_qualification_id: str = str(uuid4())
    

class TutorQualificationUpdate(BaseModel):
    qualification: str
    institution: str
    completion_year: date
    verified: bool
    
    class Config:
        from_attributes = True


# tutor availability
class TutorAvailabilityBase(BaseModel):
    day: str
    start_time: date
    end_time: date
    
    
class TutorAvailabilityCreate(TutorAvailabilityBase):
    pass


class TutorAvailabilityRead(TutorAvailabilityBase):
    tutor_availability_id: str = str(uuid4())
    
    
class TutorAvailabilityUpdate(BaseModel):
    day: str
    start_time: date
    end_time: date
    
    class Config:
        from_attributes = True
        

# tutor subject
class TutorSubjectBase(BaseModel):
    subject: str
    level: str
    price: float
    

class TutorSubjectCreate(TutorSubjectBase):
    pass


class TutorSubjectRead(TutorSubjectBase):
    tutor_subject_id: str = str(uuid4())
    
    
class TutorSubjectUpdate(BaseModel):
    subject: str
    level: str
    price: float
    
    class Config:
        from_attributes = True