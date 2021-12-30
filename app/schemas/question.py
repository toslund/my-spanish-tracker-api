from typing import Optional, List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .vocab import Vocab, VocabSimplified

    
# Shared properties
class QuestionBase(BaseModel):
    uuid: UUID
    correct: Optional[bool]
    recognize: Optional[bool]
    correctness: Optional[int]
    familiarity: Optional[int]

# Properties to receive on question creation
class QuestionProvisionalCreate(QuestionBase):
    deck_uuid: UUID
    vocab_uuid: UUID
    vocab: Optional[VocabSimplified]
    token: Optional[str]

    class Config:
        orm_mode = True

# Properties to receive on question creation
class QuestionCreate(QuestionBase):
    correct: bool
    uuid: UUID
    deck_uuid: UUID
    vocab_uuid: UUID
    owner_uuid: Optional[UUID]
    vocab: Optional[VocabSimplified]
    token: Optional[str]

# Properties to receive on question update
class QuestionUpdate(QuestionBase):
    pass


# Properties shared by models stored in DB
class QuestionInDBBase(QuestionBase):
    id: int
    uuid: UUID
    deck_uuid: UUID
    owner_uuid: Optional[UUID]
    date_added: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Question(QuestionBase):
    vocab: VocabSimplified

    class Config:
        orm_mode = True


# Properties properties stored in DB
class QuestionInDB(QuestionInDBBase):
    pass

class QuestionDBDump(QuestionBase):
    id: int
    uuid: UUID
    deck_uuid: UUID
    vocab_uuid: UUID
    owner_uuid: Optional[UUID]
    date_added: Optional[datetime]

    class Config:
        orm_mode = True