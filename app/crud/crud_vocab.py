import datetime, uuid
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, load_only
from sqlalchemy import text


from app.crud.base import CRUDBase
from app.models.vocab import Vocab
from app.schemas.vocab import VocabCreate, VocabCreate
from app.db.session import engine


class CRUDVocab(CRUDBase[Vocab, VocabCreate, VocabCreate]):
    def get_mini(self):
        # slow slow slow
        # return db.query(Vocab.word).all()
        # fast fast fast
        vocabs = None
        with engine.connect() as connection:
            vocabs = connection.execute(text("SELECT word FROM vocab"))
            vocabs = vocabs.scalars().all()
        return vocabs
        # return db.query(Vocab).all() #.options(load_only("id"))

    def create(self, db: Session, *, obj_in: VocabCreate) -> Vocab:
        db_obj = Vocab(
            uuid=str(uuid.uuid4()),
            word=obj_in.word,
            pos=obj_in.pos,
            lemma_uuid=None,
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
    def create_from_dict(self, db: Session, *, dict_in: dict) -> Vocab:
        db_obj = Vocab(
            uuid=uuid.UUID(dict_in['uuid']),
            word=dict_in['word'],
            pos=dict_in['pos'],
            lemma_uuid=dict_in['lemma_uuid'],
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
    #     self, db: Session, *, obj_in: ItemCreate, owner_uuid: int
    # ) -> Item:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_uuid=owner_uuid)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def get_multi_by_owner(
    #     self, db: Session, *, owner_uuid: int, skip: int = 0, limit: int = 100
    # ) -> List[Item]:
    #     return (
    #         db.query(self.model)
    #         .filter(Item.owner_uuid == owner_uuid)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )


vocab = CRUDVocab(Vocab)
