from math import ceil
from typing import Any, List, Optional, Dict, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()

@router.get("/", response_model=Dict[str, Union[int, List[schemas.VocabSimplified]]])
def read_vocabs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve vocabs.
    """
    if limit > 100:
        raise HTTPException(status_code=422, detail="Too many items requested")
    total_count = crud.vocab.get_number_of_ranked(db)
    total_pages = ceil(total_count/limit)
    ## TODO either change this to get definitions in one textual query or change the front end to request definitions seperately
    vocabs = [dict(vocab) for vocab in crud.vocab.get_multi_by_rank(db, skip=skip, limit=limit)]
    uuids = [vocab['uuid'] for vocab in vocabs]
    definitions= crud.definition.get_multi_by_vocab_uuids(db, uuids=uuids)
    definition_dict = {}
    for definition in definitions:
        if definition.vocab_uuid not in definition_dict:
            definition_dict[definition.vocab_uuid] = []
        definition_dict[definition.vocab_uuid].append(definition)
    for vocab in vocabs:
        vocab['definitions'] = definition_dict[vocab['uuid']]

    return {'total_count': total_count, 'total_pages': total_pages, 'vocabs': vocabs}

@router.get("/all") # response_model=List[schemas.VocabBase], response_model_include={"word"}
def read_vocabs_all(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve all vocabs with UUID, POS, and LEMMA UUID
    """
    vocabs = crud.vocab.get_mini(db)
    return vocabs

@router.get("/ranks") # response_model=List[schemas.VocabBase], response_model_include={"word"}
def read_vocabs_ranks(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all vocav ranks as fast as possible
    """
    vocabs = crud.vocab.get_ranks(db)
    return vocabs
    
@router.get("/{uuid}", response_model=schemas.Vocab)
def read_by_uuid(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    """
    Get definition by ID.
    """
    vocab = crud.vocab.get_by_uuid(db=db, uuid=uuid)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocab not found")
    return vocab

@router.get("/{uuid}/definitions", response_model=List[schemas.Definition])
def read_vocab_definitions(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    """
    Get definition by ID.
    """
    vocab = crud.vocab.get_by_uuid(db=db, uuid=uuid)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocab not found")
    return vocab.definitions

@router.get("/{uuid}/lemma", response_model=schemas.Lemma)
def read_vocab_lemma(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    """
    Get definition by ID.
    """
    vocab = crud.vocab.get_by_uuid(db=db, uuid=uuid)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocab not found")
    return vocab.lemma

# @router.post("/", response_model=schemas.Item)
# def create_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     item_in: schemas.ItemCreate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Create new item.
#     """
#     item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_uuid=current_user.uuid)
#     return item


# @router.put("/{id}", response_model=schemas.Item)
# def update_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     item_in: schemas.ItemUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an item.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_uuid != current_user.uuid):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
#     return item


# @router.get("/{id}", response_model=schemas.Item)
# def read_item(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get item by ID.
#     """
#     item = crud.item.get(db=db, id=id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     if not crud.user.is_superuser(current_user) and (item.owner_uuid != current_user.uuid):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     return item


@router.delete("/{uuid}", response_model=schemas.Vocab)
def delete_vocab(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an vocab.
    """
    vocab = crud.vocab.get(db=db, uuid=uuid)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocab not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    vocab = crud.vocab.remove(db=db, uuid=uuid)
    return vocab
