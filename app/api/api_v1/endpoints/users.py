import timeit
from datetime import timedelta
from typing import Any, List, Dict, Union
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils import send_new_account_email, generate_confirm_email_token, verify_confirm_email_token
from app.services.prediction_service import Assessment


router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/confirm-email", response_model=schemas.Msg)
def confirm_email(
    token: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_confirm_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email no longer exists.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    # verify email
    print(f'verifying email {email}')
    # user = crud.user.update(db, db_obj=user, obj_in={'verified_email': True})
    return {"msg": "Email confirmed"}


# @router.put("/me", response_model=schemas.User)
# def update_user_me(
#     *,
#     db: Session = Depends(deps.get_db),
#     password: str = Body(None),
#     full_name: str = Body(None),
#     email: EmailStr = Body(None),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update own user.
#     """
#     current_user_data = jsonable_encoder(current_user)
#     user_in = schemas.UserUpdate(**current_user_data)
#     if password is not None:
#         user_in.password = password
#     if full_name is not None:
#         user_in.full_name = full_name
#     if email is not None:
#         user_in.email = email
#     user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
#     return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model= Dict[str, Union[schemas.Token, schemas.User]])
def create_user_open(
    background_tasks: BackgroundTasks,
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    uuid: UUID = Body(...),
    full_name: str = Body(None),
    username: str = Body(...),
    leave_blank: str = Body(...),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    startrequesttime = timeit.default_timer()
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden at this time",
        )
    elif settings.DECKS_OPEN_POST:
        # honey pot stuff for open POST
        if username or leave_blank != settings.OPEN_POST_KEY:
            raise HTTPException(status_code=400, detail="Bots bad")
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name, uuid=uuid)
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED:
        confirm_email_token = generate_confirm_email_token(email=user.email)
        background_tasks.add_task(send_new_account_email, email_to=user.email, token=confirm_email_token)
    # return user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = schemas.Token(
        access_token=security.create_access_token(user.uuid, user.email, user.is_superuser, expires_delta=access_token_expires),
        token_type="bearer"
        )
    endrequesttime = timeit.default_timer()
    print(f'total request time: {endrequesttime-startrequesttime}')
    response = {
        "token": token,  
        "user": user
    }
    print(response)
    return response


@router.get("/{user_uuid}", response_model=schemas.User)
def read_user_by_uuid(
    user_uuid: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get_by_uuid(db, uuid=user_uuid)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


# @router.put("/{user_uuid}", response_model=schemas.User)
# def update_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_uuid: str,
#     user_in: schemas.UserUpdate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Update a user.
#     """
#     user = crud.user.get(db, id=user_uuid)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )
#     user = crud.user.update(db, db_obj=user, obj_in=user_in)
#     return user

## TODO PRIORITY
## create seperate DELETE route for regular users
# @router.delete("/me", response_model=schemas.UserBase)
# def delete_lemma(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:

@router.delete("/{uuid}", response_model=schemas.UserBase)
def delete_lemma(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    """
    
    user = crud.user.get_by_uuid(db=db, uuid=uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_superuser:
        ## manually delete superusers via cli
        raise HTTPException(status_code=400, detail="Not enough permissions")
    user = crud.user.remove(db=db, uuid=uuid)
    return user

@router.get("/{uuid}/decks", response_model=List[Dict[str, Union[schemas.DeckSimplified, schemas.AssessmentBase]]])
def read_decks(
    uuid: UUID,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve decks.
    """
    if current_user.is_superuser:
        pass
    elif current_user.uuid != uuid:
        raise HTTPException(status_code=400, detail="Not enough permissions") 
    decks = crud.deck.get_multi_by_owner(
        db=db, owner_uuid=uuid, skip=skip, limit=limit
    )
    assessments = []
    all_ranks = crud.vocab.get_ranks(db)
    for deck in decks:
        deck_assessment = Assessment(deck.questions, all_ranks)
        assessment_payload = {
            'deck_uuid': deck.uuid,
            'bins': deck_assessment.bins,
            'questions_queue': deck_assessment.questions_queue,
        }
        assessments.append(assessment_payload)
    response = []
    for idx, deck in enumerate(decks):
        response.append({'deck': deck, 'assessment': assessments[idx]})
    return response

