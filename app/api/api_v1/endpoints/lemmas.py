from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Lemma])
def read_lemmas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve lemmas.
    """
    lemmas = crud.lemma.get_multi(
            db=db, skip=skip, limit=limit
        )
    return lemmas

@router.get("/all") # response_model=List[schemas.VocabBase], response_model_include={"word"}
def read_lemmas_all(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve all lemmas
    """
    lemmas = crud.lemma.get_mini(db=db)
    return lemmas

@router.get("/ranks") # response_model=List[schemas.VocabBase], response_model_include={"word"}
def read_lemmas_with_ranks(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all ranks as fast as possible
    """
    lemmas = crud.lemma.get_ranks(db)
    return lemmas

@router.get("/{uuid}", response_model=schemas.LemmaWithVocab)
def read_lemma_by_uuid(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    """
    Get lemma by ID.
    """
    lemma, rank = crud.lemma.get_by_uuid(db=db, uuid=uuid)
    if not lemma:
        raise HTTPException(status_code=404, detail="Lemma not found")
    lemma = schemas.LemmaWithVocab.from_orm(lemma)
    lemma.rank = rank
    return lemma

@router.get("/ranks/{rank}") # response_model=List[schemas.VocabBase], response_model_include={"word"}
def read_lemmas_by_rank(
    *,
    db: Session = Depends(deps.get_db),
    rank: int
) -> Any:
    """
    Retrieve a lemma with a current ranks. Ranks are fluid and subject to change.
    """
    lemmas = crud.lemma.get_by_rank(db=db, rank=rank)
    return lemmas


@router.post("/", response_model=schemas.Lemma)
def create_lemma(
    *,
    db: Session = Depends(deps.get_db),
    lemma_in: schemas.LemmaCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new lemma.
    """
    lemma = crud.lemma.create_with_owner(db=db, obj_in=lemma_in, owner_uuid=current_user.uuid)
    return lemma


# @router.put("/{id}", response_model=schemas.Lemma)
# def update_lemma(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     lemma_in: schemas.LemmaUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an lemma.
#     """
#     lemma = crud.lemma.get(db=db, id=id)
#     if not lemma:
#         raise HTTPException(status_code=404, detail="Lemma not found")
#     if not crud.user.is_superuser(current_user) and (lemma.owner_uuid != current_user.uuid):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     lemma = crud.lemma.update(db=db, db_obj=lemma, obj_in=lemma_in)
#     return lemma


@router.delete("/{uuid}", response_model=schemas.Lemma)
def delete_lemma(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an lemma.
    """
    lemma = crud.lemma.get_by_uuid(db=db, uuid=uuid)
    if not lemma:
        raise HTTPException(status_code=404, detail="Lemma not found")
    lemma = crud.lemma.remove(db=db, uuid=uuid)
    return lemma
