import datetime, uuid
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, load_only
from sqlalchemy import text


from app.crud.base import CRUDBase
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionCreate
from app.db.session import engine


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionCreate]):
    pass
    # def get_mini(self):
    #     # slow slow slow
    #     # return db.query(Question.word).all()
    #     # fast fast fast
    #     vocabs = None
    #     with engine.connect() as connection:
    #         vocabs = connection.execute(text("SELECT word FROM vocab"))
    #         vocabs = vocabs.scalars().all()
    #     return vocabs
    #     # return db.query(Question).all() #.options(load_only("id"))

    # def create(self, db: Session, *, obj_in: QuestionCreate) -> Question:
    #     db_obj = Question(
    #         uuid=str(uuid.uuid4()),
    #         correct=obj_in.correct,
    #         correctness=obj_in.correctness,
    #         date_added = datetime.datetime.now,
    #         deck_uuid=obj_in.deck_uuid,
    #         vocab_uuid=obj_in.vocab_uuid,
    #     )

    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)

    #     return db_obj
    

    # def create_with_owner(
    #     self, db: Session, *, obj_in: QuestionCreate, owner_uuid: int
    # ) -> Question:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_uuid=owner_uuid)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    def get_multi_by_deck(
        self, db: Session, *, deck_uuid: int, skip: int = 0, limit: int = 100
    ) -> List[Question]:
        return (
            db.query(self.model)
            .filter(Question.deck_uuid == deck_uuid)
            .offset(skip)
            .limit(limit)
            .all()
        )


question = CRUDQuestion(Question)
