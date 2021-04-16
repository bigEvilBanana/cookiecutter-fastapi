from typing import Generator

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database import SessionLocal
from app.main import app
from app.schemas.user import User, UserCreate
from app.services import user as user_services


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user(db: Session) -> User:
    """Create and return new User"""
    fake = Faker()
    user_in = UserCreate(fullname=fake.name(), email=fake.email(), password=fake.name())
    user = user_services.create_user(db=db, user=user_in)
    return user


@pytest.fixture
def authentication_token(user: User) -> str:
    """Return a valid token for the user."""
    return create_access_token(user.id)
