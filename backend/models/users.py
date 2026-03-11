from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field

from models.base import BaseModel


class UserType(str, Enum):
    ADMIN = "ADMIN"
    NURSE = "NURSE"
    DOCTOR = "DOCTOR"
    DENTIST = "DENTIST"

class User(BaseModel, table=True):
    user_id: str = Field(unique=True, index=True, max_length=20)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True, max_length=100)
    password: str = Field(max_length=255)
    user_type: UserType = Field(default=UserType.NURSE)
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = Field(default=None)
