from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
# from app.models.definition import Definition

from .definition import Definition

from .lemma import Lemma


# Shared properties
class VocabBase(BaseModel):
    word: str
    pos: str
    note_grammar: str
    note: str
    lemma_uuid: Optional[str] = None

    class Config:
        orm_mode = True
            

# Properties to receive on item creation
class VocabCreate(VocabBase):
    note_data: Optional[str]
    note_qaqc: Optional[str]


# Properties to receive on item update
# class VocabUpdate(ItemBase):
#     pass


# Properties shared by models stored in DB
class VocabInDBBase(VocabBase):
    id: int
    uuid: str
    date_added: datetime
    date_deprecated: Optional[datetime]
    lemma: Optional[Lemma] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Vocab(BaseModel):
    uuid: str
    date_added: datetime
    date_deprecated: Optional[datetime]
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
    uuid: str
    note_data: Optional[str]
    note_qaqc: Optional[str]
    date_added: datetime
    date_deprecated: Optional[datetime]
    lemma_uuid: Optional[str] = None

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

