from typing import Optional
from datetime import datetime
from uuid import UUID


from pydantic import BaseModel

    
# Shared properties
class QuestionBase(BaseModel):
    correct: bool
    correctness: int


# Properties to receive on question creation
class QuestionCreate(QuestionBase):
    deck_uuid: UUID
    vocab_uuid: UUID


# Properties to receive on question update
class QuestionUpdate(QuestionBase):
    pass


# Properties shared by models stored in DB
class QuestionInDBBase(QuestionBase):
    id: int
    uuid: UUID
    deck_uuid: UUID
    vocab_uuid: UUID
    date_added: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Question(QuestionInDBBase):
    pass


# Properties properties stored in DB
class QuestionInDB(QuestionInDBBase):
    pass

class QuestionDBDump(QuestionInDBBase):
    pass