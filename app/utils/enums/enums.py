from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TUTOR = "tutor"
    PARENT = "parent"
    
