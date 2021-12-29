import datetime, uuid
from typing import List
import timeit

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.crud.base import CRUDBase
from app.models.lemma import Lemma
from app.schemas.lemma import LemmaCreate, LemmaCreate, LemmaSimplified
from app.db.session import engine


class CRUDLemma(CRUDBase[Lemma, LemmaCreate, LemmaCreate]):
    pass

    def create(self, db: Session, *, obj_in: LemmaCreate) -> Lemma:
        db_obj = Lemma(
            uuid=uuid.uuid4,
            word=obj_in.word,
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
    


    # def create_with_owner(
    #     self, db: Session, *, obj_in: ItemCreate, owner_uuid: int
    # ) -> Item:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_uuid=owner_uuid)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    def get_mini(self, db):
        # slow slow slow
        # return db.query(Vocab.word).all()
        # fast fast fast
        lemmas = None
        query_text = text("WITH ranked AS (SELECT uuid, word, pos, DENSE_RANK () OVER ( ORDER BY total_count DESC) rank FROM lemma) SELECT * from ranked")
        result = db.execute(query_text)
        lemmas = result.all()
        return lemmas
        # return db.query(Vocab).all() #.options(load_only("id"))

    def get_ranks(self, db: Session):
        # slow slow slow
        # return db.query(Vocab.word).all()
        # fast fast fast
        query_text = text("WITH ranked AS (SELECT uuid, word, pos, rank, DENSE_RANK () OVER ( ORDER BY total_count DESC) newrank FROM public.lemma WHERE total_count != 0) SELECT * from ranked")
        query_text = text("""
        SELECT
            uuid,
            DENSE_RANK () OVER ( 
                ORDER BY total_count DESC
            ) rank 
        FROM
            lemma
        WHERE total_count != 0
        """)
        # lemmas = None
        # with engine.connect() as connection:
        #     result = connection.execute(query_text)
        #     lemmas = result.all()
        result = db.execute(query_text)
        lemmas = result.all()
        return lemmas
        # return db.query(Vocab).all() #.options(load_only("id"))

    def get_rank_by_uuid(self, db: Session, *, lemma_uuid: uuid.UUID):
        # slow slow slow
        # return db.query(Vocab.word).all()
        # fast fast fast
        query_text = text("WITH ranked AS (SELECT uuid, word, pos, rank, DENSE_RANK () OVER ( ORDER BY total_count DESC) newrank FROM public.lemma WHERE total_count != 0) SELECT * from ranked")
        query_text = text("""
        WITH ranked_lemma AS (
            SELECT
                uuid,
                DENSE_RANK () OVER ( 
                    ORDER BY total_count DESC
                ) rank 
            FROM
                lemma
            WHERE total_count != 0
        )
        SELECT
        rank as new_rank
        FROM
        ranked_lemma
        WHERE
        uuid=:lemma_uuid
        """).bindparams(lemma_uuid=lemma_uuid)
        # lemmas = None
        # with engine.connect() as connection:
        #     result = connection.execute(query_text)
        #     lemmas = result.all()
        result = db.execute(query_text)
        rank = result.scalar()
        return rank
        # return db.query(Vocab).all() #.options(load_only("id"))

    def get_by_rank(self, db: Session, *, rank: int):
        # slow slow slow
        # return db.query(Vocab.word).all()
        # fast fast fast
        query_text = text("WITH ranked AS (SELECT uuid, word, pos, rank, DENSE_RANK () OVER ( ORDER BY total_count DESC) newrank FROM public.lemma WHERE total_count != 0) SELECT * from ranked")
        query_text = text("""
        WITH ranked_lemma AS (
            SELECT
                uuid,
                DENSE_RANK () OVER ( 
                    ORDER BY total_count DESC
                ) rank 
            FROM
                lemma
            WHERE total_count != 0
        )
        SELECT
        uuid,
        rank
        FROM
        ranked_lemma
        WHERE
        rank=:lemma_rank
        """).bindparams(lemma_rank=rank)
        # lemmas = None
        # with engine.connect() as connection:
        #     result = connection.execute(query_text)
        #     lemmas = result.all()
        result = db.execute(query_text)
        lemmas = result.all()
        return lemmas
        # return db.query(Vocab).all() #.options(load_only("id"))

    def get_by_uuid(self, db: Session, uuid: uuid) -> Lemma:
        lemma = db.query(self.model).filter(self.model.uuid == uuid).first()
        rank = self.get_rank_by_uuid(db=db, lemma_uuid=lemma.uuid)
        return lemma, rank

    # def get_by_rank(
    #     self, db: Session, *, rank: int
    # ) -> Lemma:
    #     return (
    #         db.query(self.model)
    #         .filter(Lemma.rank == rank)
    #         .first()
    #     )
    
    def get_multi_by_rank(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[LemmaSimplified]:
        return (
            db.query(self.model)
            .filter(self.model.rank is not None)
            .order_by(self.model.rank)
            .offset(skip)
            .limit(limit)
            .all()
        )
        # TODO optimize this query. Thought this would be more performative, but it's actually not
        # return (
        #     db.query(self.model).
        #     filter(self.model.rank > skip)
        #     .order_by(self.model.rank)
        #     .limit(limit)
        #     .all()
        # )


lemma = CRUDLemma(Lemma)
