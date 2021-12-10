import datetime, uuid
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.definition import Definition
from app.schemas.definition import DefinitionCreate, DefinitionCreate


class CRUDDefinition(CRUDBase[Definition, DefinitionCreate, DefinitionCreate]):
    pass

    def create(self, db: Session, *, obj_in: DefinitionCreate) -> Definition:
        db_obj = Definition(
            uuid=uuid.uuid4,
            definition=obj_in.definition,
            region=obj_in.region,
            rank=obj_in.rank,
            lemma_uuid=None,
            note=obj_in.note,
            # date_added = datetime.datetime.now,
            date_deprecated=None,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    ## TODO change obj_in type to specific schema to take advantage of built in
    def create_from_dict(self, db: Session, *, dict_in: dict) -> Definition:
        db_obj = Definition(
            uuid=uuid.UUID(dict_in['uuid']),
            definition=dict_in['definition'],
            region=dict_in['region'],
            rank=dict_in['rank'],
            vocab_uuid=dict_in['vocab_uuid'],
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


definition = CRUDDefinition(Definition)
