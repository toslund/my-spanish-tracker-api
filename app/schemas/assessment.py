from typing import List, Optional, Any
from uuid import UUID

from pydantic import BaseModel

from .question import Question


class AssessmentPayload(BaseModel):
    deck_uuid: UUID
    ranks: List[int]
    deficient: bool
    grouped_correct: Any
    deficient_groups: Any
    grouped_ranks: Any
    prediction: Optional[float]
    total_questions_to_go: int
    total_questions: int
