from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str
    uuid: UUID


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_uuid: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemBase):
    uuid: UUID
    owner_uuid: UUID

    class Config:
        orm_mode = True


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass

# Properties for db dump
class ItemDBDump(ItemBase):
    uuid: UUID
    owner_uuid: UUID

    class Config:
        orm_mode = True
