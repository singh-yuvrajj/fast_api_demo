from datetime import timedelta, datetime

import uuid
from passlib.context import CryptContext

import jwt
from sqlmodel import false

from src.config import get_settings


password_context = CryptContext(schemes=["sha256_crypt"])

settings = get_settings()


def get_encrypted_password(password: str):

    hashed_pass = password_context.hash(password)

    return hashed_pass


def verify_password(password: str, hash: str):

    return password_context.verify(password, hash)


def create_access_token(
    user_data: dict,
    expiry: timedelta = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRY),
    refresh: bool = false,
):

    try:
        payload = {}

        payload["user"] = user_data
        payload["expiry"] = str(datetime.now() + expiry)
        payload["jti"] = str(uuid.uuid4())
        payload["refresh"] = str(refresh)

        token = jwt.encode(
            payload=payload, algorithm=settings.JWT_ALGORITHM, key=settings.JWT_SECRET
        )

        return token
    except Exception as e:
        print("Here is the issue", str(e))
        raise


def decode_access_token(token: str):

    try:

        token_data = jwt.decode(
            token=token, algorithms=[settings.JWT_ALGORITHM], key=settings.JWT_SECRET
        )

        return token_data
    except jwt.PyJWTError as e:
        print(e)
        return None
