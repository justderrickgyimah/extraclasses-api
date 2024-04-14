from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.tutor_model import (
    TutorProfileCreate,
    TutorProfileRead,
    TutorProfileUpdate,
    TutorQualificationCreate,
    TutorQualificationRead,
    TutorQualificationUpdate,
    TutorAvailabilityCreate,
    TutorAvailabilityRead,
    TutorAvailabilityUpdate,
    TutorSubjectCreate,
    TutorSubjectRead,
    TutorSubjectUpdate,
)
from app.dependencies import get_db
from app.services.tutor_service import TutorProfileService, TutorQualificationService, TutorAvailabilityService, TutorSubjectService
from app.database.schemas.tutor_schema import (
    TutorProfile,
    TutorQualification,
    TutorAvailability,
    TutorSubject,
)


router = APIRouter()
profile_service = TutorProfileService(TutorProfile)
qualification_service = TutorQualificationService(TutorQualification)
availability_service = TutorAvailabilityService(TutorAvailability)
subject_service = TutorSubjectService(TutorSubject)


@router.post("/tutors", response_model=TutorProfileRead)
def create_tutor_profile(tutor: TutorProfileCreate, db: Session = Depends(get_db)):
    """Create a new tutor profile"""
    return profile_service.create(db, tutor)


@router.get("/tutors/{tutor_id}", response_model=TutorProfileRead)
def read_tutor_profile(tutor_id: str, db: Session = Depends(get_db)):
    """Read a tutor profile by ID"""
    return profile_service.read(db, tutor_id)


@router.get("/tutors", response_model=list[TutorProfileRead])
def read_all_tutors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search_string: str = None,
    columns: str = None,
):
    if columns is not None:
        columns = columns.replace(" ", "").strip().split(",")

    if search_string:
        response_data = profile_service.search(
            db,
            skip=skip,
            limit=limit,
            search_string=search_string,
            columns=columns,
        )
        
    elif search_string is None and skip is not None and limit is not None:
        response_data = profile_service.read_all_paginated(db, skip=skip, limit=limit)
        
    else:
        response_data = profile_service.read_all(db)
        
    return response_data


@router.put("/tutors/{tutor_id}", response_model=TutorProfileRead)
def update_tutor_profile(tutor_id: str, tutor: TutorProfileUpdate, db: Session = Depends(get_db)):
    """Update a tutor profile by ID"""
    return profile_service.update(db, tutor_id, tutor)


@router.delete("/tutors/{tutor_id}")
def delete_tutor_profile(tutor_id: str, db: Session = Depends(get_db)):
    """Delete a tutor profile by ID"""
    return profile_service.delete(db, tutor_id)


@router.post("/tutors/{tutor_id}/qualifications", response_model=TutorQualificationRead)
def create_tutor_qualification(tutor_id: str, qualification: TutorQualificationCreate, db: Session = Depends(get_db)):
    """Create a new tutor qualification"""
    return qualification_service.create(db, qualification, tutor_id)


@router.get("/tutors/{tutor_id}/qualifications/{qualification_id}", response_model=TutorQualificationRead)
def read_tutor_qualification(tutor_id: str, qualification_id: str, db: Session = Depends(get_db)):
    """Read a tutor qualification by ID"""
    return qualification_service.read(db, qualification_id)


@router.get("/tutors/{tutor_id}/qualifications", response_model=list[TutorQualificationRead])
def read_all_tutor_qualifications(tutor_id: str, db: Session = Depends(get_db)):
    """Read all tutor qualifications"""
    return qualification_service.read_all(db, tutor_id)


@router.put("/tutors/{tutor_id}/qualifications/{qualification_id}", response_model=TutorQualificationRead)
def update_tutor_qualification(tutor_id: str, qualification_id: str, qualification: TutorQualificationUpdate, db: Session = Depends(get_db)):
    """Update a tutor qualification by ID"""
    return qualification_service.update(db, qualification_id, qualification)


@router.delete("/tutors/{tutor_id}/qualifications/{qualification_id}")
def delete_tutor_qualification(tutor_id: str, qualification_id: str, db: Session = Depends(get_db)):
    """Delete a tutor qualification by ID"""
    return qualification_service.delete(db, qualification_id)


@router.post("/tutors/{tutor_id}/availability", response_model=TutorAvailabilityRead)
def create_tutor_availability(tutor_id: str, availability: TutorAvailabilityCreate, db: Session = Depends(get_db)):
    """Create a new tutor availability"""
    return availability_service.create(db, availability, tutor_id)


@router.get("/tutors/{tutor_id}/availability/{availability_id}", response_model=TutorAvailabilityRead)
def read_tutor_availability(tutor_id: str, availability_id: str, db: Session = Depends(get_db)):
    """Read a tutor availability by ID"""
    return availability_service.read(db, availability_id)


@router.get("/tutors/{tutor_id}/availability", response_model=list[TutorAvailabilityRead])
def read_all_tutor_availability(tutor_id: str, db: Session = Depends(get_db)):
    """Read all tutor availability"""
    return availability_service.read_all(db, tutor_id)


@router.put("/tutors/{tutor_id}/availability/{availability_id}", response_model=TutorAvailabilityRead)
def update_tutor_availability(tutor_id: str, availability_id: str, availability: TutorAvailabilityUpdate, db: Session = Depends(get_db)):
    """Update a tutor availability by ID"""
    return availability_service.update(db, availability_id, availability)


@router.delete("/tutors/{tutor_id}/availability/{availability_id}")
def delete_tutor_availability(tutor_id: str, availability_id: str, db: Session = Depends(get_db)):
    """Delete a tutor availability by ID"""
    return availability_service.delete(db, availability_id)


@router.post("/tutors/{tutor_id}/subjects", response_model=TutorSubjectRead)
def create_tutor_subject(tutor_id: str, subject: TutorSubjectCreate, db: Session = Depends(get_db)):
    """Create a new tutor subject"""
    return subject_service.create(db, subject, tutor_id)


@router.get("/tutors/{tutor_id}/subjects/{subject_id}", response_model=TutorSubjectRead)
def read_tutor_subject(tutor_id: str, subject_id: str, db: Session = Depends(get_db)):
    """Read a tutor subject by ID"""
    return subject_service.read(db, subject_id)


@router.get("/tutors/{tutor_id}/subjects", response_model=list[TutorSubjectRead])
def read_all_tutor_subjects(tutor_id: str, db: Session = Depends(get_db)):
    """Read all tutor subjects"""
    return subject_service.read_all(db, tutor_id)


@router.put("/tutors/{tutor_id}/subjects/{subject_id}", response_model=TutorSubjectRead)
def update_tutor_subject(tutor_id: str, subject_id: str, subject: TutorSubjectUpdate, db: Session = Depends(get_db)):
    """Update a tutor subject by ID"""
    return subject_service.update(db, subject_id, subject)


@router.delete("/tutors/{tutor_id}/subjects/{subject_id}")
def delete_tutor_subject(tutor_id: str, subject_id: str, db: Session = Depends(get_db)):
    """Delete a tutor subject by ID"""
    return subject_service.delete(db, subject_id)