from typing import Optional
from datetime import datetime
from uuid import UUID


from pydantic import BaseModel
    
# Shared properties
class DeckBase(BaseModel):
    pass


# Properties to receive on deck creation
class DeckCreate(DeckBase):
    owner_uuid: Optional[UUID] = None


# Properties to receive on deck update
class DeckUpdate(DeckBase):
    pass


# Properties shared by models stored in DB
class DeckInDBBase(DeckBase):
    id: int
    uuid: UUID
    owner_uuid: Optional[UUID] = None
    date_added: Optional[datetime]

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
