from datetime import datetime, timedelta
from typing import Any, Union
from uuid import UUID

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], user_email: str, is_superuser: bool, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "email": user_email, "is_superuser": is_superuser}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_new_deck_token(
    deck_uuid: UUID, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "deck_uuid": str(deck_uuid)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_post_question_token(
    uuid: UUID, vocab_uuid: UUID, deck_uuid: UUID, expires_delta: timedelta = None, nbf_delta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            seconds=settings.POST_QUESTION_TOKEN_EXPIRES_SECONDS
        )
    if nbf_delta:
        nbf = expire = datetime.utcnow() + nbf_delta
    else:
        nbf = datetime.utcnow() + timedelta(
            seconds=settings.POST_QUESTION_TOKEN_NBF_SECONDS
        )
    to_encode = {"nbf": nbf, "exp": expire, "uuid": str(uuid), "vocab_uuid": str(vocab_uuid), "deck_uuid": str(deck_uuid)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
