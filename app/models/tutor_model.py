from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4


class TutorProfileBase(BaseModel):
    tutor_profile_id: str
    user_id: str
    profile_photo: str
    first_name: str
    last_name: str
    display_name: str
    email: str
    tutor_title: str
    average_response_time: str
    short_bio: str
    about_me: str
    tutoring_style: str
    experience_years: str
    
    
class TutorProfileCreate(TutorProfileBase):
    pass


class TutorProfileRead(TutorProfileBase):
    tutor_profile_id: str = str(uuid4())
    

class TutorProfileUpdate(BaseModel):
    profile_photo: str
    first_name: str
    last_name: str
    display_name: str
    email: str
    tutor_title: str
    average_response_time: str
    short_bio: str
    about_me: str
    tutoring_style: str
    experience_years: str

    class Config:
        from_attributes = True
        
        
# TutorAvailability
class TutorAvailabilityBase(BaseModel):
    tutor_availability_id: str
    tutor_profile_id: str
    day: str
    start_time: str
    end_time: str
    

class TutorAvailabilityCreate(TutorAvailabilityBase):
    pass


class TutorAvailabilityRead(TutorAvailabilityBase):
    tutor_availability_id: str = str(uuid4())
    

class TutorAvailabilityUpdate(BaseModel):
    day: str
    start_time: str
    end_time: str

    class Config:
        from_attributes = True
        


# TutorQualification
class TutorQualificationBase(BaseModel):
    tutor_qualification_id: str
    tutor_profile_id: str
    qualification_insitution: str
    qualification_subject: str
    qualification_type: str
    qualification_grade: str
    
    
class TutorQualificationCreate(TutorQualificationBase):
    pass


class TutorQualificationRead(TutorQualificationBase):
    tutor_qualification_id: str = str(uuid4())
    
    
class TutorQualificationUpdate(BaseModel):
    qualification_insitution: str
    qualification_subject: str
    qualification_type: str
    qualification_grade: str

    class Config:
        from_attributes = True
        
        
        
# TutorSubject
class TutorSubjectBase(BaseModel):
    tutor_subject_id: str
    tutor_profile_id: str
    subject: str
    level: str
    price: str
    
    
class TutorSubjectCreate(TutorSubjectBase):
    pass


class TutorSubjectRead(TutorSubjectBase):
    tutor_subject_id: str = str(uuid4())
    
    
class TutorSubjectUpdate(BaseModel):
    subject: str
    level: str
    price: str

    class Config:
        from_attributes = True



    
# TutorReview
class TutorReviewBase(BaseModel):
    tutor_review_id: str
    tutor_profile_id: str
    user_id: str
    review: str
    rating: str


class TutorReviewCreate(TutorReviewBase):
    pass


class TutorReviewRead(TutorReviewBase):
    tutor_review_id: str = str(uuid4())
    
    
class TutorReviewUpdate(BaseModel):
    review: str
    rating: str

    class Config:
        from_attributes = True