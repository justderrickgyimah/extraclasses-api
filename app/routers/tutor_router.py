from app.models.tutor_model import TutorProfileCreate, TutorProfileRead, TutorProfileUpdate, TutorAvailabilityCreate, TutorAvailabilityRead, TutorAvailabilityUpdate, TutorQualificationCreate, TutorQualificationRead, TutorQualificationUpdate, TutorSubjectCreate, TutorSubjectRead, TutorSubjectUpdate, TutorReviewCreate, TutorReviewRead, TutorReviewUpdate
from app.services.tutor_service import TutorProfileService, TutorAvailabilityService, TutorQualificationService, TutorSubjectService, TutorReviewService
from app.routers.rest_routers import GenericCRUDRouter
from fastapi import APIRouter


# tutor_profile
router1 = APIRouter()
tutor_profile_service = TutorProfileService()
tutor_profile_router = GenericCRUDRouter[TutorProfileCreate, TutorProfileRead, TutorProfileUpdate, TutorProfileService, TutorProfileCreate, TutorProfileRead](router1, tutor_profile_service, TutorProfileCreate, TutorProfileRead)


# tutor_availability
router2 = APIRouter()
tutor_availability_service = TutorAvailabilityService()
tutor_availability_router = GenericCRUDRouter[TutorAvailabilityCreate, TutorAvailabilityRead, TutorAvailabilityUpdate, TutorAvailabilityService, TutorAvailabilityCreate, TutorAvailabilityRead](router2, tutor_availability_service, TutorAvailabilityCreate, TutorAvailabilityRead)


# tutor_qualification
router3 = APIRouter()
tutor_qualification_service = TutorQualificationService()
tutor_qualification_router = GenericCRUDRouter[TutorQualificationCreate, TutorQualificationRead, TutorQualificationUpdate, TutorQualificationService, TutorQualificationCreate, TutorQualificationRead](router3, tutor_qualification_service, TutorQualificationCreate, TutorQualificationRead)


# tutor_subject
router4 = APIRouter()
tutor_subject_service = TutorSubjectService()
tutor_subject_router = GenericCRUDRouter[TutorSubjectCreate, TutorSubjectRead, TutorSubjectUpdate, TutorSubjectService, TutorSubjectCreate, TutorSubjectRead](router4, tutor_subject_service, TutorSubjectCreate, TutorSubjectRead)


# tutor_review
router5 = APIRouter()
tutor_review_service = TutorReviewService()
tutor_review_router = GenericCRUDRouter[TutorReviewCreate, TutorReviewRead, TutorReviewUpdate, TutorReviewService, TutorReviewCreate, TutorReviewRead](router5, tutor_review_service, TutorReviewCreate, TutorReviewRead)