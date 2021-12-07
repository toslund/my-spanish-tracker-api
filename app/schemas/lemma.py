from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class LemmaBase(BaseModel):
    lemma: str
    pos: str
    rank: Optional[int] = 9999999

    total_count: Optional[int] = 0
    academic_count: Optional[int] = 0
    news_count: Optional[int] = 0
    fiction_count: Optional[int] = 0
    spoken_count: Optional[int] = 0

    note_grammar: str
    note: str
            

# Properties to receive on item creation
class LemmaCreate(LemmaBase):
    note_data: Optional[str]
    note_qaqc: Optional[str]


# Properties to receive on item update
# class LemmaUpdate(ItemBase):
#     pass


# Properties shared by models stored in DB
class LemmaInDBBase(LemmaBase):
    id: int
    uuid: str
    date_added: datetime
    date_deprecated: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class Lemma(LemmaBase):
    id: int
    date_added: datetime
    date_deprecated: Optional[datetime]

    class Config:
        orm_mode = True


# Properties properties stored in DB
class LemmaInDB(LemmaInDBBase):
    pass

# Properties for dumping to json
class LemmaDBDump(LemmaBase):
    # id: int
    uuid: str
    # lemma: str
    # pos: str
    # rank: Optional[int] = 9999999

    # total_count: Optional[int] = 0
    # academic_count: Optional[int] = 0
    # news_count: Optional[int] = 0
    # fiction_count: Optional[int] = 0
    # spoken_count: Optional[int] = 0

    note_data: Optional[str]
    note_qaqc: Optional[str]
    # note_grammar: str
    # note: str

    date_added: datetime
    date_deprecated: Optional[datetime]

    class Config:
        orm_mode = True