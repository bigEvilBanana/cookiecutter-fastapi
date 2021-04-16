from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models import user as user_models
from app.schemas import user as user_schemas


def authenticate(db: Session, email: str, password: str) -> Optional[user_schemas.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.password):  # noqa
        return None
    return user


def get_user_by_id(db: Session, user_id: int) -> user_schemas.User:
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> user_schemas.User:
    return db.query(user_models.User).filter(user_models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[user_schemas.User]:
    return db.query(user_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schemas.UserCreate) -> user_schemas.User:
    user.password = get_password_hash(user.password)
    db_user = user_models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: user_models.User, user: user_schemas.UserUpdate) -> user_schemas.User:
    # Update model class variable from requested fields
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value is not None else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
