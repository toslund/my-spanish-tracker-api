import datetime, uuid
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lemma import Lemma
from app.schemas.lemma import LemmaCreate, LemmaCreate


class CRUDLemma(CRUDBase[Lemma, LemmaCreate, LemmaCreate]):
    pass

    def create(self, db: Session, *, obj_in: LemmaCreate) -> Lemma:
        db_obj = Lemma(
            uuid=str(uuid.uuid4()),
            lemma=obj_in.lemma,
            pos=obj_in.pos,
            rank=obj_in.rank,

            total_count=obj_in.total_count,
            academic_count=obj_in.academic_count,
            news_count=obj_in.news_count,
            fiction_count=obj_in.fiction_count,
            spoken_count=obj_in.spoken_count,

            note_data=obj_in.note_data,
            note_qaqc=obj_in.note_qaqc,
            note_grammar=obj_in.note_grammar,
            note=obj_in.note,
            
            date_added = datetime.datetime.now,
            date_deprecated=None,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    ## TODO change obj_in type to specific schema to take advantage of built in
    def create_from_dict(self, db: Session, *, dict_in: dict) -> Lemma:
        db_obj = Lemma(
            uuid=dict_in['uuid'],
            lemma=dict_in['lemma'],
            pos=dict_in['pos'],
            rank=dict_in['rank'],

            total_count=dict_in['total_count'],
            academic_count=dict_in['academic_count'],
            news_count=dict_in['news_count'],
            fiction_count=dict_in['fiction_count'],
            spoken_count=dict_in['spoken_count'],

            note_data=dict_in['note_data'],
            note_qaqc=dict_in['note_qaqc'],
            note_grammar=dict_in['note_grammar'],
            note=dict_in['note'],
            date_added = datetime.datetime.fromtimestamp(dict_in['date_added']),
            date_deprecated= dict_in['date_deprecated'],
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    # def create_with_owner(
    #     self, db: Session, *, obj_in: ItemCreate, owner_id: int
    # ) -> Item:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_id=owner_id)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def get_multi_by_owner(
    #     self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    # ) -> List[Item]:
    #     return (
    #         db.query(self.model)
    #         .filter(Item.owner_id == owner_id)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )


lemma = CRUDLemma(Lemma)
