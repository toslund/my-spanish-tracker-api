from typing import Optional
from datetime import datetime


from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime

    
# Shared properties
class DeckBase(BaseModel):
    pass


# Properties to receive on deck creation
class DeckCreate(DeckBase):
    owner_uuid: Optional[str] = None


# Properties to receive on deck update
class DeckUpdate(DeckBase):
    pass


# Properties shared by models stored in DB
class DeckInDBBase(DeckBase):
    id: int
    uuid: str
    owner_uuid: Optional[str] = None
    date_added: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Deck(DeckInDBBase):
    pass


# Properties properties stored in DB
class DeckInDB(DeckInDBBase):
    pass

class DeckDBDump(DeckInDBBase):
    pass
