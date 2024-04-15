from app.services.crud_service_base import CRUDServiceBase
from app.database.crud import user as userCRUD


class UserService(CRUDServiceBase):
    def __init__(self):
        super().__init__(userCRUD)