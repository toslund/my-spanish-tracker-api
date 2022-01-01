import random
from typing import Any, List, Union, Dict
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from jose import jwt

from app import crud, models, schemas
from app.api import deps
from app.api.api_v1.endpoints import lemmas
from app.core.config import settings
from app.core import security
from app.schemas import assessment
from app.services.prediction_service import Assessment


router = APIRouter()


@router.get("/", response_model=List[schemas.Deck])
def read_decks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve decks.
    """
    if crud.user.is_superuser(current_user):
        decks = crud.deck.get_multi(db, skip=skip, limit=limit)
    else:
        decks = crud.deck.get_multi_by_owner(
            db=db, owner_uuid=current_user.uuid, skip=skip, limit=limit
        )
    return decks

@router.get("/{uuid}", response_model=schemas.Deck)
def read_deck_by_uuid(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_user_or_none),
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get deck by ID.
    """
    deck = crud.deck.get_by_uuid(db=db, uuid=uuid)
    ## Decks with owners should only be seen by owners and superusers
     #TODO upgrade to python 3.10 to use match statement
    if deck.owner_uuid == None:
        ## all anonymous decks are freely accessible
        pass
    elif current_user.is_superuser:
        pass
    elif current_user and current_user.uuid == deck.owner_uuid:
        pass
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    # if not crud.user.is_superuser(current_user) and (deck.owner_uuid != current_user.uuid):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")

    all_ranks = crud.vocab.get_ranks(db)
    predictions = []
    questions = []
    assessment_bins = []
    for question in deck.questions:
        questions.append(question)
        current_assessment = Assessment(questions, all_ranks, generate_questions_queue=False)
        predictions.append(current_assessment.prediction)
        assessment_bins.append(current_assessment.bins)
    print(type(predictions[0]))
    print(predictions[0])
    print(type(predictions[15]))
    print(predictions[15])
    deck = schemas.Deck(
        uuid=deck.uuid,
        questions=deck.questions,
        predictions=predictions,
        owner=deck.owner,
        date_added=deck.date_added,
    )
    return deck

# @router.get("/question", response_model=List[schemas.Deck])
# def read_decks(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Retrieve decks.
#     """
#     if crud.user.is_superuser(current_user):
#         decks = crud.deck.get_multi(db, skip=skip, limit=limit)
#     else:
#         decks = crud.deck.get_multi_by_owner(
#             db=db, owner_uuid=current_user.uuid, skip=skip, limit=limit
#         )
#     return decks


@router.get("/{deck_uuid}/question", response_model=schemas.QuestionProvisionalCreate)
def generate_deck_question(
    *,
    db: Session = Depends(deps.get_db),
    deck_uuid: UUID,
    vocab_uuid: UUID = None,
    current_user: models.User = Depends(deps.get_user_or_none),
) -> Any:
    """
    Get deck by ID.
    """
    deck = crud.deck.get_by_uuid(db=db, uuid=deck_uuid)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if not vocab_uuid:
        all_ranks = crud.vocab.get_ranks(db)
        deck_assessment = Assessment(deck.questions, all_ranks)
        vocab_uuid = deck_assessment.get_assesment_question()
        question_rank = True
        ## TODO fix
        if not question_rank:
            question_rank = deck_assessment.get_random_question_no_replacement()
            vocab_uuid = deck_assessment.get_random_question_no_replacement()
        # vocab_uuid = random.choice(crud.vocab.get_by_rank(db, vocab_rank=question_rank))
    vocab = crud.vocab.get_by_uuid(db, uuid=vocab_uuid)
    question_uuid = uuid4()
    question_token = security.create_post_question_token(uuid=question_uuid, vocab_uuid=vocab.uuid, deck_uuid=deck_uuid)
    question = schemas.QuestionProvisionalCreate(uuid=question_uuid, deck_uuid=deck_uuid, vocab_uuid=vocab.uuid, vocab = vocab, token=question_token)
    return question


