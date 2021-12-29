from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Definition])
def read_definitions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve definitions.
    """
    if crud.user.is_superuser(current_user):
        definitions = crud.definition.get_multi(db, skip=skip, limit=limit)
    else:
        definitions = crud.definition.get_multi_by_owner(
            db=db, owner_uuid=current_user.uuid, skip=skip, limit=limit
        )
    return definitions

@router.get("/{uuid}", response_model=schemas.Definition)
def read_definition(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    """
    Get definition by ID.
    """
    definition = crud.definition.get_by_uuid(db=db, uuid=uuid)
    if not definition:
        raise HTTPException(status_code=404, detail="Definition not found")
    return definition

# @router.post("/{uuid}", response_model=schemas.Definition)
# def create_definition(
#     *,
#     db: Session = Depends(deps.get_db),
#     uuid: UUID,
#     definition_in: schemas.DefinitionCreate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Create new definition.
#     """
#     definition = crud.definition.create_with_owner(db=db, obj_in=definition_in, owner_uuid=current_user.uuid)
#     return definition


# @router.put("/{id}", response_model=schemas.Definition)
# def update_definition(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     definition_in: schemas.DefinitionUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an definition.
#     """
#     definition = crud.definition.get(db=db, id=id)
#     if not definition:
#         raise HTTPException(status_code=404, detail="Definition not found")
#     if not crud.user.is_superuser(current_user) and (definition.owner_uuid != current_user.uuid):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     definition = crud.definition.update(db=db, db_obj=definition, obj_in=definition_in)
#     return definition



# @router.delete("/{id}", response_model=schemas.Definition)
# def delete_definition(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an definition.
#     """
#     definition = crud.definition.get(db=db, id=id)
#     if not definition:
#         raise HTTPException(status_code=404, detail="Definition not found")
#     if not crud.user.is_superuser(current_user) and (definition.owner_uuid != current_user.uuid):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     definition = crud.definition.remove(db=db, id=id)
#     return definition
