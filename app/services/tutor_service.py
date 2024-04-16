from app.services.crud_service_base import CRUDServiceBase
from app.database.crud import tutor_profile as tutor_profileCRUD
from app.database.crud import tutor_availability as tutor_availabilityCRUD
from app.database.crud import tutor_qualification as tutor_qualificationCRUD
from app.database.crud import tutor_subject as tutor_subjectCRUD
from app.database.crud import tutor_review as tutor_reviewCRUD


class TutorProfileService(CRUDServiceBase):
    def __init__(self):
        super().__init__(tutor_profileCRUD)
        
class TutorAvailabilityService(CRUDServiceBase):
    def __init__(self):
        super().__init__(tutor_availabilityCRUD)
        
class TutorQualificationService(CRUDServiceBase):
    def __init__(self):
        super().__init__(tutor_qualificationCRUD)
        
class TutorSubjectService(CRUDServiceBase):
    def __init__(self):
        super().__init__(tutor_subjectCRUD)
        
class TutorReviewService(CRUDServiceBase):
    def __init__(self):
        super().__init__(tutor_reviewCRUD)