@router.get("/{uuid}/assessment")
def generate_deck_assessment(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_user_or_none),
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get deck by ID.
    """
    deck = crud.deck.get_by_uuid(db=db, uuid=uuid)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    ## Decks with owners should only be seen by owners and superusers
     #TODO upgrade to python 3.10 to use match statement
    if deck.owner_uuid == None:
        ## all anonymous decks are freely accessible
        pass
    elif current_user.is_superuser:
        pass
    elif current_user and current_user.uuid == deck.owner_uuid:
        pass
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions") 
    all_ranks = crud.vocab.get_ranks(db)
    deck_assessment = Assessment(deck.questions, all_ranks)
    assessment_payload = {
        'deck_uuid': deck.uuid,
        'bins': deck_assessment.bins,
        'questions': deck_assessment.questions,
        'questions_queue': deck_assessment.questions_queue,
        'prediction': deck_assessment.prediction
    }
    # assessment_payload = schemas.AssessmentPayload(
    #     deck_uuid=deck.uuid,
    #     ranks=deck_assessment.ranks,
    #     grouped_correct=deck_assessment.grouped_correct,
    #     grouped_ranks=deck_assessment.grouped_ranks,
    #     deficient=deck_assessment.deficient,
    #     deficient_groups=deck_assessment.deficient_groups,
    #     prediction=deck_assessment.prediction,
    #     total_questions_to_go=deck_assessment.total_questions_to_go,
    #     total_questions = deck_assessment.total_questions)
    return assessment_payload

@router.post("/{deck_uuid}", response_model=Dict[str, Union[str, schemas.DeckSimplified]])
def create_deck(
    response: Response,
    *,
    db: Session = Depends(deps.get_db),
    deck_uuid: UUID,
    deck_in: schemas.DeckCreate,
    current_user: models.User = Depends(deps.get_user_or_none),
) -> Any:
    """
    Create new deck.
    """
    if current_user:
        if (deck_in.owner_uuid != current_user.uuid) and not current_user.is_superuser:
            raise HTTPException(status_code=422, detail="Owner does not match current authenticated user.")
        # TODO implement create_with_owner deck method
        # deck = crud.deck.create_with_owner(db=db, obj_in=deck_in, owner_uuid=current_user.uuid)
    elif settings.DECKS_OPEN_POST:
        # honey pot stuff for open POST
        if deck_in.email or deck_in.name != settings.OPEN_POST_KEY:
            raise HTTPException(status_code=400, detail="Bots bad")
    else:
        raise HTTPException(status_code=400, detail="Anonymous posing not allowed at this time")  
    if deck_uuid != deck_in.uuid:
        raise HTTPException(status_code=422, detail="Mismatching UUID")
    deck = crud.deck.get_by_uuid(db=db, uuid=deck_in.uuid)
    if deck:
        raise HTTPException(status_code=404, detail="Already exists")
    deck = crud.deck.create(db=db, obj_in=deck_in, exclude={'name', 'email'})
    deck_token = security.create_new_deck_token(deck_uuid=deck_uuid)
    response.set_cookie(key="deck_token", value=deck_token, samesite="none", secure=True)

    return {'deck_token': deck_token, 'deck': deck}

@router.post("/{deck_uuid}/question/{question_uuid}", response_model=schemas.Question)
def create_question_in_deck(
    *,
    db: Session = Depends(deps.get_db),
    question_in: schemas.QuestionCreate,
    deck_uuid: UUID,
    question_uuid: UUID,
    current_user: models.User = Depends(deps.get_user_or_none),
) -> Any:
    """
    Create new question for deck.
    """

    if not current_user:
        try:
            payload = jwt.decode(
                question_in.token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
        except jwt.JWTError as e:
            payload = {}
    try:
        verified_question_uuid = UUID(payload.get('uuid'))
        verified_vocab_uuid = UUID(payload.get('vocab_uuid'))
        verified_deck_uuid = UUID(payload.get('deck_uuid'))
    except TypeError as e:
        raise HTTPException(status_code=404, detail="Invalid request")
    if current_user:
        question_in.owner_uuid = current_user.uuid
    if verified_question_uuid != question_in.uuid or verified_vocab_uuid != question_in.vocab_uuid or verified_deck_uuid != question_in.deck_uuid:
        raise HTTPException(status_code=404, detail="Invalid request")
    question = crud.question.get_by_uuid(db=db, uuid=verified_question_uuid)
    if question:
        raise HTTPException(status_code=404, detail="Already exists")
    exclude_keys = {
        'vocab': ...,
        'token': ...
    }
    question = crud.question.create(db=db, obj_in=question_in, exclude=exclude_keys)
    return question

# @router.put("/{id}", response_model=schemas.Deck)
# def update_deck(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     deck_in: schemas.DeckUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an deck.
#     """
#     deck = crud.deck.get(db=db, id=id)
#     if not deck:
#         raise HTTPException(status_code=404, detail="Deck not found")
#     if not crud.user.is_superuser(current_user) and (deck.owner_uuid != current_user.uuid):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     deck = crud.deck.update(db=db, db_obj=deck, obj_in=deck_in)
#     return deck

@router.delete("/{id}", response_model=schemas.Deck)
def delete_deck(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an deck.
    """
    deck = crud.deck.get(db=db, id=id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    if not crud.user.is_superuser(current_user) and (deck.owner_uuid != current_user.uuid):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    deck = crud.deck.remove(db=db, id=id)
    return deck
