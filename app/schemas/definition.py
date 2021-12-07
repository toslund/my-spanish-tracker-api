from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Shared properties
class DefinitionBase(BaseModel):
    definition: str
    note: str
    rank: Optional[int] = 9999999
    region: Optional[str] = None
    vocab_uuid: Optional[int] = None
            

# Properties to receive on item creation
class DefinitionCreate(DefinitionBase):
    pass


# Properties to receive on item update
# class DefinitionUpdate(ItemBase):
#     pass


# Properties shared by models stored in DB
class DefinitionInDBBase(DefinitionBase):
    id: int
    uuid: str
    date_added: datetime
    vocab_uuid: Optional[str] = None
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
    uuid: str
    date_added: datetime
    date_deprecated: Optional[datetime]
    vocab_uuid: Optional[str] = None

    class Config:
        orm_mode = True