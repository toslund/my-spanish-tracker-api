from typing import Optional
from datetime import datetime


from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer

    
# Shared properties
class QuestionBase(BaseModel):
    correct: Boolean
    correctness: Integer


# Properties to receive on question creation
class QuestionCreate(QuestionBase):
    deck_uuid: str
    vocab_uuid: str


# Properties to receive on question update
class QuestionUpdate(QuestionBase):
    pass


# Properties shared by models stored in DB
class QuestionInDBBase(QuestionBase):
    id: int
    uuid: str
    deck_uuid: str
    vocab_uuid: str
    date_added: datetime

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