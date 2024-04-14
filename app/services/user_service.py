from app.database.schemas.user_schema import User
from app.services.crud_service_base import CRUDServiceBase
from app.database.crud import user as userCRUD




class UserService(CRUDServiceBase):
    def __init__(self, User: User):
        super().__init__(userCRUD)
        self._tablename = userCRUD.model.__tablename__
   