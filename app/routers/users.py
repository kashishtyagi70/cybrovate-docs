from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.role import RoleRead
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserWithRoles
from app.services import role_service, user_service

router = APIRouter(prefix="/users", tags=["users"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: DbSession) -> UserRead:
    try:
        return user_service.create_user(db, user_in)
    except user_service.DuplicateUserError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=list[UserRead])
def list_users(db: DbSession, skip: int = 0, limit: int = 100) -> list[UserRead]:
    return user_service.list_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserWithRoles)
def get_user(user_id: int, db: DbSession) -> UserWithRoles:
    user = user_service.get_user_with_roles(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_in: UserUpdate, db: DbSession) -> UserRead:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        return user_service.update_user(db, user, user_in)
    except user_service.DuplicateUserError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DbSession) -> Response:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_service.delete_user(db, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{user_id}/roles/{role_id}", response_model=UserWithRoles)
def assign_role_to_user(user_id: int, role_id: int, db: DbSession) -> UserWithRoles:
    user = user_service.get_user_with_roles(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    role = role_service.get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return user_service.assign_role(db, user, role)


@router.get("/{user_id}/roles", response_model=list[RoleRead])
def get_user_roles(user_id: int, db: DbSession) -> list[RoleRead]:
    user = user_service.get_user_with_roles(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.roles
