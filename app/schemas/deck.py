from typing import Optional, List, Union
from datetime import datetime
from uuid import UUID


from pydantic import BaseModel
from pydantic.networks import EmailStr

from .question import Question
from .user import User
    
# Shared properties
class DeckBase(BaseModel):
    uuid: UUID    

# Shared properties
class DeckSimplified(DeckBase):

    class Config:
        orm_mode = True


# Properties to receive on deck creation
class DeckCreate(DeckBase):
    owner_uuid: Union[UUID, None]
    # HONEYPOT
    name: str
    email: Optional[str]



# Properties to receive on deck update
class DeckUpdate(DeckBase):
    pass


# Properties shared by models stored in DB
class DeckInDBBase(DeckBase):
    id: int
    owner_uuid: Optional[UUID] = None
    date_added: Optional[datetime]

# Properties to return to client
class Deck(DeckBase):
    questions: List[Question]
    predictions: Optional[List[dict]]
    assessment_bins: Optional[List[dict]]
    owner_uuid: Optional[UUID]
    owner: Optional[User]
    date_added: Optional[datetime]

    class Config:
        orm_mode = True


# Properties properties stored in DB
class DeckInDB(DeckInDBBase):
    pass

class DeckDBDump(DeckBase):
    owner_uuid: Union[UUID, None]
    date_added: Optional[datetime]
    
    class Config:
        orm_mode = True
