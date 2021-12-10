import datetime, uuid
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, load_only
from sqlalchemy import text


from app.crud.base import CRUDBase
from app.models.deck import Deck
from app.schemas.deck import DeckCreate, DeckCreate
from app.db.session import engine


class CRUDDeck(CRUDBase[Deck, DeckCreate, DeckCreate]):
    pass
    # def get_mini(self):
    #     # slow slow slow
    #     # return db.query(Deck.word).all()
    #     # fast fast fast
    #     decks = None
    #     with engine.connect() as connection:
    #         decks = connection.execute(text("SELECT word FROM deck"))
    #         decks = decks.scalars().all()
    #     return decks
    #     # return db.query(Deck).all() #.options(load_only("id"))


    # def create(self, db: Session, *, obj_in: DeckCreate) -> Deck:
    #     db_obj = Deck(
    #         uuid=str(uuid.uuid4()),
    #         date_added = datetime.datetime.now,
    #         owner_uuid=obj_in.owner_uuid,
    #     )

    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)

    #     return db_obj
    

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


deck = CRUDDeck(Deck)
