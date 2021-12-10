from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Question])
def read_questions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    deck_uuid: str = None,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve questions.
    """
    if deck_uuid:
        this_deck=crud.deck.get_by_uuid(db=db, uuid=deck_uuid)
        if this_deck:
            questions = crud.question.get_multi_by_deck(db, deck_uuid=deck_uuid)
    # if crud.user.is_superuser(current_user):
    #     questions = crud.question.get_multi(db, skip=skip, limit=limit)
    else:
        questions = crud.question.get_multi(
            db=db, skip=skip, limit=limit
        )
    return questions


@router.post("/", response_model=schemas.Question)
def create_question(
    *,
    db: Session = Depends(deps.get_db),
    question_in: schemas.QuestionCreate,
    deck_uuid: str,
) -> Any:
    """
    Create new question.
    """
    this_deck = None
    if deck_uuid:
        this_deck=crud.deck.get_by_uuid(db=db, uuid=deck_uuid)
    if not this_deck:
        raise HTTPException(status_code=404, detail="invalid deck")
    question = crud.question.create(db=db, obj_in=question_in)
    return question


@router.put("/{id}", response_model=schemas.Question)
def update_question(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    question_in: schemas.QuestionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an question.
    """
    question = crud.question.get(db=db, id=id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if not crud.user.is_superuser(current_user) and (question.owner_uuid != current_user.uuid):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    question = crud.question.update(db=db, db_obj=question, obj_in=question_in)
    return question


@router.get("/{id}", response_model=schemas.Question)
def read_question(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get question by ID.
    """
    question = crud.question.get(db=db, id=id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if not crud.user.is_superuser(current_user) and (question.owner_uuid != current_user.uuid):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return question


@router.delete("/{id}", response_model=schemas.Question)
def delete_question(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a question.
    """
    question = crud.question.get(db=db, id=id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if not crud.user.is_superuser(current_user) and (question.owner_uuid != current_user.uuid):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    question = crud.question.remove(db=db, id=id)
    return question
