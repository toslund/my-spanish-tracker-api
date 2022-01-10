from typing import List, Optional, Any
from uuid import UUID

from pydantic import BaseModel

from .question import Question


class AssessmentBase(BaseModel):
    deck_uuid: UUID
    bins: List[Any]
    questions_queue: List[Any]
