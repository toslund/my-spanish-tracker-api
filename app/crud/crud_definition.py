import datetime, uuid
from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.definition import Definition
from app.schemas.definition import DefinitionCreate, DefinitionCreate, DefinitionSimplified


class CRUDDefinition(CRUDBase[Definition, DefinitionCreate, DefinitionCreate]):
    pass

    def create(self, db: Session, *, obj_in: DefinitionCreate) -> Definition:
        db_obj = Definition(
            uuid=uuid.uuid4,
            content=obj_in.content,
            region=obj_in.region,
            lemma_uuid=None,
            note=obj_in.note,
            # date_added = datetime.datetime.now,
            date_deprecated=None,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    def get_multi_by_vocab_uuids(self, db: Session, uuids: List[UUID]) -> List[Optional[DefinitionSimplified]]:
        return db.query(self.model).filter(self.model.vocab_uuid.in_(uuids)).all()

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
