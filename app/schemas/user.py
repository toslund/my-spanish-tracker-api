from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, EmailStr
from uuid import UUID
from .deck import Deck


# Shared properties
class UserBase(BaseModel):
    uuid: UUID
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    uuid: UUID
    hashed_password: str
    date_added: Optional[datetime]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserBase):
    uuid: UUID
    decks: List[Deck]

    class Config:
        orm_mode = True


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

class UserDBDump(UserBase):
    uuid: UUID
    hashed_password: str
    date_added: Optional[datetime]

    class Config:
        orm_mode = True