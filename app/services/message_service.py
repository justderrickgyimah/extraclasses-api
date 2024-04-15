from app.services.crud_service_base import CRUDServiceBase
from app.database.crud import message as messageCRUD


class MessageService(CRUDServiceBase):
    def __init__(self):
        super().__init__(messageCRUD)

