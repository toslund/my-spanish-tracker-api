from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
# from app.models.definition import Definition

from .vocab import VocabDefs


# Shared properties
class LemmaWithVocab(BaseModel):
    uuid: UUID
    word: str
    rank: Optional[int]
    pos: str
    note: str
    note_grammar: str
    vocabs: List[VocabDefs]

    class Config:
        orm_mode = True