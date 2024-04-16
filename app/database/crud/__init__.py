from app.database.crud.base import CRUDBase

# users
from app.database.schemas.user_schema import User
from app.models.user_model import UserCreate, UserUpdate

# messages
from app.database.schemas.message_schema import Message
from app.models.message_model import MessageCreate, MessageUpdate

# tutors
from app.database.schemas.tutor_schema import TutorProfile, TutorAvailability, TutorQualification, TutorSubject, TutorReview
from app.models.tutor_model import TutorProfileCreate, TutorProfileUpdate, TutorAvailabilityCreate, TutorAvailabilityUpdate, TutorQualificationCreate, TutorQualificationUpdate, TutorSubjectCreate, TutorSubjectUpdate, TutorReviewCreate, TutorReviewUpdate


# users
user = CRUDBase[User, UserCreate, UserUpdate](User)

# messages
message = CRUDBase[Message, MessageCreate, MessageUpdate](Message)

# tutor
tutor_profile = CRUDBase[TutorProfile, TutorProfileCreate, TutorProfileUpdate](TutorProfile)
tutor_availability = CRUDBase[TutorAvailability, TutorAvailabilityCreate, TutorAvailabilityUpdate](TutorAvailability)
tutor_qualification = CRUDBase[TutorQualification, TutorQualificationCreate, TutorQualificationUpdate](TutorQualification)
tutor_subject = CRUDBase[TutorSubject, TutorSubjectCreate, TutorSubjectUpdate](TutorSubject)
tutor_review = CRUDBase[TutorReview, TutorReviewCreate, TutorReviewUpdate](TutorReview)
