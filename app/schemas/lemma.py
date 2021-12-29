from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

# Shared properties
class LemmaBase(BaseModel):
    word: str
    pos: str
    note: str

# Shared properties
class LemmaSimplified(LemmaBase):
    note: str

    class Config:
        orm_mode = True
        
            
# Properties to receive on item creation
class LemmaCreate(LemmaBase):
    note_data: Optional[str]
    note_qaqc: Optional[str]
    note_grammar: Optional[str]

    # total_count: Optional[int] = 0
    # academic_count: Optional[int] = 0
    # news_count: Optional[int] = 0
    # fiction_count: Optional[int] = 0
    # spoken_count: Optional[int] = 0


# Properties to receive on item update
# class LemmaUpdate(ItemBase):
#     pass


# Properties shared by models stored in DB
class LemmaInDBBase(LemmaBase):
    id: int
    uuid: UUID
    date_added: Optional[datetime]
    date_deprecated: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Lemma(LemmaBase):
    uuid: UUID
    rank: Optional[int]

    class Config:
        orm_mode = True


# Properties properties stored in DB
class LemmaInDB(LemmaInDBBase):
    pass

# Properties for dumping to json
class LemmaDBDump(LemmaBase):
    # id: int
    uuid: UUID
    # lemma: str
    # pos: str
    # rank: Optional[int] = 9999999

    total_count: Optional[int] = 0
    academic_count: Optional[int] = 0
    news_count: Optional[int] = 0
    fiction_count: Optional[int] = 0
    spoken_count: Optional[int] = 0

    note_data: Optional[str]
    note_qaqc: Optional[str]
    note_grammar: str
    # note: str

    date_added: Optional[datetime]
    date_deprecated: Optional[datetime]

    class Config:
        orm_mode = True