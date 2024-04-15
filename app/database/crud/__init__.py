from app.database.crud.base import CRUDBase

# users
from app.database.schemas.user_schema import User
from app.models.user_model import UserCreate, UserUpdate

# messages
from app.database.schemas.message_schema import Message
from app.models.message_model import MessageCreate, MessageUpdate



user = CRUDBase[User, UserCreate, UserUpdate](User)

message = CRUDBase[Message, MessageCreate, MessageUpdate](Message)