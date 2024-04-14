from app.database.crud.base import CRUDBase
from app.database.schemas.user_schema import User
from app.models.user_model import UserCreate, UserUpdate

from app.database.schemas.tutor_schema import (
    TutorProfile,
    TutorAvailability,
    TutorQualification,
    TutorSubject,
)
from app.models.tutor_model import TutorProfileUpdate, TutorProfileCreate
from app.models.tutor_model import (
    TutorQualificationCreate,
    TutorQualificationUpdate,
    TutorAvailabilityCreate,
    TutorAvailabilityUpdate,
    TutorSubjectCreate,
    TutorSubjectUpdate,
)

user = CRUDBase[User, UserCreate, UserUpdate](User)

tutor_profile = CRUDBase[TutorProfile, TutorProfileCreate, TutorProfileUpdate](
    TutorProfile
)

tutor_qualification = CRUDBase[
    TutorQualification, TutorQualificationCreate, TutorQualificationUpdate
](TutorQualification)

tutor_availability = CRUDBase[
    TutorAvailability, TutorAvailabilityCreate, TutorAvailabilityUpdate
](TutorAvailability)

tutor_subject = CRUDBase[TutorSubject, TutorSubjectCreate, TutorSubjectUpdate](
    TutorSubject
)
