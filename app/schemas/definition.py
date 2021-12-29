from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

# Shared properties
class DefinitionBase(BaseModel):
    content: str
    rank: int
    region: Optional[str] = None
    note: Optional[str]

# Shared properties
class DefinitionSimplified(DefinitionBase):

    class Config:
        orm_mode = True

# Properties to receive on item creation
class DefinitionCreate(DefinitionBase):
    vocab_uuid: UUID


# Properties to receive on item update
# class DefinitionUpdate(ItemBase):
#     pass


# Properties shared by models stored in DB
class DefinitionInDBBase(DefinitionBase):
    id: int
    uuid: UUID
    date_added: Optional[datetime]
    vocab_uuid: Optional[UUID] = None
    date_deprecated: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Definition(DefinitionInDBBase):
    pass


# Properties properties stored in DB
class DefinitionInDB(DefinitionInDBBase):
    pass

# Properties for dumping to json
class DefinitionDBDump(DefinitionBase):
    # id: int
    uuid: UUID
    date_added: Optional[datetime]
    date_deprecated: Optional[datetime]
    vocab_uuid: Optional[UUID] = None

    class Config:
        orm_mode = True