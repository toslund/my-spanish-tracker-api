import datetime, uuid
from typing import List, Any
import timeit

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, load_only
from sqlalchemy import text
from sqlalchemy.sql.expression import desc


from app.crud.base import CRUDBase
from app.models.vocab import Vocab
from app.models.lemma import Lemma
from app.schemas.vocab import VocabCreate, VocabCreate, VocabSimplified
from app.db.session import engine


class CRUDVocab(CRUDBase[Vocab, VocabCreate, VocabCreate]):
    def get_mini(self, db):
        # slow slow slow
        # return db.query(Vocab.word).all()
        # fast fast fast
        vocabs = None
        query_text = text("SELECT word, uuid, pos, lemma_uuid FROM vocab")
        result = db.execute(query_text)
        vocabs = result.all()
        return vocabs
        # return db.query(Vocab).all() #.options(load_only("id"))
    
    def get_by_rank(self, db: Session, *, vocab_rank: int):
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
        vocab.uuid
        FROM
        vocab
        JOIN ranked_lemma
        ON ranked_lemma.uuid=vocab.lemma_uuid
        WHERE
        ranked_lemma.rank = :vocab_rank
        """).bindparams(vocab_rank=vocab_rank)
        # lemmas = None
        # with engine.connect() as connection:
        #     result = connection.execute(query_text)
        #     lemmas = result.all()
        result = db.execute(query_text)
        vocabs = list(result.scalars())
        return vocabs
        # return db.query(Vocab).all() #.options(load_only("id"))

    def get_multi_by_rank(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Any:
        query_text = text("""
        WITH ranked_lemma AS (
            SELECT
                uuid,
                DENSE_RANK () OVER ( 
                    ORDER BY total_count DESC
                ) rank 
            FROM
                public.lemma
            WHERE total_count != 0
            )
        SELECT
        vocab.uuid as uuid,
        vocab.word,
        vocab.pos,
        vocab.note,
        rank
        FROM
        public.vocab
        JOIN ranked_lemma
        ON ranked_lemma.uuid=vocab.lemma_uuid
        OFFSET :skip LIMIT :limit
        """).bindparams(skip=skip, limit=limit)
        result = db.execute(query_text)
        vocabs = result.all()
        return vocabs

        return db.query(self.model).offset(skip).limit(limit).all()

    def get_ranks_by_uuids(self, db: Session, *, vocab_uuids: "List[uuid.UUID]"):
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
        vocab.uuid as uuid,
        rank
        FROM
        vocab
        JOIN ranked_lemma
        ON ranked_lemma.uuid=vocab.lemma_uuid
        WHERE
        vocab.uuid = Any(:vocab_uuids)
        """).bindparams(vocab_uuids=vocab_uuids)
        # lemmas = None
        # with engine.connect() as connection:
        #     result = connection.execute(query_text)
        #     lemmas = result.all()
        result = db.execute(query_text)
        return result.all()
        # return db.query(Vocab).all() #.options(load_only("id"))

    def get_ranks(self, db: Session):
        query_text = text("""
        WITH ranked_lemma AS (
            SELECT
                uuid,
                DENSE_RANK () OVER ( 
                    ORDER BY total_count DESC
                ) rank 
            FROM
                public.lemma
            WHERE total_count != 0
            )
        SELECT
        vocab.uuid as uuid,
        rank
        FROM
        public.vocab
        JOIN ranked_lemma
        ON ranked_lemma.uuid=vocab.lemma_uuid
        ORDER BY rank ASC
        """)
        ## I don't need the ORDER BY but I don't know why
        ##
        # lemmas = None
        # with engine.connect() as connection:
        #     result = connection.execute(query_text)
        #     lemmas = result.all()
        result = db.execute(query_text)
        vocabs = result.all()
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

    def get_number_of_ranked(self, db: Session):
        count = db.query(self.model).join(Lemma).filter(Lemma.total_count != 0).count()
    
        # TODO not optimized. See following for hints
        # count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        # count = q.session.execute(count_q).scalar()
        return count

    # def get_multi_by_rank(
    #     self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[VocabSimplified]:
    #     return (
    #         db.query(self.model).join(Lemma)
    #         .order_by(Lemma.rank)
    #         .filter(Lemma.rank < 10000)
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )
    
    # def create_with_owner(
    #     self, db: Session, *, obj_in: ItemCreate, owner_uuid: int
    # ) -> Item:
    #     obj_in_data = jsonable_encoder(obj_in)
    #     db_obj = self.model(**obj_in_data, owner_uuid=owner_uuid)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

 


vocab = CRUDVocab(Vocab)
