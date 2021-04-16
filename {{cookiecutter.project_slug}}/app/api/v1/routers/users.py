from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas import user as user_schemas
from app.services import user as user_service

router = APIRouter()


@router.get("/", response_model=List[user_schemas.User])
def get_users(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    """Retrieve all users."""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_schemas.User)
def get_user(*, db: Session = Depends(deps.get_db), user_id: int) -> Any:
    """Get User by ID."""
    user = user_service.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this ID does not exist in the system",
        )
    return user


@router.post("/", response_model=user_schemas.User)
def create_user(*, db: Session = Depends(deps.get_db), user_in: user_schemas.UserCreate) -> Any:
    """Create new user."""
    user = user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = user_service.create_user(db, user=user_in)
    return user


@router.patch("/{user_id}", response_model=user_schemas.User)
def update_user(*, db: Session = Depends(deps.get_db), user_id: int, user_in: user_schemas.UserUpdate) -> Any:
    """Update User by ID"""
    user = user_service.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = user_service.update_user(db, db_user=user, user=user_in)
    return user
