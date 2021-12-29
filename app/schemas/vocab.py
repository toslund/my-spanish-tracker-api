from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
# from app.models.definition import Definition

from .definition import Definition, DefinitionSimplified

from .lemma import Lemma, LemmaSimplified


# Shared properties
class VocabBase(BaseModel):
    uuid: UUID
    word: str
    pos: str
    note: str

    class Config:
        orm_mode = True        

# Properties to receive on item creation
class VocabCreate(VocabBase):
    lemma_uuid: UUID
    note_data: Optional[str]
    note_qaqc: Optional[str]
    note_grammar: Optional[str]

class VocabSimplified(VocabBase):
    rank: Optional[int]
    # lemma: LemmaSimplified
    definitions: List[DefinitionSimplified]

class VocabDefs(VocabBase):
    definitions: List[DefinitionSimplified]

# Properties to receive on item update
# class VocabUpdate(ItemBase):
#     pass


# Properties shared by models stored in DB
class VocabInDBBase(VocabBase):
    id: int
    date_added: Optional[datetime]
    date_deprecated: Optional[datetime]
    lemma: Optional[Lemma] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Vocab(BaseModel):
    uuid: UUID
    date_added: Optional[datetime]
    date_deprecated: Optional[datetime]
    note_data: Optional[str]
    note_qaqc: Optional[str]
    note_grammar: Optional[str]
    lemma: Optional[Lemma] = None
    definitions: List[Definition]

    class Config:
        orm_mode = True


# Properties properties stored in DB
class VocabInDB(VocabInDBBase):
    pass

# Properties for dumping to json
class VocabDBDump(VocabBase):
    # id: int
    uuid: UUID
    note_data: Optional[str]
    note_qaqc: Optional[str]
    note_grammar: Optional[str]
    date_added: Optional[datetime]
    date_deprecated: Optional[datetime]
    lemma_uuid: Optional[UUID] = None

    class Config:
        orm_mode = True

# # Properties for dumping to json
# class VocabMini(VocabBase):
#     # id: int
#     uuid: str
#     note_data: Optional[str]
#     note_qaqc: Optional[str]
#     date_added: datetime
#     date_deprecated: Optional[datetime]
#     lemma_uuid: Optional[str] = None

#     class Config:
#         orm_mode = True

