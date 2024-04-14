from app.database.schemas.tutor_schema import TutorProfile, TutorQualification, TutorAvailability, TutorSubject
from app.services.crud_service_base import CRUDServiceBase
from app.database.crud import tutor_profile as tutorprofileCRUD
from app.database.crud import tutor_qualification as tutorqualificationCRUD
from app.database.crud import tutor_availability as tutoravailabilityCRUD
from app.database.crud import tutor_subject as tutorsubjectCRUD

class TutorProfileService(CRUDServiceBase):
    def __init__(self, TutorProfile: TutorProfile):
        super().__init__(tutorprofileCRUD)
        self._tablename = tutorprofileCRUD.model.__tablename__


class TutorQualificationService(CRUDServiceBase):
    def __init__(self, TutorQualification: TutorQualification):
        super().__init__(tutorqualificationCRUD)
        self._tablename = tutorqualificationCRUD.model.__tablename__
        

class TutorAvailabilityService(CRUDServiceBase):
    def __init__(self, TutorAvailability: TutorAvailability):
        super().__init__(tutoravailabilityCRUD)
        self._tablename = tutoravailabilityCRUD.model.__tablename__
        
        
class TutorSubjectService(CRUDServiceBase):
    def __init__(self, TutorSubject: TutorSubject):
        super().__init__(tutorsubjectCRUD)
        self._tablename = tutorsubjectCRUD.model.__tablename__